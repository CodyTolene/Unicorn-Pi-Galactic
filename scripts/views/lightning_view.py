# Cody Tolene
# Apache License 2.0

import uasyncio
import random

from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY
from utils.sounds import ThunderSound


class Lightning:
    def __init__(self, galacticUnicorn, graphics, sound):
        self.bolts = []
        self.flash = False
        self.flash_duration = 0
        self.galacticUnicorn = galacticUnicorn
        self.graphics = graphics
        self.height = galacticUnicorn.HEIGHT
        self.sound = ThunderSound(galacticUnicorn, sound)
        self.width = galacticUnicorn.WIDTH

    def create_bolt(self):
        bolt = []
        x = random.randint(0, self.width - 1)
        y = 0
        while y < self.height:
            bolt.append((x, y))
            x += random.choice([-1, 0, 1])
            x = max(0, min(x, self.width - 1))
            y += 1
        return bolt

    async def update(self):
        self.graphics.set_pen(self.graphics.create_pen(0, 0, 0))
        self.graphics.clear()

        if self.flash:
            self.graphics.set_pen(self.graphics.create_pen(255, 255, 255))
            for x in range(self.width):
                for y in range(self.height):
                    self.graphics.pixel(x, y)
            self.flash_duration -= 1
            if self.flash_duration <= 0:
                self.flash = False
                self.bolts = []
        else:
            if random.random() < 0.05:
                self.flash = True
                self.flash_duration = random.randint(1, 3)
                self.bolts = [self.create_bolt() for _ in range(random.randint(1, 3))]
                self.sound.play()

        for bolt in self.bolts:
            for x, y in bolt:
                self.graphics.set_pen(self.graphics.create_pen(255, 255, 255))
                self.graphics.pixel(x, y)

        self.galacticUnicorn.update(self.graphics)


async def run(galacticUnicorn, graphics, sound):
    lightning = Lightning(galacticUnicorn, graphics, sound)

    while True:
        await lightning.update()
        await uasyncio.sleep(0.1)


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
