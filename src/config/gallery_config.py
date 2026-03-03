"""
Gallery Configuration
======================
Defines settings for the image gallery viewer.
"""

WINDOW_NAME = "Photo Gallery"
SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp')

# UI Dimensions
VIEWPORT_WIDTH = 1200
VIEWPORT_HEIGHT = 800

# Key Bindings (ASCII codes)
KEY_NEXT = ord('d')      # 'd' or Right Arrow
KEY_PREV = ord('a')      # 'a' or Left Arrow
KEY_DELETE = ord('x')    # 'x' to Delete
KEY_QUIT = ord('q')      # 'q' to Quit
KEY_ESC = 27             # ESC to Quit

# Right/Left arrow keys (OpenCV codes can vary, so we use standard letters too)
KEY_ARROW_RIGHT = 83     # Windows-specific sometimes
KEY_ARROW_LEFT = 81
