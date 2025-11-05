"""
Utility functions for tests
"""

from PIL import Image
import numpy as np


def create_test_image(width=100, height=100, color=(255, 0, 0), mode='RGB'):
    """Create a test image with specified parameters."""
    return Image.new(mode, (width, height), color=color)


def create_gradient_image(width=100, height=100):
    """Create a test image with a color gradient."""
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    for i in range(width):
        for j in range(height):
            pixels[i, j] = (i * 255 // width, j * 255 // height, 128)
    return img


def create_test_pattern_image(width=100, height=100):
    """Create a test image with a checkerboard pattern."""
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    square_size = 10
    for i in range(width):
        for j in range(height):
            if ((i // square_size) + (j // square_size)) % 2 == 0:
                pixels[i, j] = (255, 255, 255)
            else:
                pixels[i, j] = (0, 0, 0)
    return img


def images_are_similar(img1, img2, threshold=0.95):
    """
    Check if two images are similar.
    
    Args:
        img1: First PIL Image
        img2: Second PIL Image
        threshold: Similarity threshold (0-1)
    
    Returns:
        True if images are similar above threshold
    """
    if img1.size != img2.size:
        return False
    
    if img1.mode != img2.mode:
        return False
    
    # Convert to numpy arrays
    arr1 = np.array(img1)
    arr2 = np.array(img2)
    
    # Calculate similarity
    if arr1.shape != arr2.shape:
        return False
    
    # Calculate percentage of matching pixels
    matching = np.sum(arr1 == arr2)
    total = arr1.size
    similarity = matching / total
    
    return similarity >= threshold


def assert_image_dimensions(img, expected_width, expected_height):
    """Assert that an image has expected dimensions."""
    assert img.width == expected_width, f"Expected width {expected_width}, got {img.width}"
    assert img.height == expected_height, f"Expected height {expected_height}, got {img.height}"


def assert_image_mode(img, expected_mode):
    """Assert that an image has expected mode."""
    assert img.mode == expected_mode, f"Expected mode {expected_mode}, got {img.mode}"

