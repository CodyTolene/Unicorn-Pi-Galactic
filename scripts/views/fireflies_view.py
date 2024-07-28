# Cody Tolene
# Apache License 2.0

import uasyncio
import random
import math
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY


class Firefly:
    def __init__(self, width, height, graphics):
        self.graphics = graphics
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        self.x = random.uniform(0, self.width)  # Random initial x position
        self.y = random.uniform(0, self.height)  # Random initial y position
        self.red = random.randint(150, 255)  # Higher red component for yellow
        self.green = random.randint(150, 255)  # Higher green component for yellow
        self.blue = random.randint(0, 50)  # Lower blue component for yellow
        self.brightness = 0.0  # Start with zero brightness
        self.life = random.uniform(
            30.0, 60.0
        )  # Initial life duration, between 30 and 60 seconds
        self.age = 0.0  # Age of the firefly
        self.phase_offset = random.uniform(
            0, 2 * math.pi
        )  # Random phase offset for independence

    async def update(self):
        # Increase age
        self.age += 0.1

        # Adjust brightness using a sine wave for smooth dimming in and out
        self.brightness = (
            math.sin(self.age * 2 * math.pi / 10 + self.phase_offset) + 1
        ) / 2

        # Reset firefly when its life runs out
        if self.age >= self.life:
            self.reset()

        # Create pen with updated brightness values
        pen = self.graphics.create_pen(
            int(self.red * self.brightness),
            int(self.green * self.brightness),
            int(self.blue * self.brightness),
        )
        self.graphics.set_pen(pen)
        self.graphics.pixel(int(self.x), int(self.y))


async def run(galacticUnicorn, graphics):
    width = galacticUnicorn.WIDTH  # Get the width of the display
    height = galacticUnicorn.HEIGHT  # Get the height of the display

    # Create fireflies
    fireflies = [Firefly(width, height, graphics) for _ in range(10)]

    while True:
        graphics.set_pen(graphics.create_pen(0, 0, 0))  # Clear the screen
        graphics.clear()

        for firefly in fireflies:
            await firefly.update()  # Update each firefly

        galacticUnicorn.update(graphics)  # Update the display
        await uasyncio.sleep(0.1)  # Pause for a short time before the next update


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
