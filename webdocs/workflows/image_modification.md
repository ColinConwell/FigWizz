# Image Modification

Transform and modify images with FigWizz's modification tools.

## Making Images Opaque

Add a solid background to transparent images:

```python
from figwizz import make_image_opaque

# Add white background (default)
img = make_image_opaque('transparent.png')
img.save('opaque.png')

# Custom background color
img = make_image_opaque('transparent.png', bg_color=(255, 0, 0))  # Red
img.save('red_background.png')
```

This is useful when:
- Converting RGBA images to JPEG
- Preparing images for formats that don't support transparency
- Creating consistent backgrounds across multiple images

## N-gon Cropping

Crop images to polygon shapes (triangles, hexagons, octagons, etc.):

```python
from figwizz.modify import ngon_crop

# Hexagon (default)
hexagon = ngon_crop('image.png')

# Triangle
triangle = ngon_crop('image.png', sides=3)

# Pentagon
pentagon = ngon_crop('image.png', sides=5)

# Octagon
octagon = ngon_crop('image.png', sides=8)
```

### With Borders

Add borders to your n-gon crops:

```python
# Auto-detected contrasting border
img = ngon_crop('image.png', border_size=10, border_color='auto')

# Custom color border (hex)
img = ngon_crop('image.png', border_size=5, border_color='#FF5733')

# Custom color border (RGB)
img = ngon_crop('image.png', border_size=5, border_color=(255, 87, 51))

# Named color
img = ngon_crop('image.png', border_size=5, border_color='red')
```

### Position and Rotation

Adjust the crop position and rotation:

```python
# Shift position
img = ngon_crop('image.png', shift_x=10, shift_y=-5)

# Rotate
img = ngon_crop('image.png', rotation=30)  # degrees

# Combine
img = ngon_crop('image.png', shift_x=5, shift_y=-10, rotation=15)
```

### Padding

Add padding before cropping to prevent cutting into image content:

```python
img = ngon_crop('image.png', padding=20)
```

### Custom Size

Specify output dimensions:

```python
img = ngon_crop('image.png', crop_size=(300, 300))
```

## Complete Example

Create a professional hexicon with all options:

```python
from figwizz.modify import ngon_crop

hexicon = ngon_crop(
    'logo.png',
    sides=6,
    crop_size=(400, 400),
    shift_x=0,
    shift_y=-10,  # Shift up slightly
    rotation=0,
    border_size=12,
    border_color='auto',  # Contrasting color
    padding=30  # Space around content
)

hexicon.save('professional_hexicon.png')
```

## Batch Processing

Process multiple images:

```python
from pathlib import Path
from figwizz.modify import ngon_crop

input_dir = Path('logos')
output_dir = Path('hexicons')
output_dir.mkdir(exist_ok=True)

for img_path in input_dir.glob('*.png'):
    hexicon = ngon_crop(
        str(img_path),
        border_size=10,
        border_color='auto'
    )
    hexicon.save(output_dir / img_path.name)
```

## Color Processing

FigWizz provides color utilities for advanced customization:

```python
from figwizz.colors import parse_color, extract_dominant_color, get_contrasting_color

# Parse different color formats
rgb = parse_color('#FF5733')  # (255, 87, 51)
rgb = parse_color('red')      # (255, 0, 0)
rgb = parse_color((100, 150, 200))  # (100, 150, 200)

# Extract dominant color from image
from PIL import Image
img = Image.open('photo.png')
dominant = extract_dominant_color(img)

# Get contrasting color
contrasting = get_contrasting_color(dominant, prefer_dark=True)
```

## See Also

- [Icon Workflows](icons.md) - Hexicon-specific workflows
- [Image Conversion](image_conversion.md) - Format conversion
- [API Reference](../api/reference.md) - Complete API documentation

