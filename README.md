# Xbox360FTP

Description This script is designed for the Xbox 360 homebrew development community. It automates the process of syncing files between your PC and Xbox 360 via FTP. The script supports auto-detection of the Xbox FTP server, automatic setup of FTP on your PC, file uploads and downloads, and even a self-updating feature for the script itself.

# Features
Auto-detect Xbox FTP server on the local network
Upload files to the Xbox 360
Download files from the Xbox 360
Automatically installs and configures the FTP server on Windows or Linux/macOS
Configures the firewall to allow FTP traffic
Provides a graphical interface for selecting files
Progress bar for file transfers
Self-updating script from GitHub repository

# Requirements
Python 3.x
requests library (install with pip)
Windows, Linux, or macOS

# Installation
Clone the repository or download the script.
Install the required dependencies: pip install -r requirements.txt
If you're using a Windows machine, make sure you have PowerShell access to install the FTP server.
For Linux/macOS, ensure that you have sudo privileges to install the FTP server.

# Usage
To run the script, open a terminal or command prompt and execute the following:
Install and configure the FTP server: python script.py --install-server
Sync Xbox files (downloads and uploads files to/from Xbox): python script.py --sync
Check for script updates and auto-update: python script.py --update

# Notes
The script automatically detects the local IP address of your PC.
The script attempts to connect to the Xbox FTP server on the default IP range (192.168.1.x). Ensure your Xbox and PC are on the same network.
The script provides a graphical file picker for file selection.
If an update to the script is available, it will be downloaded and applied automatically.
Contributing If you'd like to contribute to this project, feel free to fork the repository and create a pull request with your changes. Ensure that your contributions are well-tested and documented.

License This project is open-source. Feel free to use and modify it as needed for your own Xbox 360 development needs.

Made by Taylor Christian Newsom
