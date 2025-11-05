"""
Tests for unified image handling utilities
"""

import pytest
from PIL import Image
import base64
from io import BytesIO
from figwizz.utils.images import (
    normalize_image_input,
    normalize_image_output,
    save_image,
    is_image_path,
    is_url,
)


def test_normalize_image_input_pil(sample_rgb_image):
    """Test normalizing PIL Image input."""
    result = normalize_image_input(sample_rgb_image)
    assert isinstance(result, Image.Image)
    assert result.size == sample_rgb_image.size


def test_normalize_image_input_path(sample_image_path):
    """Test normalizing path string input."""
    result = normalize_image_input(sample_image_path)
    assert isinstance(result, Image.Image)
    assert result.size == (100, 100)


def test_normalize_image_input_bytes(sample_image_bytes):
    """Test normalizing bytes input."""
    result = normalize_image_input(sample_image_bytes)
    assert isinstance(result, Image.Image)


def test_normalize_image_input_base64(sample_rgb_image):
    """Test normalizing base64 string input."""
    # Convert image to base64
    buffer = BytesIO()
    sample_rgb_image.save(buffer, format='PNG')
    b64_string = base64.b64encode(buffer.getvalue()).decode()
    
    result = normalize_image_input(b64_string)
    assert isinstance(result, Image.Image)


@pytest.mark.requires_numpy
def test_normalize_image_input_numpy(sample_numpy_array):
    """Test normalizing numpy array input."""
    result = normalize_image_input(sample_numpy_array)
    assert isinstance(result, Image.Image)


def test_normalize_image_input_file_like(sample_image_bytes):
    """Test normalizing file-like object input."""
    file_like = BytesIO(sample_image_bytes)
    result = normalize_image_input(file_like)
    assert isinstance(result, Image.Image)


def test_normalize_image_input_invalid():
    """Test error handling for invalid input."""
    with pytest.raises(ValueError):
        normalize_image_input(12345)


def test_normalize_image_input_nonexistent_path():
    """Test error handling for nonexistent file path."""
    with pytest.raises(FileNotFoundError):
        normalize_image_input('/nonexistent/path/to/image.png')


def test_normalize_image_output_pil(sample_rgb_image):
    """Test converting to PIL format."""
    result = normalize_image_output(sample_rgb_image, 'pil')
    assert isinstance(result, Image.Image)


def test_normalize_image_output_bytes(sample_rgb_image):
    """Test converting to bytes format."""
    result = normalize_image_output(sample_rgb_image, 'bytes')
    assert isinstance(result, bytes)


@pytest.mark.requires_numpy
def test_normalize_image_output_numpy(sample_rgb_image):
    """Test converting to numpy format."""
    import numpy as np
    result = normalize_image_output(sample_rgb_image, 'numpy')
    assert isinstance(result, np.ndarray)


def test_save_image(sample_rgb_image, temp_dir):
    """Test saving image to file."""
    output_path = temp_dir / "output.png"
    result_path = save_image(sample_rgb_image, str(output_path))
    assert output_path.exists()
    assert result_path == str(output_path)


def test_save_image_auto_format(sample_rgb_image, temp_dir):
    """Test automatic format detection from extension."""
    output_path = temp_dir / "output.jpg"
    save_image(sample_rgb_image, str(output_path))
    assert output_path.exists()
    
    # Load and verify it's JPEG
    loaded = Image.open(output_path)
    assert loaded.format == 'JPEG'


def test_save_image_make_opaque(sample_rgba_image, temp_dir):
    """Test making image opaque when saving as JPEG."""
    output_path = temp_dir / "output.jpg"
    save_image(sample_rgba_image, str(output_path))
    assert output_path.exists()
    
    loaded = Image.open(output_path)
    assert loaded.mode == 'RGB'  # Should be converted


def test_is_url():
    """Test URL detection."""
    assert is_url('http://example.com/image.png')
    assert is_url('https://example.com/image.png')
    assert not is_url('/path/to/image.png')
    assert not is_url('image.png')


def test_is_image_path(sample_image_path):
    """Test image path detection."""
    assert is_image_path(sample_image_path)
    assert not is_image_path('/nonexistent/path.png')
    assert not is_image_path('http://example.com/image.png')

