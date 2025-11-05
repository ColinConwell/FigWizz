# Image Conversion

Convert images between different formats with automatic handling of transparency and color modes.

## Basic Conversion

Convert any image to a different format:

```python
from figwizz import convert_image

# Convert PNG to JPEG
convert_image('input.png', 'jpg')

# Convert to PDF
convert_image('input.png', 'pdf')

# Convert SVG to PNG
convert_image('logo.svg', 'png')
```

## Automatic Transparency Handling

FigWizz automatically makes images opaque when converting to formats that don't support transparency:

```python
# RGBA PNG → JPEG (automatically adds white background)
convert_image('transparent.png', 'jpg')

# RGBA PNG → PDF (automatically adds white background)
convert_image('transparent.png', 'pdf')
```

## Delete Original

Optionally remove the original file after conversion:

```python
convert_image('input.png', 'jpg', delete_original=True)
```

## Working with Bytes

Convert image data without saving to disk:

```python
from figwizz.convert import bytes_to_image

# Load bytes
with open('image.png', 'rb') as f:
    img_bytes = f.read()

# Convert to PIL Image
img = bytes_to_image(img_bytes)

# Or from base64
import base64
b64_string = base64.b64encode(img_bytes).decode()
img = bytes_to_image(b64_string)
```

## SVG Conversion

Convert SVG files to raster formats (requires cairosvg):

```python
from figwizz.convert import svg_to_image

# Read SVG content
with open('logo.svg', 'rb') as f:
    svg_content = f.read()

# Convert to PNG with custom size
svg_to_image(svg_content, 'output.png', width=512, height=512)

# Convert with scale factor
svg_to_image(svg_content, 'output.png', scale=3.0)
```

## Batch Conversion

Convert multiple images:

```python
from pathlib import Path
from figwizz import convert_image

input_dir = Path('inputs')
output_format = 'jpg'

for img_path in input_dir.glob('*.png'):
    convert_image(str(img_path), output_format)
```

## Flexible Input Types

Convert images from various sources:

```python
from figwizz import convert_image
from PIL import Image
import numpy as np

# From path
convert_image('image.png', 'jpg')

# From PIL Image
img = Image.open('image.png')
convert_image(img, 'jpg')

# From numpy array
arr = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
convert_image(arr, 'jpg')

# From URL
convert_image('https://example.com/image.png', 'jpg')
```

## Saving with Options

Use the unified save function for more control:

```python
from figwizz.utils.images import save_image
from PIL import Image

img = Image.open('input.png')

# Save with custom quality
save_image(img, 'output.jpg', quality=95)

# Save with custom format
save_image(img, 'output.webp', format='WEBP')

# Control transparency handling
save_image(img, 'output.jpg', make_opaque=True)
```

## Format Support

Supported formats:
- **Raster**: PNG, JPEG, TIFF, BMP, WebP
- **Vector**: SVG (input only, requires cairosvg)
- **Document**: PDF

## See Also

- [Image Modification](image_modification.md) - Transform and edit images
- [API Reference](../api/reference.md) - Complete API documentation

