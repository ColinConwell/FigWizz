__name__ = "figwizz"

from . import modify
from . import convert
from . import stitch
from . import scrape
from . import webkit

from .modify import (
    make_image_opaque,
)

from .convert import (
    convert_image,
)

from .stitch import (
    slides_to_images,
    convert_to_pdf,
    convert_images_to_pdf,
    mogrify_images_to_pdf,
)

from .scrape import (
    download_pdf_from_url,
    extract_images_from_pdf,
    extract_images_from_url,
)

__all__ = [
    # submodules
    "modify",
    "convert",
    "stitch",
    "scrape",
    "webkit",
    
    # image modification
    "make_image_opaque",
    
    # image conversion
    "convert_image",
    
    # image stitching
    "slides_to_images",
    "convert_to_pdf",
    "convert_images_to_pdf",
    "mogrify_images_to_pdf",
    
    # scrape images from the web
    "download_pdf_from_url",
    "extract_images_from_pdf",
    "extract_images_from_url",
]