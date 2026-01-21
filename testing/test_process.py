"""
Tests for image processing functions
"""

import pytest
from PIL import Image
import numpy as np
from figwizz.process import (
    load_image,
    resize_image,
    crop_image,
    rotate_image,
    flip_image,
    apply_filter,
    apply_mask,
    apply_transform,
)


# =============================================================================
# load_image tests
# =============================================================================

def test_load_image_from_path(sample_image_path):
    """Test loading image from file path."""
    result = load_image(sample_image_path)
    assert isinstance(result, Image.Image)
    assert result.size == (100, 100)


def test_load_image_from_pil(sample_rgb_image):
    """Test loading image from PIL Image."""
    result = load_image(sample_rgb_image)
    assert isinstance(result, Image.Image)
    assert result.size == sample_rgb_image.size


def test_load_image_from_bytes(sample_image_bytes):
    """Test loading image from bytes."""
    result = load_image(sample_image_bytes)
    assert isinstance(result, Image.Image)


def test_load_image_from_numpy(sample_numpy_array):
    """Test loading image from numpy array."""
    result = load_image(sample_numpy_array)
    assert isinstance(result, Image.Image)


def test_load_image_to_numpy(sample_image_path):
    """Test loading image as numpy array output."""
    result = load_image(sample_image_path, output_type='numpy')
    assert isinstance(result, np.ndarray)
    assert result.shape[:2] == (100, 100)


def test_load_image_to_bytes(sample_image_path):
    """Test loading image as bytes output."""
    result = load_image(sample_image_path, output_type='bytes')
    assert isinstance(result, bytes)


# =============================================================================
# resize_image tests
# =============================================================================

def test_resize_image_by_width(sample_rgb_image):
    """Test resizing by width only."""
    result = resize_image(sample_rgb_image, width=50)
    assert result.width == 50
    assert result.height == 50  # Maintains aspect ratio


def test_resize_image_by_height(sample_rgb_image):
    """Test resizing by height only."""
    result = resize_image(sample_rgb_image, height=50)
    assert result.height == 50
    assert result.width == 50  # Maintains aspect ratio


def test_resize_image_by_scale(sample_rgb_image):
    """Test resizing by scale factor."""
    result = resize_image(sample_rgb_image, scale=0.5)
    assert result.size == (50, 50)


def test_resize_image_double_scale(sample_rgb_image):
    """Test resizing by scale factor > 1."""
    result = resize_image(sample_rgb_image, scale=2.0)
    assert result.size == (200, 200)


def test_resize_image_explicit_dimensions(sample_rgb_image):
    """Test resizing with explicit dimensions, ignoring aspect ratio."""
    result = resize_image(sample_rgb_image, width=80, height=60, maintain_aspect=False)
    assert result.size == (80, 60)


def test_resize_image_fit_within_bounds(sample_rgb_image):
    """Test resizing to fit within bounds while maintaining aspect ratio."""
    result = resize_image(sample_rgb_image, width=200, height=50)
    # Square image should fit to height constraint
    assert result.height == 50
    assert result.width == 50


def test_resize_image_from_path(sample_image_path):
    """Test resizing from file path."""
    result = resize_image(sample_image_path, width=50)
    assert isinstance(result, Image.Image)
    assert result.width == 50


def test_resize_image_no_dimensions_raises():
    """Test that resize without dimensions raises error."""
    img = Image.new('RGB', (100, 100))
    with pytest.raises(ValueError):
        resize_image(img)


# =============================================================================
# crop_image tests
# =============================================================================

def test_crop_image_by_box(sample_rgb_image):
    """Test cropping by explicit box coordinates."""
    result = crop_image(sample_rgb_image, box=(10, 10, 60, 60))
    assert result.size == (50, 50)


def test_crop_image_by_center_and_size(sample_rgb_image):
    """Test cropping by center point and size."""
    result = crop_image(sample_rgb_image, center=(50, 50), size=(40, 40))
    assert result.size == (40, 40)


def test_crop_image_by_size_only(sample_rgb_image):
    """Test cropping from image center with size only."""
    result = crop_image(sample_rgb_image, size=(50, 50))
    assert result.size == (50, 50)


def test_crop_image_from_path(sample_image_path):
    """Test cropping from file path."""
    result = crop_image(sample_image_path, box=(0, 0, 50, 50))
    assert isinstance(result, Image.Image)
    assert result.size == (50, 50)


