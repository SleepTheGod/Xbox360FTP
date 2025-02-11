import os
import socket
import sys
import argparse
import hashlib
import requests
import subprocess
from ftplib import FTP
import tkinter as tk
from tkinter import filedialog, ttk

BANNER = """
██████   ██████   ██████      ███████ ████████ ██████  
     ██ ██       ██  ████     ██         ██    ██   ██ 
 █████  ███████  ██ ██ ██     █████      ██    ██████  
     ██ ██    ██ ████  ██     ██         ██    ██      
██████   ██████   ██████      ██         ██    ██      
       Made By Taylor Christian Newsome
"""

# FTP settings for Xbox 360 homebrew
XBOX_CREDENTIALS = {
    "ip": "192.168.1.100",  # Replace with your Xbox 360 IP
    "port": 21,
    "user": "xbox",
    "pass": "xbox"
}

def show_help():
    help_text = """
    Usage: python3 script.py [OPTIONS]

    Options:
      -h, --help          Show this help message and exit
      --install-server    Install and configure the FTP server
      --sync              Auto-detect Xbox, setup FTP, and sync files
      --update            Check for script updates and auto-update

    Example:
      python3 script.py --sync   # Auto-sync Xbox files
    """
    print(help_text)
    sys.exit()

# Auto-detect Local IP
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

# Detect Xbox FTP Server
def detect_xbox():
    for i in range(1, 255):
        ip = f"192.168.1.{i}"
        try:
            ftp = FTP()
            ftp.connect(ip, 21, timeout=2)
            ftp.login("xbox", "xbox")
            return ip
        except:
            continue
    return None

# Install FTP Server (Windows/Linux/macOS)
def install_ftp_server():
    if os.name == "nt":
        subprocess.run(["powershell", "Enable-WindowsOptionalFeature -Online -FeatureName IIS-FTPServer"], shell=True)
        subprocess.run(["powershell", "Start-Service ftpsvc"], shell=True)
    elif os.name == "posix":
        os.system("sudo apt-get install -y vsftpd && sudo systemctl enable vsftpd --now")
    print("✅ FTP Server installed and running.")

# Configure Firewall to Allow FTP
def configure_firewall():
    if os.name == "nt":
        subprocess.run(["powershell", "New-NetFirewallRule -DisplayName 'Allow FTP' -Direction Inbound -Protocol TCP -LocalPort 21 -Action Allow"], shell=True)
    elif os.name == "posix":
        os.system("sudo ufw allow 21/tcp")
    print("✅ Firewall configured for FTP.")

# File Integrity Hashing
def get_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()

# Automated File Selection
def select_files():
    pc_folder = os.path.expanduser("~/XboxBackup")
    selected_files = []
    for root, _, files in os.walk(pc_folder):
        for file in files:
            selected_files.append(os.path.join(root, file))
    return selected_files

# Progress Bar GUI
class ProgressWindow:
    def __init__(self, max_value):
        self.root = tk.Tk()
        self.root.title("File Transfer Progress")
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=20)
        self.progress["maximum"] = max_value
        self.root.update()

    def update_progress(self, value):
        self.progress["value"] = value
        self.root.update()

    def close(self):
        self.root.destroy()

# Download from Xbox
def download_from_xbox(ftp_xbox, selected_files):
    pc_folder = os.path.expanduser("~/XboxBackup")
    os.makedirs(pc_folder, exist_ok=True)
    progress = ProgressWindow(len(selected_files))

    for i, file in enumerate(selected_files):
        local_path = os.path.join(pc_folder, os.path.basename(file))
        with open(local_path, "wb") as f:
            ftp_xbox.retrbinary(f"RETR {file}", f.write)
        progress.update_progress(i + 1)

    progress.close()

# Upload to Xbox
def upload_to_xbox(ftp_xbox, selected_files):
    xbox_folder = "/HDD/Games/"
    progress = ProgressWindow(len(selected_files))

    for i, file in enumerate(selected_files):
        remote_path = xbox_folder + os.path.basename(file)
        if get_file_hash(file) == get_file_hash(remote_path):
            print(f"Skipping {file}, file already exists and is identical.")
            continue

        with open(file, "rb") as f:
            ftp_xbox.storbinary(f"STOR {remote_path}", f)
        progress.update_progress(i + 1)

    progress.close()

# Self-Updating Function
def check_for_updates():
    try:
        repo_url = "https://raw.githubusercontent.com/SleepTheGod/Xbox360FTP/main.py"
        response = requests.get(repo_url)
        with open(sys.argv[0], "r") as current_file:
            if response.text.strip() != current_file.read().strip():
                with open(sys.argv[0], "w") as updated_file:
                    updated_file.write(response.text)
                print("✅ Script updated. Restart the script.")
                sys.exit()
    except Exception as e:
        print(f"⚠️ Update check failed: {e}")

# Main Execution
if __name__ == "__main__":
    print(BANNER)
    parser = argparse.ArgumentParser()
    parser.add_argument("--install-server", action="store_true", help="Install and configure FTP server.")
    parser.add_argument("--sync", action="store_true", help="Auto-sync Xbox files.")
    parser.add_argument("--update", action="store_true", help="Check for updates and auto-update.")
    args = parser.parse_args()
    
    if args.install_server:
        install_ftp_server()
        configure_firewall()
        sys.exit()
    
    if args.update:
        check_for_updates()
        sys.exit()
    
    xbox_ip = detect_xbox()
    if not xbox_ip:
        print("❌ Xbox FTP not found on the network.")
        sys.exit()
    
    xbox = {"ip": xbox_ip, "port": 21, "user": "xbox", "pass": "xbox"}
    ftp_xbox = FTP()
    ftp_xbox.connect(xbox['ip'], xbox['port'])
    ftp_xbox.login(xbox['user'], xbox['pass'])
    print(f"✅ Connected to Xbox at {xbox['ip']}")
    
    selected_files = select_files()
    if not selected_files:
        print("❌ No files found to transfer.")
        sys.exit()
    
    upload_to_xbox(ftp_xbox, selected_files)
    download_from_xbox(ftp_xbox, selected_files)
    
    print("🎉 File sync complete!")
