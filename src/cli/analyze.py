import os
import time
from detector.main_detector import PhotoAuthenticityDetector

def analyze_single(detector: PhotoAuthenticityDetector, image_path: str, verbose: bool, as_json: bool) -> bool:
    # Print analysis start information
    print(f"\n  Analyzing: {os.path.basename(image_path)}")
    print(f"  Path: {image_path}")
    start_time = time.time()

    # Run detection and handle possible errors
    try:
        result = detector.detect(image_path)
    except FileNotFoundError:
        print(f"  ERROR: File not found - {image_path}")
        return False
    except ValueError as e:
        print(f"  ERROR: {e}")
        return False

    # Calculate elapsed time for analysis
    elapsed = time.time() - start_time

    # Output results in JSON format if requested
    if as_json:
        import json
        output = {
            "file": image_path,
            "verdict": result.verdict,
            "confidence": round(result.confidence, 4),
            "final_score": round(result.final_score, 4),
            "scores": {
                "fft": round(result.fft_result.score, 4),
                "moire": round(result.moire_result.score, 4),
                "laplacian": round(result.laplacian_result.score, 4),
                "texture": round(result.texture_result.score, 4),
            },
            "time_seconds": round(elapsed, 3),
        }
        print(json.dumps(output, indent=2))
    # Output detailed summary if verbose mode is enabled
    elif verbose:
        print(result.summary())
        print(f"\n  Analysis time: {elapsed:.2f}s")
    # Output concise result otherwise
    else:
        icon = "REAL ✓" if result.verdict == "REAL" else "RECAPTURED ✗"
        print(f"  Result: [{icon}] (confidence: {result.confidence:.1%}, score: {result.final_score:.3f})")
        print(f"  Time: {elapsed:.2f}s")
    return True
