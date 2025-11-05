"""
Tests for image display functions
"""

import pytest
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing
from figwizz.display import make_image_grid


def test_make_image_grid_basic(multiple_test_images):
    """Test creating basic image grid."""
    fig, axes = make_image_grid(multiple_test_images)
    assert fig is not None
    assert axes is not None


def test_make_image_grid_with_titles(multiple_test_images):
    """Test creating image grid with titles."""
    titles = ['Red', 'Green', 'Blue', 'Yellow']
    fig, axes = make_image_grid(multiple_test_images, titles=titles)
    assert fig is not None


def test_make_image_grid_max_cols(multiple_test_images):
    """Test creating image grid with max columns."""
    fig, axes = make_image_grid(multiple_test_images, max_cols=2)
    assert fig is not None


def test_make_image_grid_show_index(multiple_test_images):
    """Test creating image grid with index."""
    fig, axes = make_image_grid(multiple_test_images, show_index=True)
    assert fig is not None


def test_make_image_grid_custom_figsize(multiple_test_images):
    """Test creating image grid with custom figure size."""
    fig, axes = make_image_grid(multiple_test_images, figsize=(12, 8))
    assert fig is not None
    assert fig.get_figwidth() == 12
    assert fig.get_figheight() == 8


def test_make_image_grid_show_axes(multiple_test_images):
    """Test creating image grid with axes shown."""
    fig, axes = make_image_grid(multiple_test_images, show_axes=True)
    assert fig is not None


def test_make_image_grid_empty():
    """Test error handling for empty image list."""
    fig, axes = make_image_grid([])
    assert fig is None
    assert axes is None


def test_make_image_grid_single_image(sample_rgb_image):
    """Test creating grid with single image."""
    fig, axes = make_image_grid([sample_rgb_image])
    assert fig is not None


def test_make_image_grid_mixed_inputs(sample_rgb_image, sample_image_path):
    """Test creating grid with mixed input types."""
    images = [sample_rgb_image, sample_image_path]
    fig, axes = make_image_grid(images)
    assert fig is not None

