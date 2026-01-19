#!/usr/bin/env python3
import sys
import subprocess
import math
import time

def get_progress_bar(percent, length=10, colors=False):
    percent = max(0, min(100, percent))
    filled_count = math.ceil((percent / 100) * length)
    empty_count = length - filled_count
    color = "#CCCCCC"

    # Color Logic
    if colors:
        if percent <= 20: color = "#FF5555"
        elif percent <= 40: color = "#FFAA55"
        else: color = "#CCCCCC"

    # █ = Full Block, ░ = Light Shade
    filled_bar = f"<span foreground='{color}'>{'█' * filled_count}</span>"
    empty_bar = f"<span foreground='#ffffff'>{'░' * empty_count}</span>"
   
    return f"{filled_bar}{empty_bar}"

def get_battery():
    try:
        # Most laptops use BAT0 or BAT1. Check /sys/class/power_supply/ if unsure.
        with open("/sys/class/power_supply/macsmc-battery/capacity", "r") as f:
            val = int(f.read().strip())
        return get_progress_bar(val, 5, True)
    except FileNotFoundError:
        return "[ AC ]"

def get_wifi():
    try:
        # Run the command: iw dev wlan0 link
        # This is the standard for modern drivers (including Asahi)
        output = subprocess.check_output(["iw", "dev", "wlan0", "link"], text=True)
        
        for line in output.split("\n"):
            if "signal:" in line:
                # Line looks like: "	signal: -73 dBm"
                parts = line.split()
                # Grab the number (e.g., -73)
                dbm = int(float(parts[1]))
                
                # CONVERT dBm TO PERCENTAGE:
                # -30 dBm (or higher) is 100%
                # -80 dBm (or lower) is 0%
                percent = 2 * (dbm + 100)
                
                return get_progress_bar(percent, 5)
                
    except Exception:
        pass

    return "none"

def get_ram():
    try:
        # standard linux way to get memory without external libraries
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()

        mem_info = {}
        for line in lines:
            parts = line.split()
            # Create a dictionary like {'MemTotal': 16000, 'MemAvailable': 8000}
            mem_info[parts[0].strip(':')] = int(parts[1])

        total = mem_info.get('MemTotal', 1)
        available = mem_info.get('MemAvailable', 0)
        
        # Calculate used memory
        used = total - available
        percent = (used / total) * 100
        
        # Note: colors=False because your color logic highlights LOW numbers (good for battery)
        # but for RAM, low numbers are normal. We keep it grey.
        return get_progress_bar(percent, 6, False)
    except Exception:
        return "err"

if __name__ == "__main__":
    while True:
        # Construct the status line
        status = f" bat {get_battery()} wifi {get_wifi()} ram {get_ram()}"
        
        # Print to stdout with flush to ensure instant update
        print(status, flush=True)
        
        # Wait 1 second before next update
        time.sleep(3)
