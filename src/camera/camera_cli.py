"""
Camera CLI Entry Point
=======================
Open the camera for live detection or photo capture and analysis.

Usage:
    uv run camera                    # Live detection (default camera)
    uv run camera --device 1         # Use a different camera
    uv run camera --auto             # Auto mode ON by default
    uv run camera --capture-only     # Capture a photo and analyze
"""

import argparse
import sys
from src.detector.main_detector import PhotoAuthenticityDetector
from .capture import CameraCapture, CameraConfig
from .live_detector import LiveDetector, LiveConfig
from src.config import camera_config


def create_parser() -> argparse.ArgumentParser:
    """Camera CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="camera",
        description=(
            "Live Camera Authenticity Detector - Real-time detection of "
            "real photos vs recaptured images using your camera."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Live Mode Controls:
  SPACE  - Capture & Analyze current frame
  A      - Toggle auto-detection mode
  S      - Save current frame to disk
  Q/ESC  - Quit

Examples:
  uv run camera                   # Default camera, live mode
  uv run camera --device 1        # Use camera index 1
  uv run camera --auto            # Start with auto-detect ON
  uv run camera --width 1920 --height 1080
  uv run camera --capture-only    # Just capture + analyze one photo
        """,
    )

    parser.add_argument(
        "-d", "--device",
        type=int, default=camera_config.DEFAULT_DEVICE_ID,
        help=f"Camera device index (default: {camera_config.DEFAULT_DEVICE_ID})",
    )

    parser.add_argument(
        "-W", "--width",
        type=int, default=camera_config.DEFAULT_WIDTH,
        help=f"Camera frame width (default: {camera_config.DEFAULT_WIDTH})",
    )

    parser.add_argument(
        "-H", "--height",
        type=int, default=camera_config.DEFAULT_HEIGHT,
        help=f"Camera frame height (default: {camera_config.DEFAULT_HEIGHT})",
    )

    parser.add_argument(
        "--auto",
        action="store_true",
        help="Start with auto-detection ON",
    )

    parser.add_argument(
        "--interval",
        type=float, default=camera_config.DEFAULT_AUTO_INTERVAL,
        help=f"Auto-detection interval in seconds (default: {camera_config.DEFAULT_AUTO_INTERVAL})",
    )

    parser.add_argument(
        "--capture-only",
        action="store_true",
        help="Capture one photo, analyze it, and exit",
    )

    parser.add_argument(
        "-t", "--threshold",
        type=float, default=0.12,
        help="Detection threshold (default: 0.12)",
    )

    parser.add_argument(
        "--save-dir",
        type=str, default="captures",
        help="Directory to save captured photos (default: captures)",
    )

    return parser


def run_live_mode(args):
    """Start live camera detection."""
    cam_config = CameraConfig(
        device_id=args.device,
        width=args.width,
        height=args.height,
        save_dir=args.save_dir,
    )

    live_config = LiveConfig(
        auto_interval=args.interval,
    )

    detector = PhotoAuthenticityDetector(threshold=args.threshold)
    live = LiveDetector(cam_config, live_config, detector)

    # --no-auto flag for manual mode
    if not args.auto:
        live._auto_mode = True  # Default is ON, flag only confirms

    live.run()


def run_capture_mode(args):
    """Capture a photo, analyze it, and exit."""
    import cv2

    cam_config = CameraConfig(
        device_id=args.device,
        width=args.width,
        height=args.height,
        save_dir=args.save_dir,
    )

    detector = PhotoAuthenticityDetector(threshold=args.threshold)

    print("=" * 50)
    print("  CAPTURE MODE")
    print("  Capturing a photo from the camera and analyzing...")
    print("=" * 50)

    with CameraCapture(cam_config) as camera:
        if not camera.is_open:
            print("\n" + "!" * 50)
            print(f"  [ERROR] FAILED TO OPEN CAMERA (Device: {args.device})")
            print("  Troubleshooting:")
            print("  1. Check if the camera is physically connected.")
            print("  2. Ensure no other application (Zoom, Teams, etc.) is using it.")
            print("  3. Try a different device index: --device 1, --device 2, etc.")
            print("!" * 50 + "\n")
            sys.exit(1)

        # Warm-up frames (allow camera to stabilize)
        print("  Camera warming up...")
        for _ in range(camera_config.WARMUP_FRAMES):
            camera.read_frame()
            cv2.waitKey(camera_config.WARMUP_WAIT_MS)

        # Capture frame
        ret, frame = camera.read_frame()
        if not ret or frame is None:
            print("[ERROR] Frame capture failed!")
            sys.exit(1)

        # Save photo
        path = camera.save_photo(frame, prefix="capture")
        if path:
            print(f"  Photo saved: {path}")
        
        # Analyze
        print("  Analyzing...")
        result = detector.detect_from_array(frame)
        print(result.summary())


def main():
    """Camera CLI main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if args.capture_only:
        run_capture_mode(args)
    else:
        run_live_mode(args)


if __name__ == "__main__":
    main()
