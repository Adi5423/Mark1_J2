import subprocess

def get_drive_names():
    try:
        # Run the command and capture the output
        result = subprocess.run(['wmic', 'logicaldisk', 'get', 'name'], capture_output=True, text=True, check=True)
        
        # Split the output into lines and filter out empty lines
        drive_names = [line.strip() for line in result.stdout.splitlines() if line.strip()]

        # Remove the header if present
        if drive_names and drive_names[0] == "Name":
            drive_names.pop(0)

        return drive_names

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    drives = get_drive_names()
    print("Drive Names:", drives)