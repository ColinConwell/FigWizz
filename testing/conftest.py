"""
Pytest configuration and fixtures for FigWizard tests
"""

import pytest
import tempfile
import shutil
import os
from pathlib import Path
from PIL import Image
import numpy as np


# Load environment variables from .env.local if available
def pytest_configure(config):
    """Load .env.local file before running tests."""
    env_file = Path('.env.local')
    if env_file.exists():
        print(f"\nLoading environment from {env_file}")
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, _, value = line.partition('=')
                    key = key.strip()
                    value = value.strip()
                    # Remove quotes if present
                    if value and value[0] in ('"', "'") and value[-1] == value[0]:
                        value = value[1:-1]
                    os.environ[key] = value
    else:
        print(f"\nNo .env.local file found, skipping environment setup")


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test outputs."""
    tmpdir = tempfile.mkdtemp()
    yield Path(tmpdir)
    shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.fixture
def sample_rgb_image():
    """Create a simple RGB test image."""
    img = Image.new('RGB', (100, 100), color=(255, 0, 0))
    return img


@pytest.fixture
def sample_rgba_image():
    """Create a simple RGBA test image with transparency."""
    img = Image.new('RGBA', (100, 100), color=(0, 255, 0, 128))
    return img


@pytest.fixture
def sample_grayscale_image():
    """Create a simple grayscale test image."""
    img = Image.new('L', (100, 100), color=128)
    return img


@pytest.fixture
def sample_image_path(temp_dir, sample_rgb_image):
    """Save a test image to disk and return its path."""
    path = temp_dir / "test_image.png"
    sample_rgb_image.save(path)
    return str(path)


@pytest.fixture
def sample_image_bytes(sample_rgb_image):
    """Return a test image as bytes."""
    from io import BytesIO
    buffer = BytesIO()
    sample_rgb_image.save(buffer, format='PNG')
    return buffer.getvalue()


@pytest.fixture
def sample_numpy_array():
    """Return a test image as numpy array."""
    return np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)


@pytest.fixture
def multiple_test_images():
    """Create a list of test images with different colors."""
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    return [Image.new('RGB', (100, 100), color=c) for c in colors]


@pytest.fixture
def sample_svg_content():
    """Return sample SVG content."""
    return b'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
    <rect width="100" height="100" fill="red"/>
</svg>'''


@pytest.fixture
def mock_env_file(temp_dir):
    """Create a mock .env file for testing."""
    env_content = """# Test environment file
PIXABAY_API_KEY=test_pixabay_key
UNSPLASH_ACCESS_KEY=test_unsplash_key
OPENAI_API_KEY=test_openai_key
TEST_VAR="quoted value"
TEST_VAR_WITH_COMMENT=value # inline comment
"""
    env_path = temp_dir / ".env"
    env_path.write_text(env_content)
    return str(env_path)


@pytest.fixture
def sample_pdf_path(temp_dir, multiple_test_images):
    """Create a sample PDF file for testing."""
    try:
        import fitz  # PyMuPDF
        pdf_path = temp_dir / "test.pdf"
        doc = fitz.open()
        
        for img in multiple_test_images:
            # Convert PIL image to bytes
            from io import BytesIO
            img_bytes = BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes = img_bytes.getvalue()
            
            # Add page with image
            page = doc.new_page(width=100, height=100)
            page.insert_image(page.rect, stream=img_bytes)
        
        doc.save(pdf_path)
        doc.close()
        return str(pdf_path)
    except ImportError:
        pytest.skip("PyMuPDF not installed, skipping PDF test")


    # Add skip markers
    config.addinivalue_line(
        "markers", "requires_pymupdf: mark test as requiring PyMuPDF"
    )
    config.addinivalue_line(
        "markers", "requires_litellm: mark test as requiring litellm"
    )
    config.addinivalue_line(
        "markers", "requires_cairosvg: mark test as requiring cairosvg"
    )
    config.addinivalue_line(
        "markers", "requires_network: mark test as requiring network access"
    )

