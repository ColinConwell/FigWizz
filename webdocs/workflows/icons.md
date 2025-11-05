# Icons and Hexicons

Create tidyverse-style hexagonal icons and other polygon-shaped graphics.

## Basic Hexicon

Create a simple hexagonal icon:

```python
from figwizz import make_hexicon

# Create hexicon from image
hexicon = make_hexicon('logo.png')
hexicon.save('hexicon.png')
```

## With Borders

Add professional borders:

```python
# Auto-detected contrasting border
hexicon = make_hexicon(
    'logo.png',
    border_size=10,
    border_color='auto'  # Automatically chooses contrasting color
)

# Custom border color
hexicon = make_hexicon(
    'logo.png',
    border_size=12,
    border_color='#2C3E50'  # Dark blue-gray
)

# Named color
hexicon = make_hexicon(
    'logo.png',
    border_size=8,
    border_color='navy'
)
```

## Positioning

Adjust the content position within the hexicon:

```python
# Center shift
hexicon = make_hexicon(
    'logo.png',
    shift_x=0,
    shift_y=-10  # Shift up 10 pixels
)

# Off-center
hexicon = make_hexicon(
    'logo.png',
    shift_x=15,
    shift_y=-5
)
```

## Rotation

Rotate the hexagon:

```python
# Flat top (default rotation=0)
hexicon = make_hexicon('logo.png', rotation=0)

# Pointy top
hexicon = make_hexicon('logo.png', rotation=30)

# Custom angle
hexicon = make_hexicon('logo.png', rotation=45)
```

## Padding

Add padding to prevent cropping into content:

```python
hexicon = make_hexicon(
    'logo.png',
    padding=30,  # Add 30px padding
    border_size=10,
    border_color='auto'
)
```

## Custom Size

Specify output dimensions:

```python
# Standard size
hexicon = make_hexicon('logo.png', size=(400, 400))

# Large hexicon
hexicon = make_hexicon('logo.png', size=(800, 800))
```

## Complete Professional Hexicon

All options combined:

```python
from figwizz import make_hexicon

hexicon = make_hexicon(
    input_image='package_logo.png',
    size=(500, 500),
    shift_x=0,
    shift_y=-15,  # Slightly up
    rotation=0,   # Flat top
    border_size=15,
    border_color='auto',
    padding=40
)

hexicon.save('professional_hexicon.png')
```

## Other Polygon Shapes

Create other polygon-shaped icons:

```python
from figwizz.modify import ngon_crop

# Triangle icon
triangle = ngon_crop(
    'logo.png',
    sides=3,
    border_size=8,
    border_color='#E74C3C'
)

# Pentagon badge
pentagon = ngon_crop(
    'logo.png',
    sides=5,
    border_size=10,
    border_color='#3498DB'
)

# Octagon stop sign style
octagon = ngon_crop(
    'logo.png',
    sides=8,
    border_size=12,
    border_color='#C0392B'
)
```

## Batch Creation

Create hexicons for multiple logos:

```python
from pathlib import Path
from figwizz import make_hexicon

input_dir = Path('logos')
output_dir = Path('hexicons')
output_dir.mkdir(exist_ok=True)

for logo in input_dir.glob('*.png'):
    hexicon = make_hexicon(
        str(logo),
        size=(500, 500),
        border_size=12,
        border_color='auto',
        padding=30
    )
    hexicon.save(output_dir / logo.name)
    print(f"Created hexicon: {logo.name}")
```

## Flexible Input

Hexicons accept various input types:

```python
from figwizz import make_hexicon
from PIL import Image
import numpy as np

# From file path
hexicon = make_hexicon('logo.png')

# From PIL Image
img = Image.open('logo.png')
hexicon = make_hexicon(img)

# From numpy array
arr = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
hexicon = make_hexicon(arr)

# From URL
hexicon = make_hexicon('https://example.com/logo.png')

# From bytes
with open('logo.png', 'rb') as f:
    logo_bytes = f.read()
hexicon = make_hexicon(logo_bytes)
```

## Color Schemes

Create hexicons with themed borders:

```python
from figwizz import make_hexicon

# Tidyverse blue
hexicon = make_hexicon('logo.png', border_color='#1A162D', border_size=12)

# R red
hexicon = make_hexicon('logo.png', border_color='#276DC2', border_size=12)

# Python yellow
hexicon = make_hexicon('logo.png', border_color='#FFD43B', border_size=12)

# GitHub dark
hexicon = make_hexicon('logo.png', border_color='#24292E', border_size=12)
```

## Tips for Best Results

1. **High Resolution**: Use high-resolution source images (at least 1000x1000px)
2. **Square Images**: Square images work best for hexicons
3. **Padding**: Add padding if your logo extends to the edges
4. **Contrast**: Use `border_color='auto'` for optimal visibility
5. **Positioning**: Adjust `shift_y` to center vertically if needed

## Example: Package Hexicon

Create a hexicon for a Python package:

```python
from figwizz import make_hexicon

# Assuming you have a square logo
hexicon = make_hexicon(
    'mypackage_logo.png',
    size=(500, 577),  # Standard hexicon dimensions
    border_size=15,
    border_color='#1A162D',  # Tidyverse blue
    padding=40,
    shift_y=-10  # Slight upward adjustment
)

hexicon.save('mypackage_hexicon.png')

# Also create a larger version
hexicon_large = make_hexicon(
    'mypackage_logo.png',
    size=(1000, 1154),
    border_size=30,
    border_color='#1A162D',
    padding=80,
    shift_y=-20
)

hexicon_large.save('mypackage_hexicon_large.png')
```

## See Also

- [Image Modification](image_modification.md) - N-gon cropping details
- [API Reference](../api/reference.md) - Complete API documentation

