#!/usr/bin/env python3
import sys
import subprocess
import math  # Added missing import

def get_progress_bar(percent, length=50):
    percent = max(0, min(100, percent))
    filled_count = math.ceil((percent / 100) * length)
    empty_count = length - filled_count
    
    # Define colors
    filled_color = "#FFFFFF" # White for filled
    empty_color = "#FFFFFF"  # Grey for empty

    # █ = Full Block, ░ = Light Shade (or just spaces)
    filled_bar = f"<span foreground='{filled_color}'>{'█' * filled_count}</span>"
    empty_bar = f"<span foreground='{empty_color}'>{'░' * empty_count}</span>"
    
    return f"{filled_bar}{empty_bar}"

def get_volume_data():
    try:
        # Get volume from wpctl
        result = subprocess.run(["brightnessctl", "get"], 
                                capture_output=True, text=True).stdout
        
        # Parse "Volume: 0.45" -> 45
        vol_int = int((float(result) * 100) / 500)
        
        # Create the bar
        bar = get_progress_bar(vol_int, 30)
        return bar
    except Exception as e:
        return "Error", str(e)

def send_notification():
    vol_bar = get_volume_data()
    
    # DUNSTIFY COMMAND EXPLAINED:
    # -r 2593  : Replace notification with ID 2593 (arbitrary unique number)
    # -t 2000  : Timeout after 2000ms (2 seconds)
    # -u low   : Urgency low (optional, prevents it from sticking around too long)
    
    subprocess.run([
        "dunstify",
        "-r", "2593",
        "-t", "2000",
        "display",  # Title
        vol_bar                 # Body (Progress Bar)
    ])

if __name__ == "__main__":
    send_notification()
