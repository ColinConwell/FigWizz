#!/usr/bin/env python3
"""
Script to extract images/figures from URLs or PDF files.
Supports both web pages and PDF documents.
"""

import argparse
import sys
from pathlib import Path

from figwizz import (
    is_url_a_pdf,
    download_pdf_from_url,
    extract_images_from_pdf,
    extract_images_from_url,
)

def main():
    parser = argparse.ArgumentParser(
        description="Extract images from URLs or PDF files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract from local PDF (saves as figure001.png, figure002.png, etc.)
  %(prog)s paper.pdf -o figures/
  
  # Extract from PDF URL
  %(prog)s https://arxiv.org/pdf/2301.12345.pdf -o figures/
  
  # Extract from web page
  %(prog)s https://example.com/article.html -o images/
  
  # Extract from web page and convert SVG to PNG (high quality)
  %(prog)s https://example.com/article.html -o images/ --convert-svg
  
  # Convert SVG with custom scale (5x for extra high quality)
  %(prog)s https://example.com/article.html -o images/ --convert-svg --svg-scale 5.0
  
  # With custom size filtering
  %(prog)s paper.pdf -o figures/ --min-width 200 --min-height 200
  
  # With custom naming prefix (saves as img001.jpg, img002.jpg, etc.)
  %(prog)s paper.pdf -o figures/ --name-prefix img
        """
    )
    
    parser.add_argument(
        'input',
        help='URL or path to PDF file'
    )
    
    parser.add_argument(
        '-o', '--output-dir',
        default='extracted_images',
        help='Output directory for extracted images (default: extracted_images)'
    )
    
    parser.add_argument(
        '--min-width',
        type=int,
        default=100,
        help='Minimum image width in pixels (default: 100)'
    )
    
    parser.add_argument(
        '--min-height',
        type=int,
        default=100,
        help='Minimum image height in pixels (default: 100)'
    )
    
    parser.add_argument(
        '--name-prefix',
        default='figure',
        help='Prefix for saved image filenames (default: figure)'
    )
    
    parser.add_argument(
        '--convert-svg',
        action='store_true',
        help='Convert SVG files to PNG (requires cairosvg: pip install cairosvg)'
    )
    
    parser.add_argument(
        '--svg-scale',
        type=float,
        default=3.0,
        help='Scale factor for SVG to PNG conversion (default: 3.0 for high quality)'
    )
    
    args = parser.parse_args()
    
    temp_pdf_path = None
    
    try:
        # Determine if input is a URL or file path
        if args.input.startswith('http://') or args.input.startswith('https://'):
            # Check if URL points to a PDF
            if is_url_a_pdf(args.input):
                print("Detected PDF URL")
                temp_pdf_path = download_pdf_from_url(args.input)
                saved_images = extract_images_from_pdf(
                    temp_pdf_path,
                    args.output_dir,
                    args.min_width,
                    args.min_height,
                    args.name_prefix
                )
            else:
                # It's a regular web page URL
                saved_images = extract_images_from_url(
                    args.input,
                    args.output_dir,
                    args.min_width,
                    args.min_height,
                    args.name_prefix,
                    args.convert_svg,
                    args.svg_scale
                )
        elif Path(args.input).exists() and args.input.lower().endswith('.pdf'):
            # It's a local PDF file
            saved_images = extract_images_from_pdf(
                args.input,
                args.output_dir,
                args.min_width,
                args.min_height,
                args.name_prefix
            )
        else:
            print(f"Error: Input must be a valid URL or an existing PDF file")
            print(f"Provided: {args.input}")
            sys.exit(1)
        
        print(f"\n{'='*50}")
        print(f"Extraction complete!")
        print(f"Images saved to: {Path(args.output_dir).absolute()}")
        print(f"Total images: {len(saved_images)}")
        print(f"{'='*50}")
        
    finally:
        # Clean up temporary PDF file if it was created
        if temp_pdf_path and Path(temp_pdf_path).exists():
            try:
                Path(temp_pdf_path).unlink()
                print(f"\nCleaned up temporary file: {temp_pdf_path}")
            except Exception as e:
                print(f"\nWarning: Could not delete temporary file {temp_pdf_path}: {e}")


if __name__ == '__main__':
    main()