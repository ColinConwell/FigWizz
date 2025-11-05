# Scraping Images

Extract images from PDFs, websites, and download stock photos.

## Extracting from PDFs

Extract figures from academic papers and documents:

```python
from figwizz import extract_images_from_pdf

# Basic extraction
images = extract_images_from_pdf(
    pdf_path='paper.pdf',
    output_dir='extracted_figures'
)

print(f"Extracted {len(images)} images")
```

### Filter by Size

Filter out small icons and decorations:

```python
images = extract_images_from_pdf(
    pdf_path='paper.pdf',
    output_dir='figures',
    min_width=300,
    min_height=300
)
```

### Custom Naming

Use custom filename prefixes:

```python
images = extract_images_from_pdf(
    pdf_path='smith2023.pdf',
    output_dir='figures',
    name_prefix='smith2023_fig'
)
# Produces: smith2023_fig001.png, smith2023_fig002.png, ...
```

## Extracting from URLs

Download images from web pages:

```python
from figwizz import extract_images_from_url

# Extract from article
images = extract_images_from_url(
    url='https://example.com/article',
    output_dir='web_images'
)
```

### SVG Conversion

Convert SVG images to PNG automatically:

```python
images = extract_images_from_url(
    url='https://example.com/article',
    output_dir='images',
    convert_svg=True,
    svg_scale=3.0  # High quality
)
```

### Size Filtering

Only download images above a certain size:

```python
images = extract_images_from_url(
    url='https://example.com/gallery',
    output_dir='large_images',
    min_width=800,
    min_height=600
)
```

## Downloading from PDF URLs

FigWizz automatically detects and handles PDF URLs:

```python
from figwizz import extract_images_from_url

# Will automatically detect PDF and extract images
images = extract_images_from_url(
    url='https://arxiv.org/pdf/2301.12345.pdf',
    output_dir='arxiv_figures'
)
```

Or use the PDF-specific function:

```python
from figwizz import download_pdf_from_url, extract_images_from_pdf

# Download PDF
pdf_path = download_pdf_from_url('https://example.com/paper.pdf')

# Extract images
images = extract_images_from_pdf(pdf_path, 'figures')
```

## Stock Image Downloads

### Unsplash

Download high-quality stock photos from Unsplash:

```python
from figwizz import download_stock_images
import os

# Set API key
os.environ['UNSPLASH_ACCESS_KEY'] = 'your_key_here'

# Download images
images = download_stock_images(
    query='nature landscape',
    n_images=10,
    output_dir='stock_images',
    provider='unsplash'
)
```

### Pixabay

Download from Pixabay:

```python
import os
from figwizz import download_stock_images

# Set API key
os.environ['PIXABAY_API_KEY'] = 'your_key_here'

# Download images
images = download_stock_images(
    query='business meeting',
    n_images=20,
    output_dir='business_images',
    provider='pixabay'
)
```

### Metadata

Downloaded images include JSON metadata files:

```python
import json

# Load metadata for an image
with open('stock_images/image_1.json', 'r') as f:
    metadata = json.load(f)

print(metadata['User'])          # Photographer name
print(metadata['Image_URL'])     # Original URL
print(metadata['Alt_Description'])  # Description
print(metadata['Tags'])          # Tags
```

## Using Environment Files

Store API keys in a `.env` file:

```bash
# .env
UNSPLASH_ACCESS_KEY=your_unsplash_key
PIXABAY_API_KEY=your_pixabay_key
```

Load automatically:

```python
from figwizz.utils import load_env_variables
from figwizz import download_stock_images

# Load environment variables
load_env_variables()

# API keys are now available
images = download_stock_images(
    'mountains', 
    n_images=5, 
    output_dir='images',
    provider='unsplash'
)
```

## Command Line Usage

Use the included script for quick extraction:

```bash
# Extract from PDF
python scripts/download_figures.py paper.pdf -o figures/

# Extract from URL
python scripts/download_figures.py https://example.com/article -o images/

# With custom filtering
python scripts/download_figures.py paper.pdf -o figures/ \
    --min-width 400 --min-height 400 \
    --name-prefix experiment

# Convert SVG files
python scripts/download_figures.py https://example.com/page -o images/ \
    --convert-svg --svg-scale 5.0
```

## Batch Processing

Process multiple sources:

```python
from figwizz import extract_images_from_pdf
from pathlib import Path

pdf_dir = Path('papers')
output_base = Path('extracted')

for pdf_path in pdf_dir.glob('*.pdf'):
    output_dir = output_base / pdf_path.stem
    images = extract_images_from_pdf(
        str(pdf_path),
        str(output_dir),
        min_width=200,
        min_height=200
    )
    print(f"{pdf_path.name}: {len(images)} images")
```

## See Also

- [Installation](../installation.md) - Setting up API keys
- [API Reference](../api/reference.md) - Complete API documentation

