"""
Tests for image conversion functions
"""

import pytest
from PIL import Image
from figwizz.convert import convert_image, bytes_to_image, svg_to_image


def test_convert_image_png_to_jpg(sample_image_path, temp_dir):
    """Test converting PNG to JPEG."""
    result_path = convert_image(sample_image_path, 'jpg')
    assert result_path.endswith('.jpg')
    
    loaded = Image.open(result_path)
    assert loaded.format == 'JPEG'


def test_convert_image_with_deletion(sample_image_path, temp_dir):
    """Test converting with original file deletion."""
    import shutil
    import os
    
    # Make a copy to test deletion
    test_path = str(temp_dir / "test_delete.png")
    shutil.copy(sample_image_path, test_path)
    
    result_path = convert_image(test_path, 'jpg', delete_original=True)
    assert not os.path.exists(test_path)
    assert os.path.exists(result_path)


def test_convert_image_rgba_to_jpg(sample_rgba_image, temp_dir):
    """Test converting RGBA to JPEG (should make opaque)."""
    # Save RGBA image first
    rgba_path = temp_dir / "test_rgba.png"
    sample_rgba_image.save(rgba_path)
    
    result_path = convert_image(str(rgba_path), 'jpg')
    loaded = Image.open(result_path)
    assert loaded.mode == 'RGB'


def test_bytes_to_image(sample_image_bytes):
    """Test converting bytes to PIL Image."""
    result = bytes_to_image(sample_image_bytes)
    assert isinstance(result, Image.Image)


def test_bytes_to_image_base64(sample_rgb_image):
    """Test converting base64 string to PIL Image."""
    import base64
    from io import BytesIO
    
    buffer = BytesIO()
    sample_rgb_image.save(buffer, format='PNG')
    b64_string = base64.b64encode(buffer.getvalue()).decode()
    
    result = bytes_to_image(b64_string)
    assert isinstance(result, Image.Image)


def test_bytes_to_image_invalid():
    """Test error handling for invalid bytes input."""
    with pytest.raises(ValueError):
        bytes_to_image(12345)


def test_svg_to_image(sample_svg_content, temp_dir):
    """Test converting SVG to PNG."""
    try:
        import cairosvg
        # Try to actually use it to see if cairo C library is available
        from io import BytesIO
        cairosvg.svg2png(bytestring=sample_svg_content, write_to=BytesIO())
    except (ImportError, OSError) as e:
        pytest.skip(f"cairosvg/cairo library not fully available: install cairo with 'brew install cairo' (macOS) or 'apt-get install libcairo2' (Linux)")
    
    output_path = temp_dir / "output.png"
    result = svg_to_image(sample_svg_content, str(output_path))
    assert result is True
    assert output_path.exists()


def test_svg_to_image_invalid_output(sample_svg_content, temp_dir):
    """Test error handling for invalid output path."""
    output_path = temp_dir / "output.txt"
    with pytest.raises(ValueError):
        svg_to_image(sample_svg_content, str(output_path))

