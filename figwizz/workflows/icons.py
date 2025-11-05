"""
Icon workflow + convenience functions
"""

import os
from PIL import Image

from ..convert import bytes_to_image
from ..modify import ngon_crop

__all__ = ['make_hexicon']

def make_hexicon(input_image, size=None, **kwargs):
    """
    Make a tidyverse-style Hexicon from an input image.
    
    Args:
        input_image: Path to the image file or PIL Image object.
        size: Size of the output image as (width, height). If None, uses a square 
              based on the smallest dimension of the input image.
        **kwargs: Additional keyword arguments for ngon_crop.
            shift_x: Horizontal shift in pixels (default: 0). Positive values shift right.
            shift_y: Vertical shift in pixels (default: 0). Positive values shift down.
            rotation: Rotation angle in degrees (default: 0).
            border_size: Width of the border in pixels (default: 0, no border).
            border_color: Border color. Can be:
                - "auto": Automatically select contrasting color from image
                - Hex code: e.g., "#FF5733"
                - RGB tuple: e.g., (255, 87, 51)
                - Color name: e.g., "red", "blue"
    Returns:
        PIL Image object with the hexicon applied.
        
    Examples:
        >>> # Make a hexicon with no border
        >>> img = make_hexicon("input.png")
        
        >>> # Make a hexicon with red border and padding
        >>> img = make_hexicon("input.png", border_size=3, border_color="red", padding=20)
        
        >>> # Make hexicon with slight upwards shift
        >>> img = make_hexicon("input.png", shift_y=10)
    """
    # check if image is path, then bytes;
    # always convert to PIL Image object
    if isinstance(input_image, str):
        if os.path.exists(input_image):
            image = Image.open(input_image)
            
    if isinstance(input_image, bytes):
        image = bytes_to_image(input_image)
        
    if isinstance(input_image, Image.Image):
        image = input_image
        
    if not isinstance(image, Image.Image):
        raise ValueError(f"Invalid image input: {type(input_image)}. ",
                          "Input must be a valid path, bytes, or PIL Image object.")
    
    return ngon_crop(image, sides=6, crop_size=size, **kwargs)