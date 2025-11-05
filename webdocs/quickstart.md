# Quick Start

Get started with FigWizz in minutes! This guide covers the most common use cases.

## Image Format Conversion

Convert images between formats effortlessly:

```python
from figwizz import convert_image

# Convert PNG to JPEG
convert_image('input.png', 'jpg')

# Convert with original deletion
convert_image('input.png', 'pdf', delete_original=True)
```

FigWizz automatically handles transparency and color modes.

## Creating Hexicons

Create tidyverse-style hexagonal icons:

```python
from figwizz import make_hexicon

# Basic hexicon
hexicon = make_hexicon('logo.png')
hexicon.save('hexicon.png')

# With custom border
hexicon = make_hexicon('logo.png', 
                       border_size=10, 
                       border_color='auto',  # Auto-detects contrasting color
                       padding=20)
hexicon.save('hexicon_bordered.png')

# With position adjustment
hexicon = make_hexicon('logo.png',
                       shift_x=0,
                       shift_y=-10,  # Shift up
                       rotation=30)
```

## Working with Stock Images

Download images from Pixabay or Unsplash:

```python
from figwizz import download_stock_images
import os

# Set API key (or use .env file)
os.environ['UNSPLASH_ACCESS_KEY'] = 'your_key_here'

# Download from Unsplash
images = download_stock_images(
    query='mountains',
    n_images=5,
    output_dir='images',
    provider='unsplash'
)

# Download from Pixabay
os.environ['PIXABAY_API_KEY'] = 'your_key_here'
images = download_stock_images(
    query='nature',
    n_images=10,
    output_dir='nature_images',
    provider='pixabay'
)
```

## Converting Presentations

Convert PowerPoint or Keynote slides to images:

```python
from figwizz import slides_to_images

# Convert with auto-cropping
slides_to_images(
    input_path='presentation.pptx',
    output_path='figures/',
    filename_format='figure{:02d}.png',
    crop_images=True,
    margin_size='1cm',
    dpi=300
)
```

## Extracting Images from PDFs

Extract figures from academic papers and documents:

```python
from figwizz import extract_images_from_pdf

# Extract all large images
images = extract_images_from_pdf(
    pdf_path='paper.pdf',
    output_dir='extracted_figures',
    min_width=200,
    min_height=200,
    name_prefix='figure'
)

print(f"Extracted {len(images)} images")
```

## Scraping Images from Websites

Download images from web pages:

```python
from figwizz import extract_images_from_url

# Extract from URL
images = extract_images_from_url(
    url='https://example.com/article',
    output_dir='web_images',
    min_width=400,
    min_height=300,
    convert_svg=True  # Convert SVG to PNG
)
```

## Creating Image Grids

Display multiple images in a grid:

```python
from figwizz import make_image_grid
import matplotlib.pyplot as plt

images = ['img1.png', 'img2.png', 'img3.png', 'img4.png']
titles = ['Image A', 'Image B', 'Image C', 'Image D']

fig, axes = make_image_grid(
    images,
    titles=titles,
    max_cols=2,
    figsize=(10, 10),
    show_index=True
)

plt.savefig('grid.png', dpi=300, bbox_inches='tight')
plt.show()
```

## Flexible Image Input

FigWizz functions accept various input types:

```python
from figwizz import make_image_opaque
from PIL import Image
import numpy as np

# From file path
img = make_image_opaque('image.png')

# From PIL Image
pil_img = Image.open('image.png')
img = make_image_opaque(pil_img)

# From numpy array
arr = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
img = make_image_opaque(arr)

# From bytes
with open('image.png', 'rb') as f:
    img_bytes = f.read()
img = make_image_opaque(img_bytes)

# From URL
img = make_image_opaque('https://example.com/image.png')
```

## N-gon Cropping

Create custom polygon-shaped crops:

```python
from figwizz.modify import ngon_crop

# Triangle
triangle = ngon_crop('image.png', sides=3)

# Pentagon
pentagon = ngon_crop('image.png', sides=5)

# Octagon with border
octagon = ngon_crop('image.png', 
                    sides=8,
                    border_size=8,
                    border_color='#FF5733')
```

## Next Steps

- Explore detailed [workflow guides](workflows/image_conversion.md)
- Check the [API reference](api/convert.md) for all available options
- See [advanced examples](workflows/scraping.md) for complex use cases