def test_crop_image_no_params_raises():
    """Test that crop without parameters raises error."""
    img = Image.new('RGB', (100, 100))
    with pytest.raises(ValueError):
        crop_image(img)


# =============================================================================
# rotate_image tests
# =============================================================================

def test_rotate_image_90_degrees(sample_rgb_image):
    """Test 90 degree rotation."""
    result = rotate_image(sample_rgb_image, angle=90)
    assert isinstance(result, Image.Image)


def test_rotate_image_45_degrees_expand(sample_rgb_image):
    """Test 45 degree rotation with expansion."""
    result = rotate_image(sample_rgb_image, angle=45, expand=True)
    # Expanded image should be larger
    assert result.width > sample_rgb_image.width
    assert result.height > sample_rgb_image.height


def test_rotate_image_no_expand(sample_rgb_image):
    """Test rotation without expansion."""
    result = rotate_image(sample_rgb_image, angle=45, expand=False)
    assert result.size == sample_rgb_image.size


def test_rotate_image_with_fill_color(sample_rgb_image):
    """Test rotation with fill color."""
    result = rotate_image(sample_rgb_image, angle=45, fill_color=(255, 255, 255))
    assert isinstance(result, Image.Image)


def test_rotate_image_rgba(sample_rgba_image):
    """Test rotation of RGBA image."""
    result = rotate_image(sample_rgba_image, angle=30)
    assert isinstance(result, Image.Image)


def test_rotate_image_from_path(sample_image_path):
    """Test rotation from file path."""
    result = rotate_image(sample_image_path, angle=90)
    assert isinstance(result, Image.Image)


# =============================================================================
# flip_image tests
# =============================================================================

def test_flip_image_horizontal(sample_rgb_image):
    """Test horizontal flip."""
    result = flip_image(sample_rgb_image, direction='horizontal')
    assert isinstance(result, Image.Image)
    assert result.size == sample_rgb_image.size


def test_flip_image_vertical(sample_rgb_image):
    """Test vertical flip."""
    result = flip_image(sample_rgb_image, direction='vertical')
    assert isinstance(result, Image.Image)
    assert result.size == sample_rgb_image.size


def test_flip_image_both(sample_rgb_image):
    """Test both horizontal and vertical flip."""
    result = flip_image(sample_rgb_image, direction='both')
    assert isinstance(result, Image.Image)
    assert result.size == sample_rgb_image.size


def test_flip_image_shorthand_h(sample_rgb_image):
    """Test horizontal flip with shorthand 'h'."""
    result = flip_image(sample_rgb_image, direction='h')
    assert isinstance(result, Image.Image)


def test_flip_image_shorthand_v(sample_rgb_image):
    """Test vertical flip with shorthand 'v'."""
    result = flip_image(sample_rgb_image, direction='v')
    assert isinstance(result, Image.Image)


def test_flip_image_from_path(sample_image_path):
    """Test flip from file path."""
    result = flip_image(sample_image_path, direction='horizontal')
    assert isinstance(result, Image.Image)


def test_flip_image_invalid_direction():
    """Test that invalid direction raises error."""
    img = Image.new('RGB', (100, 100))
    with pytest.raises(ValueError):
        flip_image(img, direction='diagonal')


# =============================================================================
# apply_filter tests
# =============================================================================

def test_apply_filter_blur(sample_rgb_image):
    """Test Gaussian blur filter."""
    result = apply_filter(sample_rgb_image, 'blur', radius=2)
    assert isinstance(result, Image.Image)
    assert result.size == sample_rgb_image.size


def test_apply_filter_box_blur(sample_rgb_image):
    """Test box blur filter."""
    result = apply_filter(sample_rgb_image, 'box_blur', radius=3)
    assert isinstance(result, Image.Image)


def test_apply_filter_sharpen(sample_rgb_image):
    """Test sharpen filter."""
    result = apply_filter(sample_rgb_image, 'sharpen')
    assert isinstance(result, Image.Image)


def test_apply_filter_smooth(sample_rgb_image):
    """Test smooth filter."""
    result = apply_filter(sample_rgb_image, 'smooth')
    assert isinstance(result, Image.Image)


def test_apply_filter_detail(sample_rgb_image):
    """Test detail filter."""
    result = apply_filter(sample_rgb_image, 'detail')
    assert isinstance(result, Image.Image)


def test_apply_filter_edge(sample_rgb_image):
    """Test edge detection filter."""
    result = apply_filter(sample_rgb_image, 'edge')
    assert isinstance(result, Image.Image)


