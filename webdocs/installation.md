# Installation

## Basic Installation

Install FigWizz using pip:

```bash
pip install figwizz
```

This installs the core package with basic dependencies.

## Optional Dependencies

FigWizz has several optional feature sets that can be installed as needed.

### AI Image Generation

To use AI-powered image generation:

```bash
pip install figwizz[genai]
```

This installs `litellm` for accessing various AI image generation APIs.

### Development Tools

For contributing to FigWizz:

```bash
pip install figwizz[dev]
```

This installs testing and code quality tools (pytest, black, isort).

### Documentation Building

To build documentation locally:

```bash
pip install figwizz[docs]
```

This installs mkdocs and related documentation tools.

### All Optional Dependencies

To install everything:

```bash
pip install figwizz[genai,dev,docs]
```

## Platform-Specific Features

Some features require platform-specific tools:

### PDF Extraction

For extracting images from PDFs, install PyMuPDF:

```bash
pip install PyMuPDF
```

### SVG Conversion

For converting SVG images to raster formats:

```bash
pip install cairosvg
```

### Presentation Conversion

Presentation slide conversion works differently on each platform:

**macOS**: Uses AppleScript (built-in)
- Requires Keynote for `.key` files
- Requires Microsoft PowerPoint for `.ppt/.pptx` files

**Windows**: Uses COM interface
```bash
pip install pywin32
```

**Linux**: Uses LibreOffice
```bash
# Ubuntu/Debian
sudo apt-get install libreoffice

# Fedora
sudo dnf install libreoffice
```

## Environment Setup

FigWizz can load API keys from environment files. Create a `.env` file in your project root:

```bash
# .env
PIXABAY_API_KEY=your_pixabay_key
UNSPLASH_ACCESS_KEY=your_unsplash_key
OPENAI_API_KEY=your_openai_key
```

Or set them as environment variables:

```bash
export PIXABAY_API_KEY="your_key"
export UNSPLASH_ACCESS_KEY="your_key"
export OPENAI_API_KEY="your_key"
```

## Verification

Verify your installation:

```python
import figwizz
print(figwizz.__version__)

# Check available functions
print(figwizz.__all__)
```

## Troubleshooting

### Import Errors

If you encounter import errors for optional dependencies:

```python
ImportError: No module named 'litellm'
```

Install the required optional dependency:
```bash
pip install figwizz[genai]
```

### Permission Errors

On macOS, if AppleScript fails:
1. Grant Terminal/IDE access to System Events in System Preferences
2. Grant access to Keynote/PowerPoint in System Preferences

### LibreOffice Not Found

On Linux, if presentation conversion fails:
```bash
which soffice
```

If not found, install LibreOffice as shown above.

