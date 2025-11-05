#!/usr/bin/env python
"""
Preview the MkDocs documentation locally.

This script launches a local development server to preview the documentation.
The server will automatically reload when you make changes to the docs.

Usage:
    python scripts/preview_docs.py
    
    # Or with custom port
    python scripts/preview_docs.py --port 8001
    
    # Or with custom address
    python scripts/preview_docs.py --address 0.0.0.0
"""

import sys
import subprocess
import argparse
from pathlib import Path


def check_mkdocs_installed():
    """Check if mkdocs is installed."""
    try:
        import mkdocs
        return True
    except ImportError:
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Preview FigWizz documentation locally",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to serve documentation on (default: 8000)"
    )
    parser.add_argument(
        "--address",
        type=str,
        default="127.0.0.1",
        help="Address to serve documentation on (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--no-livereload",
        action="store_true",
        help="Disable live reloading of documentation"
    )
    
    args = parser.parse_args()
    
    # Check if mkdocs is installed
    if not check_mkdocs_installed():
        print("Error: mkdocs is not installed.")
        print("\nInstall it with:")
        print("  pip install figwizz[docs]")
        print("or")
        print("  pip install mkdocs mkdocs-material mkdocstrings[python]")
        sys.exit(1)
    
    # Get project root (parent of scripts directory)
    project_root = Path(__file__).parent.parent
    
    # Check if mkdocs.yml exists
    mkdocs_config = project_root / "mkdocs.yml"
    if not mkdocs_config.exists():
        print(f"Error: mkdocs.yml not found at {mkdocs_config}")
        sys.exit(1)
    
    # Build command
    cmd = [
        "mkdocs",
        "serve",
        "--dev-addr", f"{args.address}:{args.port}",
    ]
    
    if args.no_livereload:
        cmd.append("--no-livereload")
    
    # Print startup message
    print("=" * 70)
    print("FigWizz Documentation Preview")
    print("=" * 70)
    print(f"\nStarting documentation server at: http://{args.address}:{args.port}")
    print(f"Configuration file: {mkdocs_config}")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 70)
    print()
    
    # Run mkdocs serve
    try:
        subprocess.run(cmd, cwd=project_root, check=True)
    except KeyboardInterrupt:
        print("\n\nShutting down documentation server...")
        print("Goodbye!")
    except subprocess.CalledProcessError as e:
        print(f"\nError running mkdocs: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("\nError: mkdocs command not found in PATH")
        print("Make sure mkdocs is properly installed")
        sys.exit(1)


if __name__ == "__main__":
    main()

