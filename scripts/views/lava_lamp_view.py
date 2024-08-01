# Cody Tolene
# Apache License 2.0

import uasyncio
import random
from math import sqrt
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY


class LavaLamp:
    def __init__(self, galacticUnicorn, graphics, music):
        self.galacticUnicorn = galacticUnicorn
        self.graphics = graphics
        self.height = galacticUnicorn.HEIGHT
        self.music = music
        self.width = galacticUnicorn.WIDTH

        self.blobs = [self.create_blob() for _ in range(7)]

    def create_blob(self):
        color = (
            random.randint(100, 255),
            random.randint(0, 255),
            random.randint(0, 150),
        )
        pen = self.graphics.create_pen(*color)
        return {
            "color": color,
            "dx": random.uniform(-0.2, 0.2),
            "dy": random.uniform(-0.2, 0.2),
            "pen": pen,
            "radius": random.uniform(2, 5),
            "x": random.uniform(0, self.width),
            "y": random.uniform(0, self.height),
        }

    def distance(self, blob1, blob2):
        return sqrt((blob1["x"] - blob2["x"]) ** 2 + (blob1["y"] - blob2["y"]) ** 2)

    async def update_blob(self, blob):
        blob["x"] += blob["dx"]
        blob["y"] += blob["dy"]
        if blob["x"] - blob["radius"] <= 0 or blob["x"] + blob["radius"] >= self.width:
            blob["dx"] *= -1
        if blob["y"] - blob["radius"] <= 0 or blob["y"] + blob["radius"] >= self.height:
            blob["dy"] *= -1

        self.graphics.set_pen(blob["pen"])
        self.graphics.circle(int(blob["x"]), int(blob["y"]), int(blob["radius"]))

    def update_color(self, blob):
        new_color = (
            min(255, max(0, blob["color"][0] + random.randint(-1, 1))),
            min(255, max(0, blob["color"][1] + random.randint(-1, 1))),
            min(255, max(0, blob["color"][2] + random.randint(-1, 1))),
        )
        blob["color"] = new_color
        blob["pen"] = self.graphics.create_pen(*new_color)

    async def update(self):
        self.graphics.set_pen(self.graphics.create_pen(0, 0, 0))
        self.graphics.clear()

        for blob in self.blobs:
            self.update_color(blob)
            await self.update_blob(blob)

        self.galacticUnicorn.update(self.graphics)


async def run(galacticUnicorn, graphics, music):
    lava_lamp = LavaLamp(galacticUnicorn, graphics, music)

    while True:
        await lava_lamp.update()
        await uasyncio.sleep(0.25)


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
