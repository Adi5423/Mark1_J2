import os
from pathlib import Path

def create_folder_in_directory():
    # Get the directory name from the user
    directory_name = input("Enter the directory name (e.g., Desktop, D:, C:): ")
    
    # Get the folder name to create
    folder_name = input("Enter the name of the new folder: ")
    
    # Resolve the full path of the directory
    if directory_name.lower() == "desktop":
        # Get the user's Desktop path
        directory_path = Path.home() / "Desktop"
    elif directory_name.endswith(":"):
        # Handle drive letters (e.g., D:, C:)
        directory_path = Path(directory_name)  # This will resolve to the root of the drive
    else:
        # Use Path to resolve other directories
        directory_path = Path(directory_name)

    # Check if the directory exists
    if not directory_path.is_dir():
        print(f"The directory '{directory_path}' does not exist. Please check the name and try again.")
        return
    
    # Combine the path and folder name to create the full path
    new_folder_path = directory_path / folder_name
    
    # Create the folder
    try:
        new_folder_path.mkdir(parents=True, exist_ok=True)  # parents=True allows creation of parent directories
        print(f"Folder '{new_folder_path}' created successfully.")
    except Exception as e:
        print(f"Error occurred: {e}")

# Run the function
create_folder_in_directory()