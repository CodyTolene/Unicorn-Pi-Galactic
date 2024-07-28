# Cody Tolene
# Apache License 2.0

import time
import math
import uasyncio
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY


async def run(galacticUnicorn, graphics):
    width = galacticUnicorn.WIDTH
    height = galacticUnicorn.HEIGHT

    while True:
        t = time.ticks_ms() / 1000
        for x in range(width):
            await uasyncio.sleep_ms(0)
            for y in range(height):
                wave_x = math.sin((x / width * 2 * math.pi) + t)
                wave_y = math.sin((y / height * 2 * math.pi) + t)
                wave = (wave_x + wave_y) / 2

                wave = (wave + 1) / 2 * 0.8 + 0.2

                # Map the wave value to a color gradient (e.g. shades of blue)
                blue = int(wave * 255)
                green = int(wave * 127)

                PEN = graphics.create_pen(0, green, blue)
                graphics.set_pen(PEN)
                graphics.pixel(x, y)

        galacticUnicorn.update(graphics)
        await uasyncio.sleep(1.0 / 60)


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
