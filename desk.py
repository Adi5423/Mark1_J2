import os

def get_desktop_path():
    # Get the home directory
    home_directory = os.path.expanduser("~")
    
    # Construct the path to the Desktop
    desktop_path = os.path.join(home_directory, "Desktop")
    
    return desktop_path

if __name__ == "__main__":
    desktop_location = get_desktop_path()
    print("Desktop Location:", desktop_location)
