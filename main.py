from src.app_gui import launch_gui
from src.engine import generate_full_report, TEMPLATES

def main():
    launch_gui(generate_full_report, TEMPLATES)
    

if __name__ == "__main__":
    main()