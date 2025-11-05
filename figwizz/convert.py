import os, base64
from PIL import Image
from io import BytesIO

from .modify import make_image_opaque

__all__ = [
    'convert_image', 
    'bytes_to_image',
    'svg_to_image',
    'process_images']

# Input / Image Conversion ----------------------------------------

def convert_image(source_path, target_format, delete_original=False):
    """Convert an image file to another format.
    
    Args:
        source_path (str): Path to the source image file.
        target_format (str): Target format to convert to (e.g., 'jpg', 'png', 'pdf').
        **kwargs: Additional keyword arguments.
            remove_original (bool): Whether to remove the original file. Defaults to True.
            
    Returns:
        str: Path to the converted image file.
    """
    source_ext = source_path.split('.')[-1]
    if source_ext not in ['png', 'jpg', 'jpeg', 'pdf', 'svg']:
        raise ValueError(f"Invalid source path: {source_path}. ",
                         "Source path must end with .png, .jpg, .jpeg, .pdf, or .svg.")
    
    
    # Ensure the target format does not start with a dot
    if target_format.startswith('.'):
        target_format = target_format[1:]
    
    # Load the image with PIL:
    img = Image.open(source_path)
    
    if target_format in ['jpg', 'pdf']:
        img = make_image_opaque(img)
    
    # Define the new filename
    base = os.path.splitext(source_path)[0]
    target_path = f"{base}.{target_format.lower()}"
    
    # Convert and save the image
    if source_ext == 'svg':
        svg_to_image(img, target_path)
    else: # assume raster image
        img.save(target_path, target_format.upper())
    
    if delete_original:
        os.remove(source_path)

    return target_path # return the new path

def bytes_to_image(bytes_input):
    """Convert bytes to a PIL Image object.
    
    Args:
        bytes_input: Bytes input to convert to an image.
    
    Returns:
        PIL Image object.
    """
    # check bytes type (e.g. base64, bytes, etc.)
    if isinstance(bytes_input, str):
        bytes_input = base64.b64decode(bytes_input)
    elif isinstance(bytes_input, bytes):
        pass
    else: # raise error for invalid bytes input
        raise ValueError(f"Invalid bytes input: {type(bytes_input)}")
    
    # convert bytes to image
    return Image.open(BytesIO(bytes_input))

def svg_to_image(svg_content, output_path,
                 width=None, height=None, scale=None):
    """
    Convert SVG content to a raster image.
    
    Args:
        svg_content: Raw SVG file content (bytes)
        output_path: Path to save the output file
           (output type inferred from output_path)
        width: Optional width for output PNG (in pixels)
        height: Optional height for output PNG (in pixels)
        scale: Optional scale factor (e.g., 2.0 for 2x resolution)
    
    Returns:
        True if successful, False otherwise
    """
    
    if output_path.split('.')[-1] not in ['png', 'jpg', 'jpeg', 'pdf']:
        raise ValueError(f"Invalid output path: {output_path}. ",
                         "Output path must end with .png, .jpg, .jpeg, or .pdf.")
        
    output_ext = output_path.split('.')[-1]
    
    try:
        import cairosvg  # type: ignore
    except ImportError:
        print("  Warning: cairosvg not installed, cannot convert SVG to PNG")
        print("  Install with: pip install cairosvg")
        return False
    
    try:
        print('  Converting SVG to {output_ext.upper()}...')
        cairosvg.svg2png(
            bytestring=svg_content,
            write_to=str(output_path),
            output_width=width,
            output_height=height,
            scale=scale
        )
        return True
    except Exception as e:
        print(f"  Error converting SVG to {output_ext.upper()}: {e}")
        return False

# Batch Processing ------------------------------------------------

def _process_image_path(image_path):
    """Process an image path to a PIL Image object.
    
    Args:
        image_path: Path to the image file.
    """
    return Image.open(image_path)

def _process_image_bytes(image_bytes):
    """Process image bytes to a PIL Image object.
    
    Args:
        image_bytes: Bytes of the image.
    """
    return bytes_to_image(image_bytes)

def _process_image_pil(image):
    """Process a PIL Image object.
    
    Args:
        image: PIL Image object.
    """
    return image

def _process_image_list(images):
    """Process a list of images to a list of PIL Image objects.
    
    Args:
        images: List of images.
    """
    return [_process_image_pil(image) for image in images]

def process_images(images, target_format, **kwargs):
    """Process an image to a target format.
    
    Args:
        image: PIL image object, path, bytes, or list thereof.
        target_format: Target format to convert to (e.g., 'jpg', 'png', 'pdf').
        **kwargs: Additional keyword arguments.
    """
    # TODO: Implement this function. Default output format should be a PIL Image object.
    # Check if images is a list or single image
    raise NotImplementedError("process_images is not implemented yet.")