def test_apply_filter_contour(sample_rgb_image):
    """Test contour filter."""
    result = apply_filter(sample_rgb_image, 'contour')
    assert isinstance(result, Image.Image)


def test_apply_filter_emboss(sample_rgb_image):
    """Test emboss filter."""
    result = apply_filter(sample_rgb_image, 'emboss')
    assert isinstance(result, Image.Image)


def test_apply_filter_brightness(sample_rgb_image):
    """Test brightness adjustment."""
    result = apply_filter(sample_rgb_image, 'brightness', factor=1.5)
    assert isinstance(result, Image.Image)


def test_apply_filter_contrast(sample_rgb_image):
    """Test contrast adjustment."""
    result = apply_filter(sample_rgb_image, 'contrast', factor=1.5)
    assert isinstance(result, Image.Image)


def test_apply_filter_saturation(sample_rgb_image):
    """Test saturation adjustment."""
    result = apply_filter(sample_rgb_image, 'saturation', factor=1.5)
    assert isinstance(result, Image.Image)


def test_apply_filter_sharpness(sample_rgb_image):
    """Test sharpness adjustment."""
    result = apply_filter(sample_rgb_image, 'sharpness', factor=2.0)
    assert isinstance(result, Image.Image)


def test_apply_filter_grayscale(sample_rgb_image):
    """Test grayscale conversion."""
    result = apply_filter(sample_rgb_image, 'grayscale')
    assert result.mode == 'L'


def test_apply_filter_grayscale_rgba(sample_rgba_image):
    """Test grayscale conversion preserves alpha."""
    result = apply_filter(sample_rgba_image, 'grayscale')
    assert result.mode == 'RGBA'


def test_apply_filter_invert(sample_rgb_image):
    """Test color inversion."""
    result = apply_filter(sample_rgb_image, 'invert')
    assert isinstance(result, Image.Image)


def test_apply_filter_invert_rgba(sample_rgba_image):
    """Test color inversion preserves alpha."""
    result = apply_filter(sample_rgba_image, 'invert')
    assert result.mode == 'RGBA'


def test_apply_filter_from_path(sample_image_path):
    """Test filter from file path."""
    result = apply_filter(sample_image_path, 'blur')
    assert isinstance(result, Image.Image)


def test_apply_filter_unknown_raises():
    """Test that unknown filter raises error."""
    img = Image.new('RGB', (100, 100))
    with pytest.raises(ValueError):
        apply_filter(img, 'nonexistent_filter')


# =============================================================================
# apply_mask tests
# =============================================================================

def test_apply_mask_basic(sample_rgb_image):
    """Test basic mask application."""
    # Create a simple circular mask
    mask = Image.new('L', (100, 100), 0)
    from PIL import ImageDraw
    draw = ImageDraw.Draw(mask)
    draw.ellipse((10, 10, 90, 90), fill=255)
    
    result = apply_mask(sample_rgb_image, mask)
    assert result.mode == 'RGBA'


def test_apply_mask_invert(sample_rgb_image):
    """Test inverted mask application."""
    mask = Image.new('L', (100, 100), 255)
    result = apply_mask(sample_rgb_image, mask, invert=True)
    assert result.mode == 'RGBA'


def test_apply_mask_resize(sample_rgb_image):
    """Test mask is resized to match image."""
    # Create mask of different size
    mask = Image.new('L', (50, 50), 255)
    result = apply_mask(sample_rgb_image, mask)
    assert result.size == sample_rgb_image.size


def test_apply_mask_from_path(sample_image_path, temp_dir):
    """Test mask from file paths."""
    # Create and save mask
    mask = Image.new('L', (100, 100), 255)
    mask_path = temp_dir / "mask.png"
    mask.save(mask_path)
    
    result = apply_mask(sample_image_path, str(mask_path))
    assert isinstance(result, Image.Image)


# =============================================================================
# apply_transform tests
# =============================================================================

def test_apply_transform_transpose(sample_rgb_image):
    """Test transpose transform."""
    result = apply_transform(sample_rgb_image, 'transpose')
    assert isinstance(result, Image.Image)


def test_apply_transform_pad(sample_rgb_image):
    """Test padding transform."""
    result = apply_transform(sample_rgb_image, 'pad', padding=20)
    assert result.width == sample_rgb_image.width + 40
    assert result.height == sample_rgb_image.height + 40


