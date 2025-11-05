#!/usr/bin/env python3
"""
Batch create hexicons from a directory of images
"""

import argparse
from figwizz.workflows.batch import batch_create_hexicons


def main():
    parser = argparse.ArgumentParser(
        description="Create hexicons for all images in a directory"
    )
    parser.add_argument('input_dir', help='Directory containing images')
    parser.add_argument('-o', '--output-dir', default='hexicons',
                       help='Output directory (default: hexicons)')
    parser.add_argument('--size', type=int, nargs=2, metavar=('WIDTH', 'HEIGHT'),
                       help='Hexicon size as width height')
    parser.add_argument('--border-size', type=int, default=10,
                       help='Border size in pixels (default: 10)')
    parser.add_argument('--border-color', type=str, default='auto',
                       help='Border color (default: auto)')
    parser.add_argument('--padding', type=int, default=20,
                       help='Padding in pixels (default: 20)')
    
    args = parser.parse_args()
    
    kwargs = {
        'border_size': args.border_size,
        'border_color': args.border_color,
        'padding': args.padding,
    }
    
    if args.size:
        kwargs['size'] = tuple(args.size)
    
    print(f"Creating hexicons from {args.input_dir}...")
    
    hexicons = batch_create_hexicons(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        **kwargs
    )
    
    print(f"Successfully created {len(hexicons)} hexicons in {args.output_dir}!")


if __name__ == '__main__':
    main()

