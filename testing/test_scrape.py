"""
Tests for scraping functions
"""

import os
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from figwizz.scrape import (
    download_stock_images,
    download_pixabay_images,
    download_unsplash_images,
    extract_images_from_pdf,
    extract_images_from_url,
)


def test_download_pixabay_images_no_api_key(monkeypatch):
    """Test error handling for missing Pixabay API key."""
    monkeypatch.delenv('PIXABAY_API_KEY', raising=False)
    with pytest.raises(ValueError, match="PIXABAY_API_KEY"):
        download_pixabay_images('test', 2, 'output', api_key=None)


def test_download_unsplash_images_no_api_key(monkeypatch):
    """Test error handling for missing Unsplash API key."""
    monkeypatch.delenv('UNSPLASH_ACCESS_KEY', raising=False)
    with pytest.raises(ValueError, match="UNSPLASH_ACCESS_KEY"):
        download_unsplash_images('test', 2, 'output', api_key=None)


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


# Integration tests - make actual API calls
@pytest.mark.requires_network
@pytest.mark.skipif(
    not os.getenv('PIXABAY_API_KEY'),
    reason="PIXABAY_API_KEY not available in environment"
)
def test_download_pixabay_images_integration(temp_dir):
    """Test downloading real images from Pixabay."""
    api_key = os.getenv('PIXABAY_API_KEY')
    
    images = download_pixabay_images(
        query='nature',
        n_images=2,
        output_dir=str(temp_dir),
        api_key=api_key
    )
    
    assert len(images) > 0
    assert len(images) <= 2
    # Verify files actually exist
    for img_path in images:
        assert os.path.exists(img_path)
        assert str(temp_dir) in img_path
        # Verify metadata JSON also exists
        json_path = img_path.replace('.jpg', '.json')
        assert os.path.exists(json_path)


@pytest.mark.requires_network
@pytest.mark.skipif(
    not os.getenv('UNSPLASH_ACCESS_KEY'),
    reason="UNSPLASH_ACCESS_KEY not available in environment"
)
def test_download_unsplash_images_integration(temp_dir):
    """Test downloading real images from Unsplash."""
    api_key = os.getenv('UNSPLASH_ACCESS_KEY')
    
    images = download_unsplash_images(
        query='nature',
        n_images=2,
        output_dir=str(temp_dir),
        api_key=api_key
    )
    
    assert len(images) > 0
    assert len(images) <= 2
    # Verify files actually exist
    for img_path in images:
        assert os.path.exists(img_path)
        assert str(temp_dir) in img_path
        # Verify metadata JSON also exists
        json_path = img_path.replace('.jpg', '.json')
        assert os.path.exists(json_path)


@pytest.mark.requires_network
@pytest.mark.skipif(
    not os.getenv('PIXABAY_API_KEY'),
    reason="PIXABAY_API_KEY not available in environment"
)
def test_download_stock_images_pixabay_integration(temp_dir):
    """Test download_stock_images wrapper with Pixabay."""
    api_key = os.getenv('PIXABAY_API_KEY')
    
    images = download_stock_images(
        query='mountain',
        n_images=1,
        output_dir=str(temp_dir),
        provider='pixabay',
        api_key=api_key
    )
    
    assert len(images) > 0
    assert all(os.path.exists(img) for img in images)


@pytest.mark.requires_network
@pytest.mark.skipif(
    not os.getenv('UNSPLASH_ACCESS_KEY'),
    reason="UNSPLASH_ACCESS_KEY not available in environment"
)
def test_download_stock_images_unsplash_integration(temp_dir):
    """Test download_stock_images wrapper with Unsplash."""
    api_key = os.getenv('UNSPLASH_ACCESS_KEY')
    
    images = download_stock_images(
        query='mountain',
        n_images=1,
        output_dir=str(temp_dir),
        provider='unsplash',
        api_key=api_key
    )
    
    assert len(images) > 0
    assert all(os.path.exists(img) for img in images)

