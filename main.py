import sys
import os

# Add src to sys.path to ensure local imports work consistently
sys.path.append(os.path.join(os.getcwd(), 'src'))

from cli.cli import main as cli_main
from camera.camera_cli import main as camera_main
from gallery.manager import GalleryManager
from gallery.viewer import GalleryViewer
from config import camera_config

def is_gui_available():
    """Check if a GUI/Display is available for camera/gallery."""
    # Common check for Linux/Unix and Windows
    if os.name == 'posix' and not os.environ.get('DISPLAY'):
        return False
    # On Windows, we usually have a GUI, but we can check for a 'TERM' environment
    # or just let it try and catch the specific OpenCV error.
    return True

def run_smart_analysis(path=None):
    """Determine if path is a file or folder and run appropriate analysis."""
    if path is None:
        path = input("Enter path (image or folder): ").strip()
    
    path = path.strip().strip('"').strip("'")
    if not path or not os.path.exists(path):
        if path: print(f"\n[ERROR] Path does not exist: {path}")
        return

    # Mutate global sys.argv for sub-modules
    sys.argv[:] = [sys.argv[0], path]
    if os.path.isdir(path):
        print(f"\n[SMART] Folder detected. Starting BATCH analysis: {path}")
        sys.argv.append("--batch")
    else:
        print(f"\n[SMART] File detected. Starting SINGLE analysis: {path}")
    
    try:
        cli_main()
    except Exception as e:
        print(f"\n[ERROR] Analysis failed: {e}")

def run_camera(args=None):
    """Helper to run camera commands with specific flags."""
    sys.argv[:] = [sys.argv[0]]
    if args: sys.argv.extend(args)
    camera_main()

def run_manual():
    """Execute advanced manual commands."""
    mode = input("Mode (1: Detect, 2: Camera): ").strip()
    args_str = input("Arguments: ").strip()
    sys.argv[:] = [sys.argv[0]]
    if args_str: sys.argv.extend(args_str.split())
    
    if mode == "1": cli_main()
    elif mode == "2": camera_main()
    else: print("Invalid mode.")

def entry():
    # Dispatch table: {key: (label, function)}
    def gui_wrap(func):
        """Wrapper to prevent running GUI functions when no display is found."""
        def wrapper(*args, **kwargs):
            if not is_gui_available():
                print("\n" + "!" * 40)
                print("[ERROR] GUI/Display not detected.")
                print("Camera and Gallery features require a screen.")
                print("Please run these on your host machine, not in Docker.")
                print("!" * 40)
                return
            return func(*args, **kwargs)
        return wrapper

    actions = {
        "1": ("Analyze RECENT captures", lambda: run_smart_analysis(camera_config.DEFAULT_SAVE_DIR)),
        "2": ("Analyze a SINGLE image", run_smart_analysis),
        "3": ("Analyze a CUSTOM folder", run_smart_analysis),
        "4": ("Live camera detection", gui_wrap(lambda: run_camera())),
        "5": ("Camera auto-detection mode", gui_wrap(lambda: run_camera(["--auto"]))),
        "6": ("Quick photo capture & analyze", gui_wrap(lambda: run_camera(["--capture-only"]))),
        "7": ("Browse Gallery (view/delete)", gui_wrap(lambda: GalleryViewer(GalleryManager()).run())),
        "8": ("Manual command (advanced)", run_manual)
    }

    while True:
        try:
            print(f"\n{'='*40}\n  PHOTO AUTHENTICITY DETECTOR\n{'='*40}")
            for k, (label, _) in actions.items():
                if k in ["4", "8"]: print("-" * 40)
                print(f"{k}. {label}")
            print("q. Quit")
            
            choice = input("\nSelection [1-8, q]: ").strip().lower()
            if choice == 'q':
                print("Goodbye!"); break
            
            if choice in actions:
                actions[choice][1]()
            else:
                print("Invalid option.")
        except KeyboardInterrupt:
            print("\nExiting..."); break
        except Exception as e:
            print(f"\n[UNEXPECTED ERROR] {e}")

if __name__ == "__main__":
    entry()