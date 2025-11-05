"""
Tests for stitching and PDF functions
"""

import pytest
from pathlib import Path
from figwizz.stitchkit import crop_whitespace, convert_to_pdf


def test_crop_whitespace_single_image(sample_image_path, temp_dir):
    """Test cropping whitespace from single image."""
    output_path = temp_dir / "cropped.png"
    crop_whitespace(sample_image_path, str(output_path))
    assert output_path.exists()


def test_crop_whitespace_directory(temp_dir, sample_rgb_image):
    """Test cropping whitespace from directory of images."""
    # Create some test images
    for i in range(3):
        img_path = temp_dir / f"image{i}.png"
        sample_rgb_image.save(img_path)
    
    # Crop all images
    crop_whitespace(str(temp_dir))
    
    # Verify images still exist (modified in place)
    assert (temp_dir / "image0.png").exists()


def test_crop_whitespace_with_margin(sample_image_path, temp_dir):
    """Test cropping with custom margin."""
    output_path = temp_dir / "cropped_margin.png"
    crop_whitespace(sample_image_path, str(output_path), margin_size='0.5cm', dpi=300)
    assert output_path.exists()


def test_convert_to_pdf_single_image(sample_image_path, temp_dir):
    """Test converting single image to PDF."""
    # Convert in place - output will be test_image.pdf next to test_image.png
    convert_to_pdf(sample_image_path, None)
    
    # Check PDF exists next to original
    pdf_file = temp_dir / "test_image.pdf"
    assert pdf_file.exists()


def test_convert_to_pdf_directory(temp_dir, sample_rgb_image):
    """Test converting directory of images to PDF."""
    # Create test images
    img_dir = temp_dir / "images"
    img_dir.mkdir()
    
    for i in range(2):
        img_path = img_dir / f"image{i}.png"
        sample_rgb_image.save(img_path)
    
    # Convert to PDF
    convert_to_pdf(str(img_dir))
    
    # Check for PDF files
    pdf_files = list(img_dir.glob("*.pdf"))
    assert len(pdf_files) > 0


def test_convert_to_pdf_custom_dpi(sample_image_path, temp_dir):
    """Test converting with custom DPI."""
    # Convert in place
    convert_to_pdf(sample_image_path, None, dpi=150)
    
    # Check PDF exists next to original
    pdf_file = temp_dir / "test_image.pdf"
    assert pdf_file.exists()


def test_convert_to_pdf_rgba(sample_rgba_image, temp_dir):
    """Test converting RGBA image to PDF (should convert to RGB)."""
    rgba_path = temp_dir / "test_rgba.png"
    sample_rgba_image.save(rgba_path)
    
    # Convert in place
    convert_to_pdf(str(rgba_path), None)
    
    pdf_file = temp_dir / "test_rgba.pdf"
    assert pdf_file.exists()

