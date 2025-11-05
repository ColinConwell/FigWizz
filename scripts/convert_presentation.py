#!/usr/bin/env python3
"""
Enhanced presentation conversion with options
"""

import argparse
from figwizz import slides_to_images


def main():
    parser = argparse.ArgumentParser(
        description="Convert PowerPoint or Keynote presentations to images"
    )
    parser.add_argument('input', help='Path to presentation file')
    parser.add_argument('-o', '--output-dir', default='slides',
                       help='Output directory (default: slides)')
    parser.add_argument('-f', '--format', default='slide{:02d}.png',
                       help='Filename format (default: slide{:02d}.png)')
    parser.add_argument('--no-crop', action='store_true',
                       help='Disable automatic cropping')
    parser.add_argument('--margin', default='1cm',
                       help='Margin size (default: 1cm)')
    parser.add_argument('--dpi', type=int, default=300,
                       help='Output DPI (default: 300)')
    
    args = parser.parse_args()
    
    print(f"Converting {args.input} to images...")
    
    slides_to_images(
        input_path=args.input,
        output_path=args.output_dir,
        filename_format=args.format,
        crop_images=not args.no_crop,
        margin_size=args.margin,
        dpi=args.dpi
    )
    
    print(f"Slides saved to {args.output_dir}!")


if __name__ == '__main__':
    main()

