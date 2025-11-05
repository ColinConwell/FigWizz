# Presentations to Images

Convert PowerPoint and Keynote presentations to high-quality images.

## Basic Conversion

Convert slides to images with automatic cropping:

```python
from figwizz import slides_to_images

slides_to_images(
    input_path='presentation.pptx',
    output_path='figures/',
    crop_images=True
)
```

This works with:
- PowerPoint files (`.ppt`, `.pptx`)
- Keynote files (`.key`) on macOS

## Custom Filenames

Specify a naming pattern:

```python
slides_to_images(
    input_path='talk.key',
    output_path='slides/',
    filename_format='slide{:02d}.png'  # slide01.png, slide02.png, ...
)
```

## Cropping Options

Control whitespace cropping and margins:

```python
slides_to_images(
    input_path='presentation.pptx',
    output_path='figures/',
    crop_images=True,
    margin_size='0.5cm',  # Add 0.5cm margin after cropping
    dpi=300  # High quality output
)
```

## Without Cropping

Skip the automatic cropping:

```python
slides_to_images(
    input_path='deck.pptx',
    output_path='raw_slides/',
    crop_images=False
)
```

## Manual Cropping

Crop whitespace from existing images:

```python
from figwizz.stitchkit import crop_whitespace

# Single image
crop_whitespace(
    image_path='slide.png',
    output_path='cropped_slide.png',
    margin_size='1cm',
    dpi=300
)

# Directory of images
crop_whitespace(
    image_path='slides/',  # Directory
    margin_size='0.5cm'
)
```

## Converting to PDF

Convert slides to individual PDFs:

```python
from figwizz.stitchkit import convert_to_pdf

# Single image to PDF
convert_to_pdf('slide1.png', dpi=300)

# Directory of images to PDFs
convert_to_pdf('figures/', dpi=300)
```

## Platform Support

### macOS

Uses AppleScript (built-in):

```python
# PowerPoint
slides_to_images('presentation.pptx', 'output/')

# Keynote
slides_to_images('presentation.key', 'output/')
```

**Requirements:**
- Microsoft PowerPoint (for `.ppt`/`.pptx`)
- Keynote (for `.key`)

### Windows

Uses COM interface:

```bash
pip install pywin32
```

```python
slides_to_images('presentation.pptx', 'output/')
```

**Requirements:**
- Microsoft PowerPoint installed

### Linux

Uses LibreOffice command-line:

```bash
# Ubuntu/Debian
sudo apt-get install libreoffice

# Fedora
sudo dnf install libreoffice
```

```python
slides_to_images('presentation.pptx', 'output/')
```

## Complete Workflow

Full workflow from presentation to publication-ready figures:

```python
from figwizz import slides_to_images
from figwizz.stitchkit import convert_to_pdf

# 1. Convert slides to images
slides_to_images(
    input_path='conference_talk.pptx',
    output_path='figures/',
    filename_format='figure{:01d}.png',
    crop_images=True,
    margin_size='1cm',
    dpi=300
)

# 2. Convert to PDF for publication
convert_to_pdf('figures/', dpi=300)

print("Figures ready for publication!")
```

## Batch Processing

Process multiple presentations:

```python
from pathlib import Path
from figwizz import slides_to_images

presentations = Path('presentations')

for pptx in presentations.glob('*.pptx'):
    output_dir = Path('figures') / pptx.stem
    slides_to_images(
        str(pptx),
        str(output_dir),
        crop_images=True,
        margin_size='1cm'
    )
```

## Advanced: ImageMagick Conversion

For even more control, use ImageMagick:

```python
from figwizz.stitchkit import mogrify_images_to_pdf

# Requires ImageMagick installed
mogrify_images_to_pdf('figures/', pdf_only=True)
```

## Troubleshooting

### macOS Permission Issues

If AppleScript fails:
1. Open System Preferences → Security & Privacy → Privacy
2. Grant Terminal/IDE access to "System Events"
3. Grant access to PowerPoint/Keynote

### Windows COM Errors

If conversion fails:
1. Ensure PowerPoint is installed
2. Run Python as administrator
3. Check `pywin32` is installed: `pip install pywin32`

### Linux LibreOffice Not Found

If `soffice` command not found:
```bash
which soffice  # Check if installed
sudo apt-get install libreoffice  # Install if needed
```

## See Also

- [Installation](../installation.md) - Platform setup
- [Image Conversion](image_conversion.md) - Converting output images
- [API Reference](../api/reference.md) - Complete API documentation

