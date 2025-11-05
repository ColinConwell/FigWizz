#!/usr/bin/env python3
"""
Batch convert images to a different format
"""

import argparse
from pathlib import Path
from figwizz.workflows.batch import batch_convert_images


def main():
    parser = argparse.ArgumentParser(
        description="Batch convert images to a different format"
    )
    parser.add_argument('input_dir', help='Directory containing images')
    parser.add_argument('format', help='Target format (e.g., jpg, png, pdf)')
    parser.add_argument('-o', '--output-dir', help='Output directory (optional)')
    parser.add_argument('--delete-original', action='store_true',
                       help='Delete original files after conversion')
    
    args = parser.parse_args()
    
    print(f"Converting images in {args.input_dir} to {args.format}...")
    
    converted = batch_convert_images(
        input_dir=args.input_dir,
        target_format=args.format,
        output_dir=args.output_dir,
        delete_original=args.delete_original
    )
    
    print(f"Successfully converted {len(converted)} images!")


if __name__ == '__main__':
    main()

