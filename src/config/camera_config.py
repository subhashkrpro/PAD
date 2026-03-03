"""
Camera Configuration
=====================
Defines default settings for camera devices and UI overlay.
"""

# Camera Defaults
DEFAULT_DEVICE_ID = 0
DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720
DEFAULT_FPS = 30
DEFAULT_SAVE_DIR = "captures"

# Capture / Warmup
WARMUP_FRAMES = 15
WARMUP_WAIT_MS = 50

# Live Detection Defaults
DEFAULT_AUTO_INTERVAL = 1.5
DEFAULT_WINDOW_NAME = "Photo Authenticity Detector - Live"
DEFAULT_DOWNSCALE = 0.5

# UI Colors (BGR format)
COLOR_GREEN = (0, 200, 0)       # REAL
COLOR_RED = (0, 0, 220)         # RECAPTURED
COLOR_YELLOW = (0, 220, 220)    # Analyzing / uncertain
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BG_DARK = (30, 30, 30)
COLOR_BG_PANEL = (40, 40, 40)

# UI Dimensions
BORDER_THICKNESS = 8
BANNER_HEIGHT = 100
BANNER_DIVIDER_Y = 96
SCORE_BAR_WIDTH = 180
SCORE_BAR_HEIGHT = 18
SCORE_PANEL_GAP = 30
