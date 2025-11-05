"""
Tests for color processing utilities
"""

import pytest
from figwizz.colors import parse_color, extract_dominant_color, get_contrasting_color


def test_parse_color_hex():
    """Test parsing hex color."""
    result = parse_color('#FF5733')
    assert result == (255, 87, 51)


def test_parse_color_rgb_tuple():
    """Test parsing RGB tuple."""
    result = parse_color((255, 87, 51))
    assert result == (255, 87, 51)


def test_parse_color_name():
    """Test parsing color name."""
    result = parse_color('red')
    assert result == (255, 0, 0)


def test_parse_color_invalid():
    """Test error handling for invalid color."""
    with pytest.raises(ValueError):
        parse_color('not_a_color')


def test_extract_dominant_color(sample_rgb_image):
    """Test extracting dominant color from image."""
    result = extract_dominant_color(sample_rgb_image)
    assert isinstance(result, tuple)
    assert len(result) == 3
    assert all(0 <= c <= 255 for c in result)


def test_extract_dominant_color_rgba(sample_rgba_image):
    """Test extracting dominant color from RGBA image."""
    result = extract_dominant_color(sample_rgba_image)
    assert isinstance(result, tuple)
    assert len(result) == 3


def test_get_contrasting_color_light():
    """Test getting contrasting color for light color."""
    light_color = (240, 240, 240)
    result = get_contrasting_color(light_color, prefer_dark=True)
    assert isinstance(result, tuple)
    assert len(result) == 3
    # Should be dark
    assert sum(result) < sum(light_color)


def test_get_contrasting_color_dark():
    """Test getting contrasting color for dark color."""
    dark_color = (20, 20, 20)
    result = get_contrasting_color(dark_color, prefer_dark=False)
    assert isinstance(result, tuple)
    assert len(result) == 3
    # Should be light
    assert sum(result) > sum(dark_color)


def test_get_contrasting_color_prefer_dark():
    """Test prefer_dark parameter."""
    color = (128, 128, 128)
    result_dark = get_contrasting_color(color, prefer_dark=True)
    result_light = get_contrasting_color(color, prefer_dark=False)
    assert result_dark != result_light

