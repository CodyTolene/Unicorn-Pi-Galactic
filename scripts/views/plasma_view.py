# Cody Tolene
# Apache License 2.0

import uasyncio
import math
import time
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY


class WavePattern:
    def __init__(self, galacticUnicorn, graphics, sound_service):
        self.galacticUnicorn = galacticUnicorn
        self.graphics = graphics
        self.height = galacticUnicorn.HEIGHT
        self.sound_service = sound_service
        self.width = galacticUnicorn.WIDTH

    async def update(self):
        t = time.ticks_ms() / 1000  # Current time in seconds
        for y in range(self.height):
            await uasyncio.sleep_ms(0)
            for x in range(self.width):
                sine_component = math.sin(x / self.width * 8 + t)
                cosine_component = math.cos(y / self.height * 8 + t)
                color_value = (sine_component + cosine_component) * 127.5
                color = int(color_value + 127.5)

                self.graphics.set_pen(self.graphics.create_pen(color, 0, 255 - color))
                self.graphics.pixel(x, y)

        self.galacticUnicorn.update(self.graphics)


async def run(galacticUnicorn, graphics, sound_service):
    wave_pattern = WavePattern(galacticUnicorn, graphics, sound_service)

    while True:
        await wave_pattern.update()
        await uasyncio.sleep(0.1)


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
