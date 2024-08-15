# Apache License Version 2.0
# Cody Tolene

import uasyncio
import sys

from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN

# Import local packages
from utils.button_service import ButtonService
from utils.options_service import OptionsService
from utils.sound_service import SoundService
from utils.view_service import ViewService
from utils.wifi_service import WiFiService

# Ensure local packages can be imported
sys.path.append("/utils")
sys.path.append("/views")


async def main():
    # Initialize GalacticUnicorn
    galactic_unicorn = GalacticUnicorn()

    # Initialize PicoGraphics
    pico_graphics = PicoGraphics(display=DISPLAY_GALACTIC_UNICORN)

    # Initialize the options service
    options_service = OptionsService()

    # Initialize the sound service
    sound_service = SoundService(galactic_unicorn)

    # Initialize Wi-Fi service
    wifi_service = WiFiService(options_service)

    # Connect to Wi-Fi if credentials are provided in `options.json`
    await wifi_service.connect()

    # Initialize the ViewService
    view_service = ViewService(
        galactic_unicorn, options_service, pico_graphics, sound_service, wifi_service
    )
    view_service.clear_screen()

    # Initialize the button service
    button_service = ButtonService(view_service)

    # Create and schedule the button listener coroutine
    uasyncio.create_task(button_service.run())

    # Keep the main loop running indefinitely
    while True:
        await uasyncio.sleep(1)


if __name__ == "__main__":
    # Run the asyncio event loop
    uasyncio.run(main())
