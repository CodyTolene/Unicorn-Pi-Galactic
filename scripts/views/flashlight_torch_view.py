# Cody Tolene
# Apache License 2.0

import uasyncio
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY


async def run(galacticUnicorn, graphics):
    white = graphics.create_pen(255, 255, 255)

    while True:
        graphics.set_pen(white)
        graphics.clear()
        galacticUnicorn.update(graphics)
        await uasyncio.sleep(0.1)


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
