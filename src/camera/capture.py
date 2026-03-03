"""
Camera Capture Module
======================
Handles camera opening, frame grabbing, and photo capture operations.
"""

import cv2
import os
import time
from dataclasses import dataclass
from src.config import camera_config


@dataclass
class CameraConfig:
    """Camera settings."""
    device_id: int = camera_config.DEFAULT_DEVICE_ID
    width: int = camera_config.DEFAULT_WIDTH
    height: int = camera_config.DEFAULT_HEIGHT
    fps: int = camera_config.DEFAULT_FPS
    save_dir: str = camera_config.DEFAULT_SAVE_DIR


class CameraCapture:
    """
    Handles camera opening, frame grabbing, and photo saving.
    Can be used as a context manager.
    """

    def __init__(self, config: CameraConfig | None = None):
        self.config = config or CameraConfig()
        self.cap: cv2.VideoCapture | None = None
        self._is_open = False

    def open(self) -> bool:
        """Open the camera. Returns True if successful."""
        self.cap = cv2.VideoCapture(self.config.device_id)
        if not self.cap.isOpened():
            print(f"[ERROR] Unable to open camera {self.config.device_id}!")
            return False

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.config.fps)

        self._is_open = True
        actual_w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"[CAMERA] Opened: device={self.config.device_id}, resolution={actual_w}x{actual_h}")
        return True

    def read_frame(self):
        """Grab a frame. Returns (success, frame)."""
        if self.cap is None or not self._is_open:
            return False, None
        return self.cap.read()

    def save_photo(self, frame, prefix: str = "capture") -> str | None:
        """
        Save the frame to a file.
        Returns the saved file path or None on failure.
        """
        os.makedirs(self.config.save_dir, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.jpg"
        filepath = os.path.join(self.config.save_dir, filename)

        if cv2.imwrite(filepath, frame):
            print(f"[SAVED] {filepath}")
            return filepath
        return None

    def release(self):
        """Release the camera."""
        if self.cap is not None:
            self.cap.release()
            self._is_open = False
            print("[CAMERA] Released")

    @property
    def is_open(self) -> bool:
        return self._is_open and self.cap is not None and self.cap.isOpened()

    # Context manager support
    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args):
        self.release()
