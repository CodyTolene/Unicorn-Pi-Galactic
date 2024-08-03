# Cody Tolene
# Apache License 2.0

import uasyncio
import random

from math import sqrt


class LavaLamp:
    def __init__(self, galactic_unicorn, pico_graphics, sound_service):
        self.galactic_unicorn = galactic_unicorn
        self.pico_graphics = pico_graphics
        self.height = galactic_unicorn.HEIGHT
        self.sound_service = sound_service
        self.width = galactic_unicorn.WIDTH

        self.blobs = [self.create_blob() for _ in range(7)]

    def create_blob(self):
        color = (
            random.randint(100, 255),
            random.randint(0, 255),
            random.randint(0, 150),
        )
        pen = self.pico_graphics.create_pen(*color)
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

        self.pico_graphics.set_pen(blob["pen"])
        self.pico_graphics.circle(int(blob["x"]), int(blob["y"]), int(blob["radius"]))

    def update_color(self, blob):
        new_color = (
            min(255, max(0, blob["color"][0] + random.randint(-1, 1))),
            min(255, max(0, blob["color"][1] + random.randint(-1, 1))),
            min(255, max(0, blob["color"][2] + random.randint(-1, 1))),
        )
        blob["color"] = new_color
        blob["pen"] = self.pico_graphics.create_pen(*new_color)

    async def update(self):
        self.pico_graphics.set_pen(self.pico_graphics.create_pen(0, 0, 0))
        self.pico_graphics.clear()

        for blob in self.blobs:
            self.update_color(blob)
            await self.update_blob(blob)

        self.galactic_unicorn.update(self.pico_graphics)


async def run(galactic_unicorn, pico_graphics, sound_service):
    lava_lamp = LavaLamp(galactic_unicorn, pico_graphics, sound_service)

    while True:
        await lava_lamp.update()
        await uasyncio.sleep(0.25)
