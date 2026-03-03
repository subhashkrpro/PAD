"""
CLI Entry Point - Photo Authenticity Detector
===============================================
Command line se image analyze karo:

Usage:
    uv run detect <image_path>
    uv run detect <image_path> --verbose
    uv run detect <folder_path> --batch
"""

import os
import sys

from src.detector.main_detector import PhotoAuthenticityDetector
from .parser import create_parser
from .analyze import analyze_single
from src.config import cli_config


def main():
    parser = create_parser()
    args = parser.parse_args()
    detector = PhotoAuthenticityDetector(threshold=args.threshold)
    for line in cli_config.HEADER_LINES:
        print(line)
    if args.batch:
        if not os.path.isdir(args.input):
            print(f"  ERROR: '{args.input}' is not a directory. Use --batch with a folder.")
            sys.exit(1)
        image_files = [
            os.path.join(args.input, f)
            for f in sorted(os.listdir(args.input))
            if os.path.splitext(f)[1].lower() in cli_config.IMAGE_EXTENSIONS
        ]
        if not image_files:
            print(f"  No image files found in '{args.input}'")
            sys.exit(1)
        print(f"\n  Found {len(image_files)} images in '{args.input}'")
        results = {"REAL": 0, "RECAPTURED": 0, "ERROR": 0}
        for img_path in image_files:
            success = analyze_single(detector, img_path, args.verbose, args.json)
            if not success:
                results["ERROR"] += 1
            print("-" * cli_config.SEPARATOR_LENGTH)
        print(cli_config.BATCH_SUMMARY_LINE.format(count=len(image_files)))
    else:
        if not os.path.isfile(args.input):
            print(f"  ERROR: '{args.input}' is not a file.")
            sys.exit(1)
        analyze_single(detector, args.input, args.verbose, args.json)
    print()


if __name__ == "__main__":
    main()
