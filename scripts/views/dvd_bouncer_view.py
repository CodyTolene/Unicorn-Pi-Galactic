# Cody Tolene
# Apache License 2.0

import random
import uasyncio
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY


class DVDBouncer:
    def __init__(self, galacticUnicorn, graphics, sound):
        self.dx = 1 if random.choice([True, False]) else -1
        self.dy = 1 if random.choice([True, False]) else -1
        self.galacticUnicorn = galacticUnicorn
        self.graphics = graphics
        self.height = galacticUnicorn.HEIGHT
        self.logo_height = 1
        self.logo_width = 2
        self.sound = sound
        self.width = galacticUnicorn.WIDTH
        self.x = random.randint(1, self.width - self.logo_width - 1)
        self.y = random.randint(1, self.height - self.logo_height - 1)
        self.color = self.random_color()

    def random_color(self):
        return self.graphics.create_pen(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

    def draw_logo(self):
        self.graphics.set_pen(self.color)
        for i in range(self.logo_width):
            for j in range(self.logo_height):
                self.graphics.pixel(self.x + i, self.y + j)

    def clear_logo(self):
        self.graphics.set_pen(self.graphics.create_pen(0, 0, 0))
        for i in range(self.logo_width):
            for j in range(self.logo_height):
                self.graphics.pixel(self.x + i, self.y + j)

    def update_position(self):
        self.clear_logo()

        # Update the position of the logo
        self.x += self.dx
        self.y += self.dy

        # Check for collisions with the screen edges
        if self.x <= 0 or self.x >= self.width - self.logo_width:
            self.dx = -self.dx
            self.color = self.random_color()
            # Ensure it moves away from the edge
            self.x = max(0, min(self.x, self.width - self.logo_width))

        if self.y <= 0 or self.y >= self.height - self.logo_height:
            self.dy = -self.dy
            self.color = self.random_color()
            # Ensure it moves away from the edge
            self.y = max(0, min(self.y, self.height - self.logo_height))

        self.draw_logo()

    async def update(self):
        self.update_position()
        self.galacticUnicorn.update(self.graphics)


async def run(galacticUnicorn, graphics, sound):
    dvd_bouncer = DVDBouncer(galacticUnicorn, graphics, sound)

    while True:
        await dvd_bouncer.update()
        await uasyncio.sleep(0.25)


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
