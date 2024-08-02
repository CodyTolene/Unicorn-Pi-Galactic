# Cody Tolene
# Apache License 2.0

import uasyncio
import random

from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY
from utils.sounds import RaindropsSound


class Raindrops:
    def __init__(self, galacticUnicorn, graphics, sound):
        self.direction = random.choice([-0.3, 0.3])
        self.galacticUnicorn = galacticUnicorn
        self.graphics = graphics
        self.height = galacticUnicorn.HEIGHT
        self.sound = RaindropsSound(galacticUnicorn, sound)
        self.width = galacticUnicorn.WIDTH

        self.raindrops = [
            Raindrop(self.width, self.height, self.graphics, self.direction)
            for _ in range(30)
        ]
        self.sound.play()

    async def update(self):
        self.graphics.set_pen(self.graphics.create_pen(0, 0, 0))
        self.graphics.clear()

        for raindrop in self.raindrops:
            await raindrop.update()

        self.galacticUnicorn.update(self.graphics)


class Raindrop:
    def __init__(self, width, height, graphics, direction):
        self.color = graphics.create_pen(0, 0, random.randint(150, 255))
        self.graphics = graphics
        self.height = height
        self.speed_x = direction
        self.speed_y = random.uniform(0.3, 0.7)
        self.width = width
        self.x = random.randint(0, width - 1)
        self.y = random.uniform(0, height - 1)

    async def update(self):
        self.graphics.set_pen(self.color)
        self.graphics.pixel(int(self.x), int(self.y))
        self.x += self.speed_x
        self.y += self.speed_y
        if self.y >= self.height or self.x < 0 or self.x >= self.width:
            self.y = 0
            self.x = random.randint(0, self.width - 1)


async def run(galacticUnicorn, graphics, sound):
    raindrops = Raindrops(galacticUnicorn, graphics, sound)

    while True:
        await raindrops.update()
        await uasyncio.sleep(0.025)


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
