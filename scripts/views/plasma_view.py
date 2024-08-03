# Cody Tolene
# Apache License 2.0

import uasyncio
import math
import time


class WavePattern:
    def __init__(self, galactic_unicorn, pico_graphics, sound_service):
        self.galactic_unicorn = galactic_unicorn
        self.pico_graphics = pico_graphics
        self.height = galactic_unicorn.HEIGHT
        self.sound_service = sound_service
        self.width = galactic_unicorn.WIDTH

    async def update(self):
        t = time.ticks_ms() / 1000  # Current time in seconds
        for y in range(self.height):
            await uasyncio.sleep_ms(0)
            for x in range(self.width):
                sine_component = math.sin(x / self.width * 8 + t)
                cosine_component = math.cos(y / self.height * 8 + t)
                color_value = (sine_component + cosine_component) * 127.5
                color = int(color_value + 127.5)

                self.pico_graphics.set_pen(
                    self.pico_graphics.create_pen(color, 0, 255 - color)
                )
                self.pico_graphics.pixel(x, y)

        self.galactic_unicorn.update(self.pico_graphics)


async def run(galactic_unicorn, pico_graphics, sound_service):
    wave_pattern = WavePattern(galactic_unicorn, pico_graphics, sound_service)

    while True:
        await wave_pattern.update()
        await uasyncio.sleep(0.1)
