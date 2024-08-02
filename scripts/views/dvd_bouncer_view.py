# Cody Tolene
# Apache License 2.0

import random
import uasyncio
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY
from utils.sounds import CelebrationSound, CelebrationSound2, ExplosionSound


class DVDBouncer:
    def __init__(self, galacticUnicorn, graphics, sound_service):
        self.dx = 1 if random.choice([True, False]) else -1
        self.dy = 1 if random.choice([True, False]) else -1
        self.galacticUnicorn = galacticUnicorn
        self.graphics = graphics
        self.height = galacticUnicorn.HEIGHT
        self.logo_height = 1
        self.logo_width = 2
        self.width = galacticUnicorn.WIDTH
        self.x = random.randint(1, self.width - self.logo_width - 1)
        self.y = random.randint(1, self.height - self.logo_height - 1)
        self.color = self.random_color()
        self.celebration_sound = CelebrationSound(galacticUnicorn, sound_service)
        self.celebration_sound_2 = CelebrationSound2(galacticUnicorn, sound_service)
        self.explosion_sound = ExplosionSound(galacticUnicorn, sound_service)

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

        # Check if we hit a diagonal corner
        hit_corner = (self.x <= 0 or self.x >= self.width - self.logo_width) and (
            self.y <= 0 or self.y >= self.height - self.logo_height
        )

        # Update the position of the logo
        self.x += self.dx
        self.y += self.dy

        # Check for collisions with the screen edges
        if self.x <= 0 or self.x >= self.width - self.logo_width:
            self.explosion_sound.play()
            self.dx = -self.dx
            self.color = self.random_color()
            # Ensure it moves away from the edge
            self.x = max(0, min(self.x, self.width - self.logo_width))

        if self.y <= 0 or self.y >= self.height - self.logo_height:
            self.explosion_sound.play()
            self.dy = -self.dy
            self.color = self.random_color()
            # Ensure it moves away from the edge
            self.y = max(0, min(self.y, self.height - self.logo_height))

        # Play random celebration sound if a corner is hit
        if hit_corner:
            if random.choice([True, False]):
                self.celebration_sound.play()
            else:
                self.celebration_sound_2.play()

        self.draw_logo()

    async def update(self):
        self.update_position()
        self.galacticUnicorn.update(self.graphics)


async def run(galacticUnicorn, graphics, sound_service):
    dvd_bouncer = DVDBouncer(galacticUnicorn, graphics, sound_service)

    while True:
        await dvd_bouncer.update()
        await uasyncio.sleep(0.25)


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
