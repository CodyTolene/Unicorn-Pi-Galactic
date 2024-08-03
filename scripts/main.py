# Apache License Version 2.0
# Cody Tolene

import uasyncio
import sys

from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN

from utils.button_service import ButtonService
from utils.options_service import OptionsService
from utils.sound_service import SoundService
from utils.view_service import ViewService

# Ensure local packages can be imported
sys.path.append("/utils")
sys.path.append("/views")

if __name__ == "__main__":
    # Initialize GalacticUnicorn
    galactic_unicorn = GalacticUnicorn()

    # Initialize PicoGraphics
    graphics = PicoGraphics(display=DISPLAY_GALACTIC_UNICORN)

    # Initialize the options service
    options_service = OptionsService()

    # Initialize the sound player
    sound_service = SoundService(galactic_unicorn)

    # Initialize the ViewService
    view_service = ViewService(galactic_unicorn, graphics, sound_service)
    view_service.clear_screen()

    # Start the asyncio event loop
    loop = uasyncio.get_event_loop()

    # Start the initial view
    starting_view = view_service.get_current_view()
    current_view_task = loop.create_task(starting_view)

    # Initialize the button service
    button_service = ButtonService(view_service, current_view_task)

    # Create and schedule the button listener coroutine
    loop.create_task(button_service.run())

    # Run the event loop forever
    loop.run_forever()
