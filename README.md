USB Flash Drive Monitor & Bootable ISO Writer

Overview

This Python script monitors USB flash drive connections and provides an easy way to make bootable drives from ISO files. Upon detecting a USB flash drive, it prompts the user for an ISO file path, unmounts any partitions, and writes the ISO to the USB using the dd command. The script is particularly useful for users who frequently create bootable drives for operating system installations.

⚠️ Warning: The dd command used in this script can overwrite any disk without warning. Ensure you double-check the target device to avoid accidental data loss.

Features

Real-Time USB Monitoring: Continuously monitors for USB flash drive connections using pyudev.

Automated Bootable Drive Creation: Prompts the user to provide an ISO file upon detecting a USB connection and uses dd to create a bootable USB drive.

Partition Management: Automatically unmounts any mounted partitions on the USB drive before writing the ISO to prevent issues.

Interactive Safety Prompts: Prompts the user for confirmation before executing the dd command to avoid accidental overwriting of data.

Prerequisites

Python 3: The script is written in Python 3 and should be run with it.

pyudev: The pyudev library is used to interact with udev for device event monitoring.

Install with pip:

pip install pyudev

Or using an AUR helper like yay (for Arch Linux users):

yay -S python-pyudev

Sudo Privileges: Since the script involves writing to block devices and unmounting partitions, sudo privileges are required.

Installation

Clone the repository:

git clone https://github.com/yourusername/usb_iso_writer.git
cd usb_iso_writer

Install the required dependencies using pip:

pip install -r requirements.txt

Make the script executable (optional):

chmod +x usb_monitor_dd.py

Usage

Run the script using Python 3:

sudo python3 usb_monitor_dd.py

What to Expect

The script will display a message indicating that it is monitoring USB flash drive connections.

Upon detecting a USB drive, it will prompt you to enter the path to an ISO file you wish to write to the drive.

After verifying the ISO file, the script will ask for confirmation before proceeding to write the ISO to the USB.

Example Interaction:

📟 Monitoring USB flash drive connections. Press Ctrl+C to exit.

[+] USB Storage Device Connected: /dev/sdb
    - Partitions:
        - /dev/sdb1
        - /dev/sdb2

Enter the path to the ISO file you want to write to the USB drive (or type 'skip' to ignore): /home/user/Downloads/ubuntu-22.04.iso

You are about to write '/home/user/Downloads/ubuntu-22.04.iso' to '/dev/sdb'. This will erase all data on the USB drive.
Type 'yes' to proceed, or anything else to cancel: yes

Unmounting /dev/sdb1 from /run/media/user/USB...
Successfully unmounted /dev/sdb1.
Unmounting /dev/sdb2 from /run/media/user/USB2...
Successfully unmounted /dev/sdb2.

Writing ISO to /dev/sdb...

Executing dd command:
sudo dd if=/home/user/Downloads/ubuntu-22.04.iso of=/dev/sdb bs=4M status=progress oflag=sync

This may take several minutes. Do not interrupt the process.

✅ Successfully wrote '/home/user/Downloads/ubuntu-22.04.iso' to '/dev/sdb'.
🔄 Sync completed. USB drive is now ready.

Stopping the Script

To stop monitoring USB connections, press Ctrl+C.

Important Considerations

Running as Sudo: The script should be run with sudo to perform actions like unmounting and writing to the USB drive.

Double-Check Device Paths: Always confirm the device path (/dev/sdX) before proceeding to prevent data loss on unintended devices.

Do Not Interrupt ****dd: Avoid interrupting the script during the dd operation to prevent data corruption.



Contributing

Contributions are welcome! Feel free to submit issues, pull requests, or feature suggestions.

License

This project is licensed under the MIT License. See the LICENSE file for details.

