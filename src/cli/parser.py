import argparse
from config import cli_config

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=cli_config.PROGRAM_NAME,
        description=cli_config.DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=cli_config.EPILOG,
    )
    parser.add_argument(
        "input",
        type=str,
        help="Image file path or folder path (use --batch for folders)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed analysis output",
    )
    parser.add_argument(
        "-b", "--batch",
        action="store_true",
        help="Analyze all images in the folder",
    )
    parser.add_argument(
        "-t", "--threshold",
        type=float,
        default=cli_config.DEFAULT_THRESHOLD,
        help="Detection threshold (default: 0.12, range: 0.0-1.0)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format",
    )
    return parser
