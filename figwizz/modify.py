from copy import copy
from PIL import Image

__all__ = ['make_image_opaque']

def make_image_opaque(img_input, bg_color=(255, 255, 255)):
    """
    Make an image opaque by adding a white background.
    
    Args:
        img_input: Path to the image file or PIL Image object.
        bg_color: Background color (default: white).
    
    Returns:
        PIL Image object with a white background.
    """
    # if input is path, load it as image
    if isinstance(img_input, str):
        img = Image.open(img_input)
        
    else: # assume input is image
        img = copy(img_input)
    
    # Check if the image has an alpha channel
    if img.mode in ('RGBA', 'LA') or ('transparency' in img.info):
        # Create a new image with a white background
        background = Image.new(img.mode[:-1], img.size, bg_color)
        # Paste the image on the background (masking with itself)
        background.paste(img, img.split()[-1])
        image = background  # ... using the alpha channel as mask
    
    # Convert image to RGB 
    if img.mode != 'RGB':
        img = img.convert('RGB')
            
    return img # image updated with nontrasparent background