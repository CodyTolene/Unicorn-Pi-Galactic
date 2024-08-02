# Apache License Version 2.0
# Cody Tolene

import uasyncio
import sys

from collections import OrderedDict
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN

from views import digital_clock_12_view
from views import digital_clock_24_view
from views import digital_rain_view
from views import dvd_bouncer_view
from views import emergency_view
from views import fire_view
from views import fireflies_view
from views import fireplace_view
from views import fireworks_view
from views import flashlight_torch_view
from views import lava_lamp_view
from views import lightning_view
from views import nyan_cat_view
from views import plasma_view
from views import rainbow_view
from views import raindrops_view
from views import snowfall_view
from views import sos_signal_view
from views import warp_speed_view
from views import wave_view

from utils.button_listener import buttonListenerProcess
from utils.sound_service import SoundService
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
        ("DVD Bouncer", dvd_bouncer_view.run),
        ("Digital Clock 12-Hour", digital_clock_12_view.run),
        ("Digital Clock 24-Hour", digital_clock_24_view.run),
        ("Digital Rain", digital_rain_view.run),
        ("Emergency", emergency_view.run),
        ("Fire", fire_view.run),
        ("Fireflies", fireflies_view.run),
        ("Fireplace", fireplace_view.run),
        ("Fireworks", fireworks_view.run),
        ("Flashlight Torch", flashlight_torch_view.run),
        ("Lava Lamp", lava_lamp_view.run),
        ("Lightning", lightning_view.run),
        ("Nyan Cat", nyan_cat_view.run),
        ("Plasma", plasma_view.run),
        ("Rainbow", rainbow_view.run),
        ("Raindrops", raindrops_view.run),
        ("SOS", sos_signal_view.run),
        ("Snowfall", snowfall_view.run),
        ("Warp Speed", warp_speed_view.run),
        ("Wave", wave_view.run),
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

    # Initialize the sound player
    sound_service = SoundService(galacticUnicorn)

    # Start the asyncio event loop
    loop = uasyncio.get_event_loop()

    # Start the initial view
    currentViewTask = loop.create_task(
        views[currentViewKey](galacticUnicorn, graphics, sound_service)
    )

    # Create and schedule the button listener coroutine
    loop.create_task(
        buttonListenerProcess(
            views,
            galacticUnicorn,
            graphics,
            currentViewKey,
            currentViewTask,
            sound_service,
        )
    )

    # Run the event loop forever
    loop.run_forever()
