#!/usr/bin/env python3
"""
Minecraft Resource Pack Converter - Main Entry Point
Usage: python3 main.py [pack_name]
atau: python3 main.py (untuk interactive mode)
"""

import sys
import argparse
from pathlib import Path

# Add converter to path
sys.path.insert(0, str(Path(__file__).parent))

from converter.ui.cli import ConverterCLI
from converter.core.resource_pack_converter import ResourcePackConverter
from converter.config import INPUT_DIR


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Minecraft Resource Pack Converter - Java to Bedrock with Geyser",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main.py                  # Interactive mode
  python3 main.py my_pack          # Convert specific pack
  python3 main.py my_pack.zip      # Convert zip file
  python3 main.py -v my_pack       # Verbose output
        """
    )
    
    parser.add_argument(
        'pack',
        nargs='?',
        help='Resource pack name or filename (optional, interactive mode if not provided)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--no-geyser',
        action='store_true',
        help='Skip Geyser mapping generation'
    )
    
    args = parser.parse_args()
    
    # Ensure directories exist
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    if args.pack:
        # Direct conversion mode
        print("=" * 70)
        print("MINECRAFT RESOURCE PACK CONVERTER")
        print("=" * 70)
        print()
        
        converter = ResourcePackConverter(args.pack, verbose=args.verbose)
        success = converter.convert()
        
        stats = converter.get_statistics()
        
        print("\n" + "=" * 70)
        print("CONVERSION COMPLETE" if success else "CONVERSION FAILED")
        print("=" * 70)
        print(f"Pack: {args.pack}")
        print(f"Status: {stats['status']}")
        print(f"Duration: {stats['duration']:.2f}s")
        print(f"Textures: {stats['total_textures']}")
        print(f"Sounds: {stats['total_sounds']}")
        print(f"Models: {stats['total_models']}")
        print(f"Fonts: {stats['total_fonts']}")
        
        if stats['errors']:
            print(f"\nErrors: {len(stats['errors'])}")
            for error in stats['errors']:
                print(f"  - {error}")
        
        print(f"\nOutput: {converter.bedrock_pack_path}")
        print("=" * 70)
        print()
        
        return 0 if success else 1
    
    else:
        # Interactive mode
        cli = ConverterCLI()
        cli.run()
        return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nOperation cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
