#!/usr/bin/env python3
import i3ipc
import sys

# Usage: python3 move_global.py [next|prev]

ipc = i3ipc.Connection()

def get_sorted_workspace_windows(workspace):
    """Returns a list of windows on the workspace, sorted by position."""
    # Sort by Y first, then X to read top-to-bottom, left-to-right
    return sorted(workspace.leaves(), key=lambda w: (w.rect.y, w.rect.x))

def move_global(direction="next"):
    tree = ipc.get_tree()
    focused = tree.find_focused()
    
    if not focused:
        return

    current_ws = focused.workspace()
    if not current_ws:
        return

    # Get windows on THIS workspace only
    ws_windows = get_sorted_workspace_windows(current_ws)
    
    # Find our index
    try:
        current_index = [w.id for w in ws_windows].index(focused.id)
    except ValueError:
        return

    # LOGIC GATE: Check if we are at the visual edge
    at_edge = False
    if direction == "next" and current_index == len(ws_windows) - 1:
        at_edge = True
    elif direction == "prev" and current_index == 0:
        at_edge = True

    # SCENARIO A: Not at the edge? Just shuffle window inside current workspace.
    if not at_edge:
        cmd_dir = "right" if direction == "next" else "left"
        ipc.command(f'move {cmd_dir}')
        return

    # SCENARIO B: At the edge? Move to the next NUMERICAL workspace.
    # This fixes the "stuck" bug by forcing creation of the next workspace number.
    current_num = current_ws.num
    
    if direction == "next":
        target_num = current_num + 1
    else:
        target_num = current_num - 1
        # Prevent going to workspace 0 or negative
        if target_num < 1:
            return

    # Move container and follow it
    ipc.command(f'move container to workspace number {target_num}')
    ipc.command(f'workspace number {target_num}')

if __name__ == "__main__":
    direction = "next"
    if len(sys.argv) > 1 and sys.argv[1] == "prev":
        direction = "prev"
    move_global(direction)
