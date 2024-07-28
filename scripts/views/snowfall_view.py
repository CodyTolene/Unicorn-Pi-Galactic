# Cody Tolene
# Apache License 2.0

import uasyncio
import random
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY


async def run(galacticUnicorn, graphics):
    width = galacticUnicorn.WIDTH
    height = galacticUnicorn.HEIGHT

    class Snowflake:
        def __init__(self):
            self.x = random.randint(0, width - 1)
            self.y = random.uniform(0, height - 1)
            self.speed_y = random.uniform(0.1, 0.3)
            self.color = graphics.create_pen(
                random.randint(200, 255),
                random.randint(200, 255),
                random.randint(200, 255),
            )
            self.drift_direction = random.choice([-0.1, 0.1])  # Initial drift direction

        async def update(self):
            graphics.set_pen(self.color)
            graphics.pixel(int(self.x), int(self.y))
            self.y += self.speed_y
            self.x += self.drift_direction  # Apply horizontal drift

            # Randomly change direction to create a puffy effect
            if random.random() < 0.3:
                self.drift_direction = random.choice([-0.1, 0.1])

            # Reset snowflake if it moves out of bounds
            if self.y >= height or self.x < 0 or self.x >= width:
                self.y = 0
                self.x = random.randint(0, width - 1)
                self.color = graphics.create_pen(
                    random.randint(200, 255),
                    random.randint(200, 255),
                    random.randint(200, 255),
                )  # New random shade of white
                self.drift_direction = random.choice(
                    [-0.1, 0.1]
                )  # Reset drift direction

    snowflakes = [Snowflake() for _ in range(20)]

    while True:
        graphics.set_pen(graphics.create_pen(0, 0, 0))
        graphics.clear()

        for snowflake in snowflakes:
            await snowflake.update()

        galacticUnicorn.update(graphics)
        await uasyncio.sleep(0.1)


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
