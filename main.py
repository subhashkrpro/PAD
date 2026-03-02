from src.cli.cli import main as cli_main
from src.camera.camera_cli import main as camera_main

def main():
    print("Welcome to the Photo Authenticity Detector CLI!")
    print("Choose an option:")
    print("1. Analyze a photo or folder of photos")
    print("2. Use live camera detection")
    choice = input("Enter 1 or 2: ").strip()
    if choice == "1":
        cli_main()
    elif choice == "2":
        camera_main()
    else:
        print("Invalid choice. Please run the program again and select either 1 or 2.")


if __name__ == "__main__":
    main()
