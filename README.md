# Brute-Force ZIP/RAR Archive Cracker

This Python project is a GUI (graphical user interface) application developed with PyQt5 that attempts to crack the password of ZIP and RAR archives protected by a password. The application uses a brute-force approach by testing each password from a wordlist file.

## Main Features:
- Simple and intuitive graphical interface built with PyQt5.
- Support for ZIP and RAR formats.
- Uses a wordlist (text file) to attempt to unlock archives.
- Progress tracking with a progress bar.
- Extracts files to a designated folder if the password is found.
- Redirects to YouTube, GitHub, and Linktree for additional resources.

## Requirements:
- Python 3.x
- PyQt5
- `zipfile` and `rarfile` (for handling ZIP and RAR archives, respectively).
- WinRAR must be installed on your machine for processing RAR archives.

## Installation:
1. Clone this repository or download the source file.
2. Install the required dependencies via pip:
   ```bash
   pip install pyqt5 rarfile tqdm
   ```
Ensure that the path to UnRAR.exe is properly configured on your machine (WinRAR must be installed).

## Usage:
Launch the application by running the Python script.
Select the ZIP or RAR file you want to unlock.
Choose a file containing a list of passwords (by default, a wordlist file is included).
Click "Start Attack" to begin the brute-force process.
If a password is found, the files will be extracted to a designated folder.
## Example Usage:
Use this program to recover forgotten or lost passwords for ZIP/RAR files.
Customize the wordlist to try specific passwords relevant to your situation.
## Code Explanation:
The application works by brute-forcing the password using a list of possible passwords from a wordlist. It uses the following components:

PyQt5 for the GUI (Graphical User Interface).
zipfile for opening and extracting files from ZIP archives.
rarfile for handling RAR archives.
Threading for non-blocking password cracking in the background.
tqdm for displaying progress during the cracking process.
## Application Flow:
File Selection: The user selects a ZIP or RAR file.
Wordlist Selection: The user selects a password wordlist (text file).
Crack Start: The application starts attempting each password from the wordlist on the selected archive.
Progress Tracking: The progress bar updates in real-time as passwords are tested.
Extraction: If a correct password is found, files from the archive are extracted to a folder.

## Notes:
This application is intended for personal use, such as recovering passwords for ZIP and RAR files that you own or have permission to access.
It may not work if the ZIP or RAR archive is damaged or uses a more advanced encryption method not supported by the brute-force method.
