# Cody Tolene
# Apache License 2.0

import uasyncio
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY


async def run(galacticUnicorn, graphics):
    red = graphics.create_pen(255, 0, 0)
    blue = graphics.create_pen(0, 0, 255)

    while True:
        # Flash red
        graphics.set_pen(red)
        graphics.clear()
        galacticUnicorn.update(graphics)
        await uasyncio.sleep(0.5)

        # Flash blue
        graphics.set_pen(blue)
        graphics.clear()
        galacticUnicorn.update(graphics)
        await uasyncio.sleep(0.5)


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
