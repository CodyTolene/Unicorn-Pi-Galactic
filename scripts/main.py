# Apache License Version 2.0
# Cody Tolene

import uasyncio
import sys

from collections import OrderedDict
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN
from galactic import GalacticUnicorn

from views import digital_rain_view
from views import lightning_view
from views import rainbow_view

from utils.button_listener import buttonListenerProcess
from utils.view_manager import load_current_view_index

# Ensure local packages can be imported
sys.path.append("/utils")
sys.path.append("/views")

# Initialize GalacticUnicorn & PicoGraphics
galacticUnicorn = GalacticUnicorn()
graphics = PicoGraphics(display=DISPLAY_GALACTIC_UNICORN)

# Ordered dictionary of view functions
views = OrderedDict(
    [
        ("Digital Rain", digital_rain_view.run),
        ("Lightning", lightning_view.run),
        ("Rainbow", rainbow_view.run),
    ]
)

# Current key of the view being displayed
currentViewKey = load_current_view_index()

# Task to keep track of the current running view
currentViewTask = None

if __name__ == "__main__":
    # Clear the screen initially
    graphics.set_pen(0)  # Black
    graphics.clear()
    galacticUnicorn.update(graphics)

    # Start the asyncio event loop
    loop = uasyncio.get_event_loop()

    # Start the initial view
    currentViewTask = loop.create_task(views[currentViewKey](galacticUnicorn, graphics))

    # Create and schedule the button listener coroutine
    loop.create_task(
        buttonListenerProcess(
            views, galacticUnicorn, graphics, currentViewKey, currentViewTask
        )
    )

    # Run the event loop forever
    loop.run_forever()
