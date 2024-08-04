# Cody Tolene
# Apache License 2.0

import uasyncio
import random

from utils.sounds import RaindropsSound


class Raindrops:
    def __init__(
        self,
        galactic_unicorn,
        options_service,
        pico_graphics,
        sound_service,
        wifi_service,
    ):
        self.direction = random.choice([-0.3, 0.3])
        self.galactic_unicorn = galactic_unicorn
        self.height = galactic_unicorn.HEIGHT
        self.options_service = options_service
        self.pico_graphics = pico_graphics
        self.sound_service = RaindropsSound(galactic_unicorn, sound_service)
        self.width = galactic_unicorn.WIDTH
        self.wifi_service = wifi_service

        self.raindrops = [
            Raindrop(self.width, self.height, self.pico_graphics, self.direction)
            for _ in range(30)
        ]
        self.sound_service.play()

    async def update(self):
        self.pico_graphics.set_pen(self.pico_graphics.create_pen(0, 0, 0))
        self.pico_graphics.clear()

        for raindrop in self.raindrops:
            await raindrop.update()

        self.galactic_unicorn.update(self.pico_graphics)


class Raindrop:
    def __init__(self, width, height, pico_graphics, direction):
        self.color = pico_graphics.create_pen(0, 0, random.randint(150, 255))
        self.pico_graphics = pico_graphics
        self.height = height
        self.speed_x = direction
        self.speed_y = random.uniform(0.3, 0.7)
        self.width = width
        self.x = random.randint(0, width - 1)
        self.y = random.uniform(0, height - 1)

    async def update(self):
        self.pico_graphics.set_pen(self.color)
        self.pico_graphics.pixel(int(self.x), int(self.y))
        self.x += self.speed_x
        self.y += self.speed_y
        if self.y >= self.height or self.x < 0 or self.x >= self.width:
            self.y = 0
            self.x = random.randint(0, self.width - 1)


async def run(
    galactic_unicorn, options_service, pico_graphics, sound_service, wifi_service
):
    raindrops = Raindrops(
        galactic_unicorn, options_service, pico_graphics, sound_service, wifi_service
    )

    while True:
        await raindrops.update()
        await uasyncio.sleep(0.025)
