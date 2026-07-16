from src.app_gui import launch_gui
from src.engine import generate_full_report

def main():
    launch_gui(generate_full_report)
    

if __name__ == "__main__":
    main()