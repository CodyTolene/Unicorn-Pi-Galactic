# Cody Tolene
# Apache License 2.0

import time
import math
import uasyncio


class Wave:
    def __init__(
        self,
        galactic_unicorn,
        options_service,
        pico_graphics,
        sound_service,
        wifi_service,
    ):
        self.galactic_unicorn = galactic_unicorn
        self.height = galactic_unicorn.HEIGHT
        self.options_service = options_service
        self.pico_graphics = pico_graphics
        self.sound_service = sound_service
        self.width = galactic_unicorn.WIDTH
        self.wifi_service = wifi_service

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

                PEN = self.pico_graphics.create_pen(0, green, blue)
                self.pico_graphics.set_pen(PEN)
                self.pico_graphics.pixel(x, y)

        self.galactic_unicorn.update(self.pico_graphics)


async def run(
    galactic_unicorn, options_service, pico_graphics, sound_service, wifi_service
):
    wave = Wave(
        galactic_unicorn, options_service, pico_graphics, sound_service, wifi_service
    )

    while True:
        await wave.update()
        await uasyncio.sleep(0.1)
