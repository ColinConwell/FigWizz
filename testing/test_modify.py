"""
Tests for image modification functions
"""

import pytest
from PIL import Image
from figwizz.modify import make_image_opaque, ngon_crop


def test_make_image_opaque_rgba(sample_rgba_image):
    """Test making RGBA image opaque."""
    result = make_image_opaque(sample_rgba_image)
    assert result.mode == 'RGB'
    assert result.size == sample_rgba_image.size


def test_make_image_opaque_rgb(sample_rgb_image):
    """Test making already opaque image (should not change)."""
    result = make_image_opaque(sample_rgb_image)
    assert result.mode == 'RGB'
    assert result.size == sample_rgb_image.size


def test_make_image_opaque_custom_background(sample_rgba_image):
    """Test making image opaque with custom background color."""
    result = make_image_opaque(sample_rgba_image, bg_color=(255, 0, 0))
    assert result.mode == 'RGB'


def test_make_image_opaque_from_path(sample_image_path):
    """Test making image opaque from file path."""
    result = make_image_opaque(sample_image_path)
    assert isinstance(result, Image.Image)


def test_ngon_crop_hexagon(sample_rgb_image):
    """Test hexagon crop (default)."""
    result = ngon_crop(sample_rgb_image)
    assert isinstance(result, Image.Image)
    assert result.mode == 'RGBA'  # Should have transparency


def test_ngon_crop_different_sides(sample_rgb_image):
    """Test n-gon crop with different number of sides."""
    for sides in [3, 4, 5, 6, 8]:
        result = ngon_crop(sample_rgb_image, sides=sides)
        assert isinstance(result, Image.Image)
        assert result.mode == 'RGBA'


def test_ngon_crop_with_border(sample_rgb_image):
    """Test n-gon crop with border."""
    result = ngon_crop(sample_rgb_image, border_size=5, border_color="red")
    assert isinstance(result, Image.Image)


def test_ngon_crop_with_auto_border(sample_rgb_image):
    """Test n-gon crop with auto border color."""
    result = ngon_crop(sample_rgb_image, border_size=5, border_color="auto")
    assert isinstance(result, Image.Image)


def test_ngon_crop_with_shift(sample_rgb_image):
    """Test n-gon crop with position shift."""
    result = ngon_crop(sample_rgb_image, shift_x=10, shift_y=-10)
    assert isinstance(result, Image.Image)


def test_ngon_crop_with_rotation(sample_rgb_image):
    """Test n-gon crop with rotation."""
    result = ngon_crop(sample_rgb_image, rotation=45)
    assert isinstance(result, Image.Image)


def test_ngon_crop_with_padding(sample_rgb_image):
    """Test n-gon crop with padding."""
    result = ngon_crop(sample_rgb_image, padding=20)
    assert isinstance(result, Image.Image)


def test_ngon_crop_custom_size(sample_rgb_image):
    """Test n-gon crop with custom output size."""
    result = ngon_crop(sample_rgb_image, crop_size=(200, 200))
    assert result.size == (200, 200)


def test_ngon_crop_from_path(sample_image_path):
    """Test n-gon crop from file path."""
    result = ngon_crop(sample_image_path)
    assert isinstance(result, Image.Image)

