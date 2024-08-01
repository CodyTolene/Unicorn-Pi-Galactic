# Cody Tolene
# Apache License 2.0

import time
import math
import uasyncio
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY


class Wave:
    def __init__(self, galacticUnicorn, graphics, music):
        self.galacticUnicorn = galacticUnicorn
        self.graphics = graphics
        self.height = galacticUnicorn.HEIGHT
        self.music = music
        self.width = galacticUnicorn.WIDTH

    async def update(self):
        t = time.ticks_ms() / 1000
        for x in range(self.width):
            await uasyncio.sleep_ms(0)
            for y in range(self.height):
                wave_x = math.sin((x / self.width * 2 * math.pi) + t)
                wave_y = math.sin((y / self.height * 2 * math.pi) + t)
                wave = (wave_x + wave_y) / 2

                wave = (wave + 1) / 2 * 0.8 + 0.2

                # Map the wave value to a color gradient (e.g. shades of blue)
                blue = int(wave * 255)
                green = int(wave * 127)

                PEN = self.graphics.create_pen(0, green, blue)
                self.graphics.set_pen(PEN)
                self.graphics.pixel(x, y)

        self.galacticUnicorn.update(self.graphics)


async def run(galacticUnicorn, graphics, music):
    wave = Wave(galacticUnicorn, graphics, music)

    while True:
        await wave.update()
        await uasyncio.sleep(0.1)


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
