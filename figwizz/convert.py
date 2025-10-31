import os
from PIL import Image

from .modify import make_image_opaque

__all__ = ['convert_image']

# Input / Image Conversion ----------------------------------------

def convert_image(source_path, target_format, **kwargs):
    """Convert an image file to another format.
    
    Args:
        source_path (str): Path to the source image file.
        target_format (str): Target format to convert to (e.g., 'jpg', 'png', 'pdf').
        **kwargs: Additional keyword arguments.
            remove_original (bool): Whether to remove the original file. Defaults to True.
            
    Returns:
        str: Path to the converted image file.
    """
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
    img.save(target_path, target_format.upper())
    
    if kwargs.pop('remove_original', True):
        os.remove(source_path)

    return target_path # return the new path