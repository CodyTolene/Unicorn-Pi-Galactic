# Cody Tolene
# Apache License 2.0

import uasyncio
import math
import time
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY


async def run(galacticUnicorn, graphics):
    width = galacticUnicorn.WIDTH
    height = galacticUnicorn.HEIGHT

    while True:
        t = time.ticks_ms() / 1000  # Current time in seconds
        for y in range(height):
            await uasyncio.sleep_ms(0)
            for x in range(width):
                sine_component = math.sin(x / width * 8 + t)
                cosine_component = math.cos(y / height * 8 + t)
                color_value = (sine_component + cosine_component) * 127.5
                color = int(color_value + 127.5)

                graphics.set_pen(graphics.create_pen(color, 0, 255 - color))
                graphics.pixel(x, y)

        galacticUnicorn.update(graphics)
        await uasyncio.sleep(0.1)


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
