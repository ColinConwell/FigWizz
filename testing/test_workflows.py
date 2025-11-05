"""
Tests for workflow functions
"""

import pytest
from PIL import Image
from figwizz.workflows import make_hexicon


def test_make_hexicon_basic(sample_rgb_image):
    """Test creating basic hexicon."""
    result = make_hexicon(sample_rgb_image)
    assert isinstance(result, Image.Image)
    assert result.mode == 'RGBA'


def test_make_hexicon_from_path(sample_image_path):
    """Test creating hexicon from file path."""
    result = make_hexicon(sample_image_path)
    assert isinstance(result, Image.Image)


def test_make_hexicon_custom_size(sample_rgb_image):
    """Test creating hexicon with custom size."""
    result = make_hexicon(sample_rgb_image, size=(200, 200))
    assert result.size == (200, 200)


def test_make_hexicon_with_border(sample_rgb_image):
    """Test creating hexicon with border."""
    result = make_hexicon(sample_rgb_image, border_size=10, border_color='red')
    assert isinstance(result, Image.Image)


def test_make_hexicon_with_shift(sample_rgb_image):
    """Test creating hexicon with position shift."""
    result = make_hexicon(sample_rgb_image, shift_x=10, shift_y=-5)
    assert isinstance(result, Image.Image)


def test_make_hexicon_with_rotation(sample_rgb_image):
    """Test creating hexicon with rotation."""
    result = make_hexicon(sample_rgb_image, rotation=30)
    assert isinstance(result, Image.Image)


def test_make_hexicon_with_auto_border(sample_rgb_image):
    """Test creating hexicon with auto border color."""
    result = make_hexicon(sample_rgb_image, border_size=5, border_color='auto')
    assert isinstance(result, Image.Image)


def test_make_hexicon_bytes_input(sample_image_bytes):
    """Test creating hexicon from bytes."""
    result = make_hexicon(sample_image_bytes)
    assert isinstance(result, Image.Image)


@pytest.mark.requires_numpy
def test_make_hexicon_numpy_input(sample_numpy_array):
    """Test creating hexicon from numpy array."""
    result = make_hexicon(sample_numpy_array)
    assert isinstance(result, Image.Image)


def test_make_hexicon_with_background_color(sample_rgb_image):
    """Test creating hexicon with background color."""
    result = make_hexicon(sample_rgb_image, background_color="white")
    assert isinstance(result, Image.Image)
    assert result.mode == 'RGBA'


def test_make_hexicon_with_background_and_border(sample_rgb_image):
    """Test creating hexicon with background color and border."""
    result = make_hexicon(sample_rgb_image, background_color="#F0F0F0",
                         border_size=10, border_color="black")
    assert isinstance(result, Image.Image)
    assert result.mode == 'RGBA'

