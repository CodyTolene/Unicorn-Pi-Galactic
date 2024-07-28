# Cody Tolene
# Apache License 2.0

import random
import uasyncio
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY


async def run(galacticUnicorn, graphics):
    width = galacticUnicorn.WIDTH
    height = galacticUnicorn.HEIGHT

    # Define the size of the "DVD" logo
    logo_width = 2
    logo_height = 1

    # Initialize the position and velocity of the logo
    x = random.randint(0, width - logo_width)
    y = random.randint(0, height - logo_height)
    dx = 1
    dy = 1

    # Define the blue color for the logo
    blue_pen = graphics.create_pen(0, 0, 255)

    # Function to draw the "DVD" logo
    def draw_logo(x, y):
        graphics.set_pen(blue_pen)
        for i in range(logo_width):
            for j in range(logo_height):
                graphics.pixel(x + i, y + j)

    # Function to clear the "DVD" logo
    def clear_logo(x, y):
        graphics.set_pen(graphics.create_pen(0, 0, 0))
        for i in range(logo_width):
            for j in range(logo_height):
                graphics.pixel(x + i, y + j)

    while True:
        # Clear the previous logo position
        clear_logo(x, y)

        # Update the position of the logo
        x += dx
        y += dy

        # Check for collisions with the screen edges
        if x <= 0 or x >= width - logo_width:
            dx = -dx
            graphics.set_pen(
                graphics.create_pen(
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                )
            )
        if y <= 0 or y >= height - logo_height:
            dy = -dy
            graphics.set_pen(
                graphics.create_pen(
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                )
            )

        # Draw the new logo position
        draw_logo(x, y)

        # Update the display
        galacticUnicorn.update(graphics)

        # Wait for a short period to control the animation speed
        await uasyncio.sleep(0.25)


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