def test_apply_transform_pad_asymmetric(sample_rgb_image):
    """Test padding with different horizontal/vertical values."""
    result = apply_transform(sample_rgb_image, 'pad', padding=(10, 20))
    assert result.width == sample_rgb_image.width + 20
    assert result.height == sample_rgb_image.height + 40


def test_apply_transform_pad_with_color(sample_rgb_image):
    """Test padding with fill color."""
    result = apply_transform(sample_rgb_image, 'pad', padding=10, fill_color=(255, 0, 0))
    assert isinstance(result, Image.Image)


def test_apply_transform_fit(sample_rgb_image):
    """Test fit transform with letterboxing."""
    result = apply_transform(sample_rgb_image, 'fit', size=(200, 100))
    assert result.size == (200, 100)


def test_apply_transform_fit_with_color(sample_rgb_image):
    """Test fit transform with custom letterbox color."""
    result = apply_transform(sample_rgb_image, 'fit', size=(200, 100), fill_color=(128, 128, 128))
    assert result.size == (200, 100)


def test_apply_transform_autocontrast(sample_rgb_image):
    """Test autocontrast transform."""
    result = apply_transform(sample_rgb_image, 'autocontrast')
    assert isinstance(result, Image.Image)


def test_apply_transform_autocontrast_rgba(sample_rgba_image):
    """Test autocontrast preserves alpha."""
    result = apply_transform(sample_rgba_image, 'autocontrast')
    assert result.mode == 'RGBA'


def test_apply_transform_equalize(sample_rgb_image):
    """Test histogram equalization."""
    result = apply_transform(sample_rgb_image, 'equalize')
    assert isinstance(result, Image.Image)


def test_apply_transform_posterize(sample_rgb_image):
    """Test posterize transform."""
    result = apply_transform(sample_rgb_image, 'posterize', bits=4)
    assert isinstance(result, Image.Image)


def test_apply_transform_solarize(sample_rgb_image):
    """Test solarize transform."""
    result = apply_transform(sample_rgb_image, 'solarize', threshold=128)
    assert isinstance(result, Image.Image)


def test_apply_transform_from_path(sample_image_path):
    """Test transform from file path."""
    result = apply_transform(sample_image_path, 'pad', padding=10)
    assert isinstance(result, Image.Image)


def test_apply_transform_unknown_raises():
    """Test that unknown transform raises error."""
    img = Image.new('RGB', (100, 100))
    with pytest.raises(ValueError):
        apply_transform(img, 'nonexistent_transform')


def test_apply_transform_perspective_requires_coefficients():
    """Test that perspective transform requires coefficients."""
    img = Image.new('RGB', (100, 100))
    with pytest.raises(ValueError):
        apply_transform(img, 'perspective')


def test_apply_transform_affine_requires_matrix():
    """Test that affine transform requires matrix."""
    img = Image.new('RGB', (100, 100))
    with pytest.raises(ValueError):
        apply_transform(img, 'affine')


def test_apply_transform_fit_requires_size():
    """Test that fit transform requires size."""
    img = Image.new('RGB', (100, 100))
    with pytest.raises(ValueError):
        apply_transform(img, 'fit')


# =============================================================================
# Integration tests
# =============================================================================

def test_chain_operations(sample_rgb_image):
    """Test chaining multiple operations."""
    result = sample_rgb_image
    result = resize_image(result, scale=0.5)
    result = rotate_image(result, angle=45)
    result = apply_filter(result, 'blur', radius=1)
    result = flip_image(result, 'horizontal')
    
    assert isinstance(result, Image.Image)


def test_operations_preserve_rgba(sample_rgba_image):
    """Test that operations preserve RGBA mode when appropriate."""
    result = resize_image(sample_rgba_image, scale=0.5)
    assert result.mode == 'RGBA'
    
    result = rotate_image(sample_rgba_image, angle=45)
    assert result.mode == 'RGBA'
    
    result = flip_image(sample_rgba_image, 'horizontal')
    assert result.mode == 'RGBA'


def test_grayscale_image_operations(sample_grayscale_image):
    """Test operations on grayscale images."""
    result = resize_image(sample_grayscale_image, scale=0.5)
    assert isinstance(result, Image.Image)
    
    result = rotate_image(sample_grayscale_image, angle=90)
    assert isinstance(result, Image.Image)
    
    result = flip_image(sample_grayscale_image, 'vertical')
    assert isinstance(result, Image.Image)
