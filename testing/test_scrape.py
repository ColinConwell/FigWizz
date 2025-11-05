"""
Tests for scraping functions
"""

import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from figwizz.scrape import (
    download_stock_images,
    download_pixabay_images,
    download_unsplash_images,
    extract_images_from_pdf,
    extract_images_from_url,
)


@pytest.mark.requires_network
@patch('figwizz.scrape.requests.get')
def test_download_pixabay_images_success(mock_get, temp_dir):
    """Test downloading images from Pixabay."""
    # Mock API response
    mock_response = Mock()
    mock_response.json.return_value = {
        'hits': [
            {'largeImageURL': 'http://example.com/img1.jpg', 'id': 1},
            {'largeImageURL': 'http://example.com/img2.jpg', 'id': 2}
        ]
    }
    mock_response.content = b'fake_image_data'
    mock_get.return_value = mock_response
    
    result = download_pixabay_images(
        'test', 2, str(temp_dir), api_key='test_key'
    )
    
    assert len(result) == 2
    assert all(str(temp_dir) in path for path in result)


def test_download_pixabay_images_no_api_key(monkeypatch):
    """Test error handling for missing Pixabay API key."""
    monkeypatch.delenv('PIXABAY_API_KEY', raising=False)
    with pytest.raises(ValueError, match="PIXABAY_API_KEY"):
        download_pixabay_images('test', 2, 'output', api_key=None)


@patch('figwizz.scrape.requests.get')
def test_download_pixabay_images_api_error(mock_get, temp_dir):
    """Test handling of Pixabay API errors."""
    from requests import RequestException
    mock_get.side_effect = RequestException("API Error")
    
    with pytest.raises(RuntimeError, match="Failed to fetch"):
        download_pixabay_images('test', 2, str(temp_dir), api_key='test_key')


@pytest.mark.requires_network
@patch('figwizz.scrape.requests.get')
def test_download_unsplash_images_success(mock_get, temp_dir):
    """Test downloading images from Unsplash."""
    # Mock API response
    mock_response = Mock()
    mock_response.json.return_value = {
        'results': [
            {
                'urls': {'full': 'http://example.com/img1.jpg'},
                'user': {'name': 'User1', 'links': {'html': 'http://example.com/user1'}},
                'links': {'html': 'http://example.com/photo1'},
                'width': 1920,
                'height': 1080,
                'likes': 100,
                'tags': []
            }
        ]
    }
    mock_response.content = b'fake_image_data'
    mock_get.return_value = mock_response
    
    result = download_unsplash_images(
        'test', 1, str(temp_dir), api_key='test_key'
    )
    
    assert len(result) == 1


def test_download_unsplash_images_no_api_key(monkeypatch):
    """Test error handling for missing Unsplash API key."""
    monkeypatch.delenv('UNSPLASH_ACCESS_KEY', raising=False)
    with pytest.raises(ValueError, match="UNSPLASH_ACCESS_KEY"):
        download_unsplash_images('test', 2, 'output', api_key=None)


def test_download_stock_images_pixabay(temp_dir):
    """Test download_stock_images with Pixabay provider."""
    with patch('figwizz.scrape.download_pixabay_images') as mock_download:
        mock_download.return_value = ['image1.jpg', 'image2.jpg']
        result = download_stock_images('test', 2, str(temp_dir), provider='pixabay', api_key='test')
        assert len(result) == 2


def test_download_stock_images_unsplash(temp_dir):
    """Test download_stock_images with Unsplash provider."""
    with patch('figwizz.scrape.download_unsplash_images') as mock_download:
        mock_download.return_value = ['image1.jpg']
        result = download_stock_images('test', 1, str(temp_dir), provider='unsplash', api_key='test')
        assert len(result) == 1


def test_download_stock_images_invalid_provider(temp_dir):
    """Test error handling for invalid provider."""
    with pytest.raises(ValueError, match="Invalid provider"):
        download_stock_images('test', 2, str(temp_dir), provider='invalid')


@pytest.mark.requires_pymupdf
def test_extract_images_from_pdf(sample_pdf_path, temp_dir):
    """Test extracting images from PDF."""
    result = extract_images_from_pdf(sample_pdf_path, str(temp_dir))
    assert isinstance(result, list)


def test_extract_images_from_pdf_nonexistent():
    """Test error handling for nonexistent PDF."""
    import sys
    from pathlib import Path
    # The function will call sys.exit(1) for nonexistent files
    with pytest.raises(SystemExit):
        extract_images_from_pdf('/nonexistent/file.pdf', 'output')


@pytest.mark.requires_network
@patch('figwizz.scrape.requests.get')
def test_extract_images_from_url(mock_get, temp_dir):
    """Test extracting images from URL."""
    # Mock HTML response
    mock_html_response = Mock()
    mock_html_response.content = b'''
    <html>
        <body>
            <img src="http://example.com/image1.jpg"/>
            <img src="http://example.com/image2.png"/>
        </body>
    </html>
    '''
    
    # Mock image responses
    mock_image_response = Mock()
    mock_image_response.content = b'fake_image_data'
    mock_image_response.headers = {'Content-Type': 'image/jpeg'}
    
    def side_effect(*args, **kwargs):
        if 'image' in args[0]:
            return mock_image_response
        return mock_html_response
    
    mock_get.side_effect = side_effect
    
    # Need to mock Image.open to avoid actual image processing
    with patch('figwizz.scrape.Image.open'):
        result = extract_images_from_url('http://example.com', str(temp_dir))
        assert isinstance(result, list)


# Live integration tests (only run when API keys are available)
@pytest.mark.requires_network
@pytest.mark.skipif(
    not os.getenv('PIXABAY_API_KEY'),
    reason="PIXABAY_API_KEY not available in environment"
)
def test_download_pixabay_images_live(temp_dir):
    """Test downloading real images from Pixabay."""
    from figwizz import download_stock_images
    
    api_key = os.getenv('PIXABAY_API_KEY')
    if not api_key:
        pytest.skip("PIXABAY_API_KEY not set")
    
    images = download_stock_images(
        query='nature',
        n_images=2,
        output_dir=str(temp_dir),
        provider='pixabay',
        api_key=api_key
    )
    
    assert len(images) > 0
    assert all((temp_dir / img.split('/')[-1]).exists() for img in images)


@pytest.mark.requires_network
@pytest.mark.skipif(
    not os.getenv('UNSPLASH_ACCESS_KEY'),
    reason="UNSPLASH_ACCESS_KEY not available in environment"
)
def test_download_unsplash_images_live(temp_dir):
    """Test downloading real images from Unsplash."""
    from figwizz import download_stock_images
    
    api_key = os.getenv('UNSPLASH_ACCESS_KEY')
    if not api_key:
        pytest.skip("UNSPLASH_ACCESS_KEY not set")
    
    images = download_stock_images(
        query='nature',
        n_images=2,
        output_dir=str(temp_dir),
        provider='unsplash',
        api_key=api_key
    )
    
    assert len(images) > 0
    assert all((temp_dir / img.split('/')[-1]).exists() for img in images)

