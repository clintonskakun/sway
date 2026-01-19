#!/usr/bin/env python3
import i3ipc
import sys

# Connect to sway
ipc = i3ipc.Connection()

def cycle_global(direction="next"):
    tree = ipc.get_tree()
    focused = tree.find_focused()
    
    # FIX: Changed 'null' to 'None'
    # We filter for standard containers that belong to a workspace
    all_windows = [w for w in tree.leaves() if w.type == "con" and w.workspace() is not None]

    if not focused or not all_windows:
        return

    # Find current index
    try:
        current_index = [w.id for w in all_windows].index(focused.id)
    except ValueError:
        # If the focused window isn't in our list (e.g. a floating tool), start at 0
        current_index = 0

    # Calculate next index
    if direction == "next":
        next_index = (current_index + 1) % len(all_windows)
    else:
        next_index = (current_index - 1) % len(all_windows)

    # Focus the next window
    next_window = all_windows[next_index]
    ipc.command(f'[con_id={next_window.id}] focus')

if __name__ == "__main__":
    direction = "next"
    if len(sys.argv) > 1 and sys.argv[1] == "prev":
        direction = "prev"
    cycle_global(direction)
