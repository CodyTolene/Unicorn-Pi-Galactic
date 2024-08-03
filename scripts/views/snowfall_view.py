# Cody Tolene
# Apache License 2.0

import uasyncio
import random


class Snowfall:
    def __init__(self, galactic_unicorn, pico_graphics, sound_service):
        self.galactic_unicorn = galactic_unicorn
        self.pico_graphics = pico_graphics
        self.height = galactic_unicorn.HEIGHT
        self.sound_service = sound_service
        self.width = galactic_unicorn.WIDTH

        self.snowflakes = [
            self.Snowflake(self.width, self.height, self.pico_graphics, initial=True)
            for _ in range(20)
        ]

    class Snowflake:
        def __init__(self, width, height, pico_graphics, initial=False):
            self.width = width
            self.height = height
            self.pico_graphics = pico_graphics
            self.reset(initial)

        def reset(self, initial=False):
            self.x = random.randint(0, self.width - 1)
            # Start from random position if initial, otherwise from the top
            self.y = random.uniform(0, self.height - 1) if initial else 0
            self.speed_y = random.uniform(0.1, 0.3)
            self.color = self.pico_graphics.create_pen(
                random.randint(200, 255),
                random.randint(200, 255),
                random.randint(200, 255),
            )
            # Initial drift direction
            self.drift_direction = random.choice([-0.1, 0.1])

        async def update(self):
            self.pico_graphics.set_pen(self.color)
            self.pico_graphics.pixel(int(self.x), int(self.y))
            self.y += self.speed_y
            # Side drift
            self.x += self.drift_direction

            # Randomly change direction to create a puffy effect
            if random.random() < 0.3:
                self.drift_direction = random.choice([-0.1, 0.1])

            # Reset snowflake if it moves out of bounds
            if self.y >= self.height or self.x < 0 or self.x >= self.width:
                self.reset()

    async def update(self):
        self.pico_graphics.set_pen(self.pico_graphics.create_pen(0, 0, 0))
        self.pico_graphics.clear()

        for snowflake in self.snowflakes:
            await snowflake.update()

        self.galactic_unicorn.update(self.pico_graphics)


async def run(galactic_unicorn, pico_graphics, sound_service):
    snowfall = Snowfall(galactic_unicorn, pico_graphics, sound_service)

    while True:
        await snowfall.update()
        await uasyncio.sleep(0.1)
