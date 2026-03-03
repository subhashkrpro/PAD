"""
UI Overlay Module
==================
Draw results on camera feed - boxes, text, bars, colors.
"""

import cv2
import numpy as np
from src.config import camera_config


class OverlayUI:
    """Draw detection results on camera frame."""

    @staticmethod
    def draw_border(frame, verdict: str):
        """Draw a colored border around the entire frame for instant visual feedback."""
        h, w = frame.shape[:2]
        is_real = verdict == "REAL"
        color = camera_config.COLOR_GREEN if is_real else camera_config.COLOR_RED
        thickness = camera_config.BORDER_THICKNESS
        cv2.rectangle(frame, (0, 0), (w - 1, h - 1), color, thickness)

    @staticmethod
    def draw_verdict(frame, verdict: str, confidence: float, score: float):
        """Draw a large verdict banner at the top of the frame."""
        h, w = frame.shape[:2]

        is_real = verdict == "REAL"
        color = camera_config.COLOR_GREEN if is_real else camera_config.COLOR_RED

        # Descriptive text - clear explanation
        if is_real:
            main_text = "REAL PHOTO"
            sub_text = "This is a genuine photo"
        else:
            main_text = "PHOTO OF SCREEN/IMAGE"
            sub_text = "This is a photo of a screen or poster"

        # Top banner background - bigger
        cv2.rectangle(frame, (0, 0), (w, camera_config.BANNER_HEIGHT), camera_config.COLOR_BG_DARK, -1)
        cv2.rectangle(frame, (0, camera_config.BANNER_DIVIDER_Y), (w, camera_config.BANNER_HEIGHT), color, -1)

        # Main verdict text - BADA
        cv2.putText(
            frame, main_text,
            (20, 42), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3,
        )

        # Sub text - English explanation
        cv2.putText(
            frame, sub_text,
            (20, 78), cv2.FONT_HERSHEY_SIMPLEX, 0.7, camera_config.COLOR_WHITE, 2,
        )

        # Confidence - right side
        conf_text = f"Confidence: {confidence:.0%}"
        cv2.putText(
            frame, conf_text,
            (w - 300, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, camera_config.COLOR_WHITE, 2,
        )

        # Score
        score_text = f"Score: {score:.3f}"
        cv2.putText(
            frame, score_text,
            (w - 300, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2,
        )

    @staticmethod
    def draw_small_indicator(frame, text: str):
        """Draw a small analyzing indicator without hiding the verdict."""
        h, w = frame.shape[:2]
        cv2.putText(
            frame, text,
            (w - 160, h - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, camera_config.COLOR_YELLOW, 1,
        )

    @staticmethod
    def draw_score_bars(frame, scores: dict[str, float], y_start: int = 110):
        """Draw horizontal bars for individual analyzer scores."""
        h, w = frame.shape[:2]
        bar_w = camera_config.SCORE_BAR_WIDTH
        bar_h = camera_config.SCORE_BAR_HEIGHT
        x_start = w - bar_w - 20
        label_x = x_start - 110
        gap = camera_config.SCORE_PANEL_GAP

        # Panel background
        panel_x = label_x - 10
        panel_h = len(scores) * gap + 15
        cv2.rectangle(
            frame,
            (panel_x, y_start - 5),
            (w - 5, y_start + panel_h),
            camera_config.COLOR_BG_PANEL, -1,
        )
        cv2.rectangle(
            frame,
            (panel_x, y_start - 5),
            (w - 5, y_start + panel_h),
            (60, 60, 60), 1,
        )

        for i, (name, val) in enumerate(scores.items()):
            y = y_start + i * gap + 15

            # Label
            cv2.putText(
                frame, name,
                (label_x, y + 3), cv2.FONT_HERSHEY_SIMPLEX, 0.45, camera_config.COLOR_WHITE, 1,
            )

            # Bar background
            cv2.rectangle(frame, (x_start, y - 8), (x_start + bar_w, y - 8 + bar_h), (60, 60, 60), -1)

            # Bar fill
            fill_w = int(bar_w * min(val, 1.0))
            bar_color = OverlayUI._score_color(val)
            cv2.rectangle(frame, (x_start, y - 8), (x_start + fill_w, y - 8 + bar_h), bar_color, -1)

            # Value text
            cv2.putText(
                frame, f"{val:.2f}",
                (x_start + bar_w + 5, y + 3), cv2.FONT_HERSHEY_SIMPLEX, 0.4, camera_config.COLOR_WHITE, 1,
            )

    @staticmethod
    def draw_help(frame):
        """Show keyboard shortcuts at the bottom of the frame."""
        h, w = frame.shape[:2]
        cv2.rectangle(frame, (0, h - 35), (w, h), camera_config.COLOR_BG_DARK, -1)
        help_text = "[SPACE] Capture & Analyze  |  [A] Toggle Auto  |  [Q] Quit"
        cv2.putText(
            frame, help_text,
            (15, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1,
        )

    @staticmethod
    def draw_fps(frame, fps: float):
        """Draw FPS counter."""
        cv2.putText(
            frame, f"FPS: {fps:.0f}",
            (15, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.5, camera_config.COLOR_YELLOW, 1,
        )

    @staticmethod
    def draw_analyzing(frame):
        """Show 'Analyzing...' indicator."""
        h, w = frame.shape[:2]
        cv2.rectangle(frame, (0, 0), (w, 70), camera_config.COLOR_BG_DARK, -1)
        cv2.putText(
            frame, "ANALYZING...",
            (15, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.2, camera_config.COLOR_YELLOW, 2,
        )

    @staticmethod
    def draw_status(frame, text: str, color=None):
        """Draw status text at the bottom-left of the frame."""
        if color is None:
            color = camera_config.COLOR_WHITE
        h, w = frame.shape[:2]
        cv2.putText(
            frame, text,
            (15, h - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 1,
        )

    @staticmethod
    def _score_color(val: float):
        """Return color based on score (green->yellow->red)."""
        if val < 0.3:
            return camera_config.COLOR_GREEN
        elif val < 0.6:
            return camera_config.COLOR_YELLOW
        else:
            return camera_config.COLOR_RED
