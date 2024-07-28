# Cody Tolene
# Apache License 2.0

import uasyncio
import math
import time
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY


async def run(galacticUnicorn, graphics):
    width = galacticUnicorn.WIDTH  # Get the width of the display
    height = galacticUnicorn.HEIGHT  # Get the height of the display

    while True:
        t = time.ticks_ms() / 1000  # Get the current time in seconds
        for y in range(height):
            for x in range(width):
                # Calculate the color based on sine and cosine functions
                sine_component = math.sin(x / width * 8 + t)
                cosine_component = math.cos(y / height * 8 + t)
                color_value = (sine_component + cosine_component) * 127.5
                color = int(color_value + 127.5)

                # Set the pen to the calculated color
                graphics.set_pen(graphics.create_pen(color, 0, 255 - color))
                # Draw the pixel at (x, y) with the current pen color
                graphics.pixel(x, y)
        # Update the display with the new graphics
        galacticUnicorn.update(graphics)
        # Wait for a short time before the next update
        await uasyncio.sleep(0.1)


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
