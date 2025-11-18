# FigWizz Justfile
# Development automation commands

# Default recipe (list all commands)
default:
    @just --list

# Installation commands
# =====================

# Install package in development mode
install:
    pip install -e .

# Install with all optional dependencies
install-all:
    pip install -e ".[genai,pdf,svg,dev,docs]"

# Install development dependencies only
install-dev:
    pip install -e ".[dev]"

# Install documentation dependencies
install-docs:
    pip install -e ".[docs]"

# Testing commands
# ================

# Run all tests
test:
    pytest

# Run tests with coverage report
test-cov:
    pytest --cov=figwizz --cov-report=html --cov-report=term

# Run specific test file
test-file FILE:
    pytest {{FILE}} -v

# Run tests matching pattern
test-match PATTERN:
    pytest -k "{{PATTERN}}" -v

# Run tests without network dependencies
test-offline:
    pytest -m "not requires_network"

# Code quality commands
# ======================

# Format code with black
format:
    black figwizz/ testing/

# Check code formatting
format-check:
    black --check figwizz/ testing/

# Sort imports with isort
sort-imports:
    isort figwizz/ testing/

# Run all linters
lint: format-check sort-imports
    @echo "Linting complete!"

# Fix all code quality issues
fix: format sort-imports
    @echo "Code formatting complete!"

# Documentation commands
# ======================

# Serve documentation locally
docs-serve:
    mkdocs serve

# Preview documentation with custom script (supports additional options)
docs-preview:
    python scripts/preview_docs.py

# Build documentation
docs-build:
    mkdocs build --clean

# Deploy documentation to GitHub Pages
docs-deploy:
    mkdocs gh-deploy --force

# Build commands
# ==============

# Clean build artifacts
clean:
    rm -rf build/
    rm -rf dist/
    rm -rf *.egg-info/
    rm -rf site/
    rm -rf .pytest_cache/
    rm -rf htmlcov/
    rm -rf .coverage
    find . -type d -name __pycache__ -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
    find . -type f -name "*.pyo" -delete

# Build distribution packages
build: clean
    python -m build

# Check distribution packages
check-dist: build
    twine check dist/*

# Development utilities
# =====================

# Check dependencies
check-deps:
    pip list --outdated

# Show package version
version:
    python -c "import figwizz; print(figwizz.__version__ if hasattr(figwizz, '__version__') else 'unknown')"

# Example workflows
# =================

# Example: Download stock images
example-download QUERY="mountains":
    @echo "Downloading stock images: {{QUERY}}"
    @mkdir -p examples/stock_images
    python -c "from figwizz import download_stock_images; \
               download_stock_images('{{QUERY}}', 5, 'examples/stock_images', provider='unsplash')"

# Example: Convert images to different format
example-convert FORMAT="jpg":
    @echo "Converting example images to {{FORMAT}}"
    @mkdir -p examples/converted
    python -c "from figwizz import convert_image; \
               from pathlib import Path; \
               [convert_image(str(p), '{{FORMAT}}') for p in Path('examples').glob('*.png')]"

# Example: Create hexicons
example-hexicon:
    @echo "Creating hexicon example"
    @mkdir -p examples/hexicons
    python -c "from figwizz import make_hexicon; \
               from PIL import Image; \
               img = Image.new('RGB', (200, 200), (100, 150, 200)); \
               hexicon = make_hexicon(img, border_size=10, border_color='auto'); \
               hexicon.save('examples/hexicons/example_hexicon.png')"

# Example: Scrape images from URL
example-scrape URL="https://example.com":
    @echo "Scraping images from {{URL}}"
    @mkdir -p examples/scraped
    python -c "from figwizz import extract_images_from_url; \
               extract_images_from_url('{{URL}}', 'examples/scraped')"

# Complete workflow: Generate and process
example-workflow:
    @echo "Running complete example workflow..."
    @mkdir -p examples/workflow
    python -c "from PIL import Image; \
               from figwizz import make_hexicon, convert_image; \
               import numpy as np; \
               # Generate test image; \
               arr = np.random.randint(50, 200, (300, 300, 3), dtype=np.uint8); \
               img = Image.fromarray(arr); \
               img.save('examples/workflow/generated.png'); \
               # Create hexicon; \
               hexicon = make_hexicon(img, border_size=15, border_color='auto'); \
               hexicon.save('examples/workflow/hexicon.png'); \
               # Convert to JPEG; \
               convert_image('examples/workflow/hexicon.png', 'jpg'); \
               print('Workflow complete!')"

# Full development setup
# ======================

# Set up complete development environment
setup: install-all
    @echo "Development environment ready!"
    @echo "Run 'just test' to run tests"
    @echo "Run 'just docs-serve' to view documentation"

# Run full validation (tests, linting, docs)
validate: lint test docs-build
    @echo "✓ All validation passed!"

# Prepare for release
release-check: clean validate build check-dist
    @echo "✓ Ready for release!"
    @echo "Run 'twine upload dist/*' to upload to PyPI"