# Figure Operations

The `figure_ops` module provides functionality for converting PowerPoint and Keynote presentations to images and PDFs, with options for cropping and reformatting.

## Main Functions

### slides_to_images

::: figwizz.convert.slides_to_images

This is the primary function that detects file type (.key, .ppt, .pptx) and applies the appropriate conversion method.

Example:

```python
from figwizz.convert import slides_to_images

# Convert a presentation to PNG images, cropping whitespace
slides_to_images('presentation.pptx', 'output_folder', 
                filename_format='figure{:02d}.png',
                crop_images=True,
                margin_size='0.5cm')
```

## Presentation Conversion

### keynote_to_images

::: figwizz.convert.keynote_to_images

Example:

```python
from figwizz.convert import keynote_to_images

# Convert a Keynote presentation to PNG images
keynote_to_images('presentation.key', 'output_folder')
```

### powerpoint_to_images

::: figwizz.convert.powerpoint_to_images

Example:

```python
from figwizz.convert import powerpoint_to_images

# Convert a PowerPoint presentation to PNG images
powerpoint_to_images('presentation.pptx', 'output_folder')
```

## Image Processing

### crop_whitespace

::: figwizz.modify.crop_whitespace
    
Example:

```python
from figwizz.modify import crop_whitespace

# Crop whitespace from all images in a folder
crop_whitespace('output_folder', margin_size='1cm')
```

## PDF Conversion

### convert_to_pdf

::: figwizz.convert.convert_to_pdf

Example:

```python
from figwizz.convert import convert_to_pdf

# Convert a PNG image to PDF
convert_to_pdf('image.png', dpi=300)
```

### convert_images_to_pdf

::: figwizz.convert.convert_images_to_pdf

Example:

```python
from figwizz.convert import convert_images_to_pdf

# Convert all PNG images in a folder to PDFs
convert_images_to_pdf('output_folder', dpi=300)
```

## Platform Support

The module provides platform-specific implementations:

* **macOS**: Uses AppleScript to interact with Keynote and PowerPoint alike
* **Windows**: Uses the COM interface (via pywin32) to control PowerPoint
* **Linux/Other**: Uses LibreOffice command-line tools with python-pptx as a fallback

