"""
Live Detector Module
=====================
Perform real-time detection on camera feed.
- Run analysis every N frames (for performance)
- Display results on overlay
- Manual capture and analyze with Space key
- Continuous detection in auto mode
"""

import cv2
import time
import threading
from dataclasses import dataclass

from src.detector.result import DetectionResult
from src.detector.main_detector import PhotoAuthenticityDetector

from .capture import CameraCapture, CameraConfig
from .ui import OverlayUI


@dataclass
class LiveConfig:
    """Live detection settings."""
    auto_interval: float = 0.8    # Interval (seconds) between analyses in auto mode
    window_name: str = "Photo Authenticity Detector - Live"
    downscale: float = 0.5        # Frame resize factor for analysis


class LiveDetector:
    """
    Real-time authenticity detection on live camera feed.

    Controls:
        SPACE  - Capture frame and analyze
        A      - Toggle auto-detection mode
        S      - Save current frame
        Q/ESC  - Quit
    """

    def __init__(
        self,
        camera_config: CameraConfig | None = None,
        live_config: LiveConfig | None = None,
        detector: PhotoAuthenticityDetector | None = None,
    ):
        self.cam_config = camera_config or CameraConfig()
        self.live_config = live_config or LiveConfig()
        self.detector = detector or PhotoAuthenticityDetector()
        self.camera = CameraCapture(self.cam_config)
        self.ui = OverlayUI()

        # State
        self._last_result: DetectionResult | None = None
        self._auto_mode = True
        self._last_auto_time = 0.0
        self._analyzing = False
        self._fps = 0.0
        self._status_msg = ""
        self._status_color = (255, 255, 255)

    def run(self):
        """Main loop - open camera and start live detection."""
        if not self.camera.open():
            print("[ERROR] Unable to open camera. Please check if the camera is connected.")
            return

        print("\n" + "=" * 50)
        print("  LIVE DETECTION MODE")
        print("  SPACE = Capture & Analyze")
        print("  A     = Toggle Auto-detect")
        print("  S     = Save frame")
        print("  Q/ESC = Quit")
        print("=" * 50 + "\n")

        prev_time = time.time()
        frame_count = 0
        first_analyze_done = False

        try:
            while True:
                ret, frame = self.camera.read_frame()
                if not ret or frame is None:
                    print("[ERROR] Frame read failed!")
                    break

                # Analyze the first frame immediately
                if not first_analyze_done and frame_count > 5:
                    self._run_analysis_threaded(frame.copy())
                    first_analyze_done = True

                # Calculate FPS
                frame_count += 1
                now = time.time()
                if now - prev_time >= 1.0:
                    self._fps = frame_count / (now - prev_time)
                    frame_count = 0
                    prev_time = now

                # Auto mode: periodic analysis
                if self._auto_mode and not self._analyzing:
                    if now - self._last_auto_time >= self.live_config.auto_interval:
                        self._run_analysis_threaded(frame.copy())
                        self._last_auto_time = now

                # Draw UI overlay
                display = frame.copy()
                self._draw_overlay(display)

                cv2.imshow(self.live_config.window_name, display)

                # Keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:  # Q or ESC
                    break
                elif key == ord(' '):  # SPACE - manual capture and analyze
                    self._run_analysis_threaded(frame.copy())
                    self._set_status("Analyzing captured frame...", (0, 220, 220))
                elif key == ord('a'):  # A - toggle auto
                    self._auto_mode = not self._auto_mode
                    mode_text = "ON" if self._auto_mode else "OFF"
                    self._set_status(f"Auto-detect: {mode_text}", (0, 220, 220))
                    print(f"[AUTO] Auto-detection: {mode_text}")
                elif key == ord('s'):  # S - save frame
                    path = self.camera.save_photo(frame)
                    if path:
                        self._set_status(f"Saved: {path}", (0, 200, 0))

        except KeyboardInterrupt:
            print("\n[STOPPED] Keyboard interrupt")
        finally:
            self.camera.release()
            cv2.destroyAllWindows()

    def _run_analysis_threaded(self, frame):
        """Run analysis in a background thread to prevent UI freezing."""
        if self._analyzing:
            return

        def _worker():
            self._analyzing = True
            try:
                # Downscale for speed
                scale = self.live_config.downscale
                if scale < 1.0:
                    small = cv2.resize(frame, None, fx=scale, fy=scale)
                else:
                    small = frame

                result = self.detector.detect_from_array(small)
                self._last_result = result

                icon = "REAL" if result.verdict == "REAL" else "RECAPTURED"
                color = (0, 200, 0) if result.verdict == "REAL" else (0, 0, 220)
                self._set_status(f"Result: {icon} ({result.confidence:.0%})", color)
            except Exception as e:
                self._set_status(f"Error: {e}", (0, 0, 255))
            finally:
                self._analyzing = False

        thread = threading.Thread(target=_worker, daemon=True)
        thread.start()

    def _draw_overlay(self, frame):
        """Draw all UI elements on the frame."""
        if self._last_result is not None:
            # Always show last result, even while analyzing
            r = self._last_result
            self.ui.draw_border(frame, r.verdict)
            self.ui.draw_verdict(frame, r.verdict, r.confidence, r.final_score)
            self.ui.draw_score_bars(frame, {
                "FFT": r.fft_result.score,
                "Moire": r.moire_result.score,
                "Laplacian": r.laplacian_result.score,
                "Texture": r.texture_result.score,
            })
            if self._analyzing:
                self.ui.draw_small_indicator(frame, "Analyzing...")
        elif self._analyzing:
            self.ui.draw_analyzing(frame)
        else:
            # No result yet
            h, w = frame.shape[:2]
            cv2.rectangle(frame, (0, 0), (w, 70), (30, 30, 30), -1)
            cv2.putText(
                frame, "Starting detection...",
                (15, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 220, 220), 2,
            )

        # Auto mode indicator
        if self._auto_mode:
            self.ui.draw_status(frame, "[AUTO MODE - Live Detecting]", (0, 220, 220))
        else:
            self.ui.draw_status(frame, "[MANUAL - Press SPACE to analyze]", (180, 180, 180))

        self.ui.draw_fps(frame, self._fps)
        self.ui.draw_help(frame)

    def _set_status(self, msg: str, color=(255, 255, 255)):
        self._status_msg = msg
        self._status_color = color
