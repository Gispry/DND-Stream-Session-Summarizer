import os
import subprocess
from tkinter import Tk, messagebox
from multiprocessing import Process
import creds

def check_file_permissions():
    test_file = "test_permission_file.tmp"
    try:
        # Try to create a temporary file
        with open(test_file, 'w') as file:
            file.write("Test")
        
        # Try to delete the temporary file
        os.remove(test_file)
    except PermissionError:
        # If a permission error occurs, show a warning
        root = Tk()
        root.withdraw()  # Hide the main window
        messagebox.showwarning("Permission Issue",
                               "The program does not have permission to create or delete files. Please create a shortcut of this .bat file and run it as Administrator.")
        root.destroy()
        exit(1)  # Exit the program after showing the warning

# Function to check for existing audio files and ask the user about deletion
def check_and_handle_audio_files():
    audio_files = [f"audio{i}.wav" for i in range(1, 7)]
    existing_files = [file for file in audio_files if os.path.exists(file)]

    if existing_files:
        root = Tk()
        root.withdraw()  # Hide the main window
        user_choice = messagebox.askyesno("Audio Files Found",
                                           "Audio files exist from a previous session. Do you want to delete them?")
        root.destroy()

        if user_choice:
            for file in existing_files:
                os.remove(file)
                print(f"Deleted {file}")
        else:
            print("Using existing audio files.")

# New function to check and potentially clear the history.txt content
def check_and_handle_history_file():
    history_file = "history.txt"
    if os.path.exists(history_file) and os.path.getsize(history_file) > 0:
        root = Tk()
        root.withdraw()  # Hide the main window
        user_choice = messagebox.askyesno("History Content Found",
                                           "The history.txt file contains content. Do you want to clear history for this new session?")
        root.destroy()

        if user_choice:
            with open(history_file, 'w') as file:
                file.truncate(0)  # Clear the content of history.txt
            print("Cleared history.txt for the new session.")
        else:
            print("Keeping existing history.")

def run_script(script_name):
    try:
        subprocess.run(["python", script_name])
    except KeyboardInterrupt:
        print(f"Interrupted {script_name}")

if __name__ == "__main__":
    # Conditional checks based on the settings in creds.py
    if creds.CHECK_PERMISSIONS.upper() == 'YES':
        check_file_permissions()  # Only check if the program has permissions if enabled in creds.py
    
    if creds.CHECK_AUDIO_FILES.upper() == 'YES':
        check_and_handle_audio_files()  # Only check for and handle existing audio files if enabled in creds.py
    
    if creds.CHECK_HISTORY.upper() == 'YES':
        check_and_handle_history_file()  # Only check and potentially clear the history.txt content if enabled in creds.py

    # Define scripts to run
    scripts = ["Chatbot.py", "recorder.py", "Summeriser.py"]

    # Create a process for each script
    processes = [Process(target=run_script, args=(script,)) for script in scripts]

    # Start all processes
    for process in processes:
        process.start()

    try:
        # Wait for all processes to finish
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        print("Main script interrupted. Attempting to terminate all subprocesses...")
        for process in processes:
            process.terminate()
        print("All subprocesses terminated.")
