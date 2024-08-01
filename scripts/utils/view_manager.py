# Cody Tolene
# Apache License 2.0

import uasyncio
import json

VIEW_INDEX_FILE = "/current_view.json"


# Save the current view index to a file
def save_current_view_index(key):
    with open(VIEW_INDEX_FILE, "w") as f:
        json.dump({"current_view_key": key}, f)


# Load the current view index from a file
def load_current_view_index():
    try:
        with open(VIEW_INDEX_FILE, "r") as f:
            data = json.load(f)
            return data.get("current_view_key", "Rainbow")
    except OSError:
        return "Rainbow"


# Switch to the current view
async def switch_view(
    views, currentViewKey, currentViewTask, galacticUnicorn, graphics, music
):
    if currentViewTask:
        currentViewTask.cancel()
        try:
            await currentViewTask
        except uasyncio.CancelledError:
            pass

    # Clear the screen
    graphics.set_pen(0)  # Black
    graphics.clear()
    galacticUnicorn.update(graphics)
    save_current_view_index(currentViewKey)
    currentViewTask = uasyncio.create_task(
        views[currentViewKey](galacticUnicorn, graphics, music)
    )
    return currentViewTask
