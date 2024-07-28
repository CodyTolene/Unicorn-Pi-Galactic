# Cody Tolene
# Apache License 2.0

import random
import uasyncio
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY


async def run(galacticUnicorn, graphics):
    width = galacticUnicorn.WIDTH
    height = galacticUnicorn.HEIGHT
    cx = width // 2
    cy = height // 2

    # Generate stars with random positions and speeds
    num_stars = 50
    stars = [
        {
            "x": random.uniform(-width, width),
            "y": random.uniform(-height, height),
            "speed": random.uniform(0.01, 0.1),
        }
        for _ in range(num_stars)
    ]

    while True:
        graphics.set_pen(graphics.create_pen(0, 0, 0))
        graphics.clear()

        for star in stars:
            # Update star position
            star["x"] += star["x"] * star["speed"]
            star["y"] += star["y"] * star["speed"]

            # Reset star if it goes out of bounds
            x_out_of_bounds = star["x"] > width // 2 or star["x"] < -width // 2
            y_out_of_bounds = star["y"] > height // 2 or star["y"] < -height // 2
            if x_out_of_bounds or y_out_of_bounds:
                star["x"] = random.uniform(-width, width)
                star["y"] = random.uniform(-height, height)
                star["speed"] = random.uniform(0.01, 0.1)

            # Calculate screen position
            sx = int(cx + star["x"])
            sy = int(cy + star["y"])

            # Draw star
            if 0 <= sx < width and 0 <= sy < height:
                brightness = int((star["speed"] / 0.1) * 255)
                graphics.set_pen(
                    graphics.create_pen(brightness, brightness, brightness)
                )
                graphics.pixel(sx, sy)

        # Ask the Unicorn to update the graphics
        galacticUnicorn.update(graphics)

        # And sleep, so we update ~ 60fps
        await uasyncio.sleep(1.0 / 60)


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
