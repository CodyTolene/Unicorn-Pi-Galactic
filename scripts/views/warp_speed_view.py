# Cody Tolene
# Apache License 2.0

import random
import uasyncio
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY


class WarpSpeed:
    def __init__(self, galacticUnicorn, graphics, num_stars=50):
        self.galacticUnicorn = galacticUnicorn
        self.graphics = graphics
        self.width = galacticUnicorn.WIDTH
        self.height = galacticUnicorn.HEIGHT
        self.cx = self.width // 2
        self.cy = self.height // 2
        self.stars = [
            {
                "x": random.uniform(-self.width, self.width),
                "y": random.uniform(-self.height, self.height),
                "speed": random.uniform(0.01, 0.1),
            }
            for _ in range(num_stars)
        ]

    def reset_star(self, star):
        star["x"] = random.uniform(-self.width, self.width)
        star["y"] = random.uniform(-self.height, self.height)
        star["speed"] = random.uniform(0.01, 0.1)

    async def update_star(self, star):
        star["x"] += star["x"] * star["speed"]
        star["y"] += star["y"] * star["speed"]

        if (
            star["x"] > self.width // 2  # noqa: W503
            or star["x"] < -self.width // 2  # noqa: W503
            or star["y"] > self.height // 2  # noqa: W503
            or star["y"] < -self.height // 2  # noqa: W503
        ):
            self.reset_star(star)

        sx = int(self.cx + star["x"])
        sy = int(self.cy + star["y"])

        if 0 <= sx < self.width and 0 <= sy < self.height:
            brightness = int((star["speed"] / 0.1) * 255)
            self.graphics.set_pen(
                self.graphics.create_pen(brightness, brightness, brightness)
            )
            self.graphics.pixel(sx, sy)

    async def update(self):
        self.graphics.set_pen(self.graphics.create_pen(0, 0, 0))
        self.graphics.clear()

        for star in self.stars:
            await self.update_star(star)

        self.galacticUnicorn.update(self.graphics)


async def run(galacticUnicorn, graphics):
    warp_speed = WarpSpeed(galacticUnicorn, graphics)

    while True:
        await warp_speed.update()
        await uasyncio.sleep(0.016)


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
