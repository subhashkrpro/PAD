"""
Gallery Manager Module
=======================
Handles scanning and file operations for the gallery.
"""

import os
from config import gallery_config, camera_config

class GalleryManager:
    """Manages image files for the gallery."""

    def __init__(self, directory: str | None = None):
        self.directory = directory or camera_config.DEFAULT_SAVE_DIR
        self.images: list[str] = []
        self.refresh()

    def refresh(self):
        """Scans the directory for supported images."""
        if not os.path.exists(self.directory):
            self.images = []
            return

        self.images = [
            f for f in os.listdir(self.directory)
            if f.lower().endswith(gallery_config.SUPPORTED_EXTENSIONS)
        ]
        # Sort by newest first (assuming timestamp in filename)
        self.images.sort(reverse=True)

    def get_full_path(self, filename: str) -> str:
        """Returns the absolute path for a filename."""
        return os.path.join(self.directory, filename)

    def delete_image(self, filename: str) -> bool:
        """Deletes an image file from disk."""
        path = self.get_full_path(filename)
        try:
            if os.path.exists(path):
                os.remove(path)
                self.refresh()
                return True
        except Exception as e:
            print(f"[ERROR] Failed to delete {filename}: {e}")
        return False

    def get_count(self) -> int:
        """Returns the number of images in the gallery."""
        return len(self.images)
