# FigWizz

Python toolkit for programmatic figure design.

## Overview

FigWizz is a comprehensive Python toolkit that simplifies working with images, figures, and scientific visualizations. Whether you're preparing figures for publications, creating image workflows, or automating visual content generation, FigWizz provides intuitive tools to get the job done.

## Key Features

- **Format Conversion**: Seamlessly convert images between formats (PNG, JPEG, PDF, SVG)
- **Presentation Processing**: Convert PowerPoint/Keynote slides to images with auto-cropping
- **Image Scraping**: Extract figures from PDFs and websites
- **Stock Images**: Download images from Pixabay and Unsplash
- **AI Generation**: Generate images from text prompts using AI models
- **Image Modification**: Create hexicons, n-gon crops, and apply transformations
- **Flexible Input**: Work with paths, PIL Images, bytes, numpy arrays, URLs, and more

## Quick Start

### Installation

```bash
pip install figwizz
```

For AI image generation support:
```bash
pip install figwizz[genai]
```

For development:
```bash
pip install figwizz[dev]
```

### Basic Usage

Convert an image:
```python
from figwizz import convert_image
convert_image('input.png', 'jpg')
```

Create a hexicon:
```python
from figwizz import make_hexicon
hexicon = make_hexicon('logo.png', border_size=10, border_color='auto')
hexicon.save('hexicon.png')
```

Download stock images:
```python
from figwizz import download_stock_images
images = download_stock_images('mountains', n_images=5, 
                                output_dir='images', 
                                provider='unsplash')
```

Convert slides to images:
```python
from figwizz import slides_to_images
slides_to_images('presentation.pptx', 'figures/', crop_images=True)
```

## Documentation Structure

- [Installation Guide](installation.md) - Detailed installation instructions
- [Quick Start](quickstart.md) - Get started quickly with common workflows
- **Workflows** - Organized by use case:
  - [Image Conversion](workflows/image_conversion.md)
  - [Image Modification](workflows/image_modification.md)
  - [Scraping](workflows/scraping.md)
  - [Presentations](workflows/presentations.md)
  - [Icons & Hexicons](workflows/icons.md)
  - [AI Generation](workflows/genai.md)
- **API Reference** - Complete module documentation

## Requirements

- Python >= 3.7
- PIL/Pillow
- matplotlib
- requests
- beautifulsoup4

Optional dependencies:
- PyMuPDF (for PDF extraction)
- cairosvg (for SVG conversion)
- litellm (for AI image generation)
- numpy (for numpy array support)

## License

GPL-3.0-only
