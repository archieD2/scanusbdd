#!/usr/bin/env python3

import pyudev
import sys
import time
import subprocess
import os

def is_usb_storage_device(device):
    """
    Determine if the device is a USB storage device.

    Args:
        device (pyudev.Device): The device to check.

    Returns:
        bool: True if it's a USB storage device, False otherwise.
    """
    if device.device_type not in ['disk', 'partition']:
        return False

    # Check if the device is a USB device
    if device.get('ID_BUS') == 'usb':
        return True

    # Fallback: Check the parent devices
    for parent in device.ancestors:
        if parent.get('ID_BUS') == 'usb':
            return True

    return False

def get_partitions(device):
    """
    Retrieve partition device nodes for a given disk.

    Args:
        device (pyudev.Device): The disk device.

    Returns:
        list: List of partition device nodes.
    """
    partitions = []
    for child in device.children:
        if child.device_type == 'partition':
            partitions.append(child.device_node)
    return partitions

def handle_event(device):
    """
    Handle udev events.

    Args:
        device (pyudev.Device): The device related to the event.
    """
    action = device.action  # Extract the action ('add', 'remove', etc.)

    if is_usb_storage_device(device):
        if action == 'add':
            device_path = device.device_node
            print(f"\n[+] USB Storage Device Connected: {device_path}")
            # If it's a disk, list its partitions
            if device.device_type == 'disk':
                partitions = get_partitions(device)
                if partitions:
                    print("    - Partitions:")
                    for part in partitions:
                        print(f"        - {part}")
                else:
                    print("    - No partitions found.")
            
            # Proceed to prompt user for ISO path and write to USB
            process_usb_connection(device)
            
        elif action == 'remove':
            device_path = device.device_node
            print(f"\n[-] USB Storage Device Removed: {device_path}")

def process_usb_connection(device):
    """
    Handle the process of writing an ISO to the connected USB device.

    Args:
        device (pyudev.Device): The connected USB device.
    """
    device_path = device.device_node

    # Prompt user for ISO path
    while True:
        iso_path = input("\nEnter the path to the ISO file you want to write to the USB drive (or type 'skip' to ignore): ").strip()
        if iso_path.lower() == 'skip':
            print("Skipping writing ISO to USB.")
            return
        if os.path.isfile(iso_path):
            if iso_path.lower().endswith('.iso'):
                break
            else:
                print("The specified file does not have an .iso extension. Please provide a valid ISO file.")
        else:
            print("The specified path does not exist or is not a file. Please try again.")

    # Confirm with the user
    print(f"\nYou are about to write '{iso_path}' to '{device_path}'. This will erase all data on the USB drive.")
    confirmation = input("Type 'yes' to proceed, or anything else to cancel: ").strip().lower()
    if confirmation != 'yes':
        print("Operation canceled by user.")
        return

    # Unmount any mounted partitions on the USB drive
    unmount_partitions(device)

    # Execute the dd command
    write_iso_to_usb(iso_path, device_path)

def unmount_partitions(device):
    """
    Unmount all mounted partitions of the USB device.

    Args:
        device (pyudev.Device): The USB device.
    """
    partitions = get_partitions(device)
    for part in partitions:
        # Check if the partition is mounted
        mount_point = get_mount_point(part)
        if mount_point:
            print(f"Unmounting {part} from {mount_point}...")
            try:
                subprocess.run(['sudo', 'umount', part], check=True)
                print(f"Successfully unmounted {part}.")
            except subprocess.CalledProcessError:
                print(f"Failed to unmount {part}. Please unmount it manually if necessary.")

def get_mount_point(device_node):
    """
    Get the mount point of a device node.

    Args:
        device_node (str): The device node (e.g., /dev/sdb1).

    Returns:
        str or None: The mount point if mounted, else None.
    """
    try:
        result = subprocess.run(['lsblk', '-no', 'MOUNTPOINT', device_node], stdout=subprocess.PIPE, text=True, check=True)
        mount_point = result.stdout.strip()
        return mount_point if mount_point else None
    except subprocess.CalledProcessError:
        return None

def write_iso_to_usb(iso_path, device_path):
    """
    Write the ISO to the USB device using dd.

    Args:
        iso_path (str): Path to the ISO file.
        device_path (str): Device path of the USB (e.g., /dev/sdb).
    """
    print(f"\nWriting ISO to {device_path}...")
    # Build the dd command
    # Using bs=4M, status=progress, oflag=sync
    dd_command = [
        'sudo', 'dd',
        f'if={iso_path}',
        f'of={device_path}',
        'bs=4M',
        'status=progress',
        'oflag=sync'
    ]

    # Inform the user
    print("\nExecuting dd command:")
    print(' '.join(dd_command))
    print("\nThis may take several minutes. Do not interrupt the process.\n")

    try:
        # Run the dd command
        subprocess.run(dd_command, check=True)
        print(f"\n✅ Successfully wrote '{iso_path}' to '{device_path}'.")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ An error occurred while writing the ISO: {e}")
        return

    # Sync to ensure all data is written
    try:
        subprocess.run(['sudo', 'sync'], check=True)
        print("🔄 Sync completed. USB drive is now ready.")
    except subprocess.CalledProcessError as e:
        print(f"❌ An error occurred during sync: {e}")

def main():
    context = pyudev.Context()

    # Create a monitor for block devices
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='block')

    # Use MonitorObserver to handle events asynchronously
    observer = pyudev.MonitorObserver(monitor, callback=handle_event, name='usb-monitor-observer')
    observer.start()

    print("📟 Monitoring USB flash drive connections. Press Ctrl+C to exit.")

    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Exiting...")
        observer.stop()
        sys.exit(0)

if __name__ == "__main__":
    main()
