# Cody Tolene
# Apache License 2.0

import uasyncio
import random

from utils.sounds import ThunderSound


class Lightning:
    def __init__(self, galactic_unicorn, pico_graphics, sound_service):
        self.bolts = []
        self.galactic_unicorn = galactic_unicorn
        self.pico_graphics = pico_graphics
        self.height = galactic_unicorn.HEIGHT
        self.sound_service = ThunderSound(galactic_unicorn, sound_service)
        self.width = galactic_unicorn.WIDTH

        self.bolts = [
            self.create_bolt() for _ in range(random.randint(1, 3))
        ]  # Initial bolts

        # Start with a flash immediately
        self.flash = True
        self.flash_duration = random.randint(1, 3)
        self.sound_service.play()

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
        self.pico_graphics.set_pen(self.pico_graphics.create_pen(0, 0, 0))
        self.pico_graphics.clear()

        if self.flash:
            self.pico_graphics.set_pen(self.pico_graphics.create_pen(255, 255, 255))
            for x in range(self.width):
                for y in range(self.height):
                    self.pico_graphics.pixel(x, y)
            self.flash_duration -= 1
            if self.flash_duration <= 0:
                self.flash = False
                self.bolts = []
        else:
            if random.random() < 0.05:
                self.flash = True
                self.flash_duration = random.randint(1, 3)
                self.bolts = [self.create_bolt() for _ in range(random.randint(1, 3))]
                self.sound_service.play()

        for bolt in self.bolts:
            for x, y in bolt:
                self.pico_graphics.set_pen(self.pico_graphics.create_pen(255, 255, 255))
                self.pico_graphics.pixel(x, y)

        self.galactic_unicorn.update(self.pico_graphics)


async def run(galactic_unicorn, pico_graphics, sound_service):
    lightning = Lightning(galactic_unicorn, pico_graphics, sound_service)

    while True:
        await lightning.update()
        await uasyncio.sleep(0.1)
