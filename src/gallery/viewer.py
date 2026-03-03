"""
Gallery Viewer Module
======================
UI for browsing and deleting captured images.
"""

import cv2
import numpy as np
from config import gallery_config, camera_config
from .manager import GalleryManager

class GalleryViewer:
    """Displays images and handles user interactions."""

    def __init__(self, manager: GalleryManager):
        self.manager = manager
        self.current_idx = 0
        self.window_name = gallery_config.WINDOW_NAME

    def run(self):
        """Main loop for the gallery viewer."""
        self.manager.refresh()
        if self.manager.get_count() == 0:
            print("[INFO] Gallery is empty.")
            return

        cv2.namedWindow(self.window_name)

        while True:
            self._display_current()
            
            key = cv2.waitKey(0) & 0xFF

            if key == gallery_config.KEY_QUIT or key == gallery_config.KEY_ESC:
                break
            elif key == gallery_config.KEY_NEXT or key == gallery_config.KEY_ARROW_RIGHT:
                self.current_idx = (self.current_idx + 1) % self.manager.get_count()
            elif key == gallery_config.KEY_PREV or key == gallery_config.KEY_ARROW_LEFT:
                self.current_idx = (self.current_idx - 1) % self.manager.get_count()
            elif key == gallery_config.KEY_DELETE:
                self._handle_delete()
                if self.manager.get_count() == 0:
                    print("[INFO] Gallery empty after deletion.")
                    break

        cv2.destroyWindow(self.window_name)

    def _display_current(self):
        """Shows the current image with overlapping info."""
        if self.manager.get_count() == 0:
            return

        filename = self.manager.images[self.current_idx]
        path = self.manager.get_full_path(filename)
        
        image = cv2.imread(path)
        if image is None:
            # Handle corrupted or missing file
            self._draw_error(f"Error loading: {filename}")
            return

        # Resize for viewport
        h, w = image.shape[:2]
        scale = min(gallery_config.VIEWPORT_WIDTH / w, gallery_config.VIEWPORT_HEIGHT / h)
        if scale < 1.0:
            image = cv2.resize(image, None, fx=scale, fy=scale)

        # Draw Overlay
        display_img = self._draw_overlay(image, filename)
        cv2.imshow(self.window_name, display_img)

    def _draw_overlay(self, image, filename):
        """Draws UI info on the image."""
        overlay = image.copy()
        h, w = overlay.shape[:2]
        
        # Bottom bar
        cv2.rectangle(overlay, (0, h - 60), (w, h), (40, 40, 40), -1)
        
        info_text = f"Image {self.current_idx + 1}/{self.manager.get_count()}: {filename}"
        cv2.putText(overlay, info_text, (20, h - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        help_text = "[A/D] Prev/Next  |  [X] Delete  |  [Q] Exit"
        cv2.putText(overlay, help_text, (20, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)
        
        return overlay

    def _draw_error(self, message):
        """Shows an error screen."""
        error_img = np.zeros((400, 600, 3), dtype=np.uint8)
        cv2.putText(error_img, message, (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow(self.window_name, error_img)

    def _handle_delete(self):
        """Deletes current image after refresh."""
        filename = self.manager.images[self.current_idx]
        if self.manager.delete_image(filename):
            print(f"[GALLERY] Deleted: {filename}")
            if self.manager.get_count() > 0:
                self.current_idx = self.current_idx % self.manager.get_count()
