#!/usr/bin/env python3

import os
import subprocess
import urllib.request

def run_as_sudo():
    """
    Ensure the script is running with sudo privileges by prompting for the user's password.
    """
    if os.geteuid() != 0:
        print("This script requires root privileges. Please enter your password.")
        try:
            subprocess.run(["sudo", "-v"], check=True)
        except subprocess.CalledProcessError:
            print("Failed to gain root privileges. Exiting.")
            exit(1)

def get_linux_distribution():
    """
    Provide a list of popular Linux distributions and prompt the user to choose one.

    Returns:
        str: The chosen Linux distribution.
    """
    distros = [
        "Ubuntu",
        "Debian",
        "Arch Linux",
        "Fedora",
        "openSUSE",
        "CentOS",
        "Manjaro",
        "Linux Mint",
        "Pop!_OS",
        "Elementary OS"
    ]

    print("Please select your Linux distribution:")
    for i, distro in enumerate(distros, 1):
        print(f"{i}. {distro}")

    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(distros):
                print(f"[DEBUG] User selected: {distros[choice - 1]}")
                return distros[choice - 1]
            else:
                print("Invalid choice. Please select a number between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 10.")

def determine_paths(distro):
    """
    Determine paths based on the Linux distribution.

    Args:
        distro (str): The chosen Linux distribution.

    Returns:
        dict: Dictionary containing paths for installation.
    """
    print(f"[DEBUG] Determining paths for distro: {distro}")
    paths = {
        "bin_path": "/usr/local/bin",
        "script_path": "/usr/local/bin/usbwriter"
    }

    if distro in ["Ubuntu", "Debian", "Linux Mint", "Pop!_OS", "Elementary OS"]:
        paths["bin_path"] = "/usr/local/bin"
    elif distro in ["Arch Linux", "Manjaro"]:
        paths["bin_path"] = "/usr/local/bin"
    elif distro in ["Fedora", "openSUSE", "CentOS"]:
        paths["bin_path"] = "/usr/local/bin"

    print(f"[DEBUG] Paths determined: {paths}")
    return paths

def install_usbwriter(paths):
    """
    Install the usbwriter script to the appropriate location.

    Args:
        paths (dict): Dictionary containing paths for installation.
    """
    source_script = "usb_monitor_dd.py"
    target_path = os.path.join(paths["bin_path"], "usbwriter")

    print(f"[DEBUG] Source script: {source_script}")
    print(f"[DEBUG] Target path: {target_path}")

    if not os.path.isfile(source_script):
        print(f"{source_script} not found. Downloading from the remote server...")
        try:
            urllib.request.urlretrieve("http://davidsklepmistr.jecool.net/usb_monitor_dd.py", source_script)
            print(f"[DEBUG] Successfully downloaded {source_script}.")
        except Exception as e:
            print(f"Error: Failed to download {source_script}. {e}")
            return

    try:
        # Make the script executable
        print(f"[DEBUG] Making {source_script} executable.")
        subprocess.run(["chmod", "+x", source_script], check=True)
        # Move the script to the target path
        print(f"[DEBUG] Moving {source_script} to {target_path}.")
        subprocess.run(["sudo", "mv", source_script, target_path], check=True)
        print(f"usbwriter installed successfully to {target_path}.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during installation: {e}")

def main():
    run_as_sudo()
    print("[DEBUG] Starting usbwriter installation process.")
    distro = get_linux_distribution()
    paths = determine_paths(distro)
    install_usbwriter(paths)
    print("[DEBUG] usbwriter installation process completed.")

if __name__ == "__main__":
    main()

