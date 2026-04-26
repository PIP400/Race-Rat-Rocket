# Race-Rat-Rocket
A Hidden Screen Recorder Watcher With no Audio, Only Video &amp; Auto Save By Keystroke

# How to Download & Run
1. Download: Download the project as a ZIP file from the GitHub repository.
2. Heavy: download the file here --> https://drive.google.com/file/d/1jFqKnqQP_2lv3MG7BGhmydLj_bOKYB2X/view?usp=sharing
2. Locate: The donwloaded application exe.
3. Run: Double-click the executable to start the application.
4. Troubleshooting: If you encounter errors such as "STDN missing" or other startup issues, please follow the VS Code setup instructions below.

# Running via VS Code (Development Mode)
If the executable fails to run, you can launch the application directly using Python:
1. Setup: Open VS Code and ensure the Python extension is installed.
2. Import: Open the uncompressed "Race Rat Rocket" folder in VS Code.
3. Terminal: Open a new terminal window within VS Code.
# Environment: Create a virtual environment by typing:
python -m venv venv
# Activation: Activate the virtual environment:
venv\Scripts\Activate
# Dependencies: Install the required libraries:
pip install opencv-python numpy mss keyboard
# Updates: Ensure your package manager is up to date:
python.exe -m pip install --upgrade pip
# Launch: Start the application by typing:
python rat.py
# Operating How to Use Race Rat Rocket
1. shortcut.png the keystroke to remember.
2.Preparation: * Ensure you have the required libraries 
- If you have a file named icon.ico in the folder, the program will use it as the window icon.
3. Initialization: Run the script. Click the "ALLOW & SCAN" button.
- It will ask for Administrator permissions. Accept this so it can create the viewlog folder in your Program Files.
- if viewlog not found, create a folder name viewlog and copy/paste it inside programm files in C: drive.
4. Start Recording:
Click "START RECORDING". The status bar at the bottom will turn green.
The program is now capturing your screen at 15 FPS.
5. Stealth Mode:
Press Ctrl + Tab. The program window will vanish. It is still recording in the background.
6. Managing Clips:
Whenever something important happens on screen, press Alt + Tab.
The "Notification" counter (red box in the bottom right) will go up, signaling that a video segment has been successfully saved to C:\Program Files\viewlog.
7. Viewing Files:
To see your recordings, navigate to C:\Program Files\viewlog. The files are named with the format RAT_[Timestamp].avi.
8. Closing:
Press Ctrl + Tab + E to show the window again, then click "STOP RECORDING" before closing the app to ensure the final video file is saved correctly.
