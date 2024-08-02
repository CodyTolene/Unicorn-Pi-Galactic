# Cody Tolene
# Apache License 2.0

import uasyncio
import random
import math


class Fireflies:
    def __init__(self, galacticUnicorn, graphics, sound_service):
        self.galacticUnicorn = galacticUnicorn
        self.graphics = graphics
        self.height = galacticUnicorn.HEIGHT
        self.sound_service = sound_service
        self.width = galacticUnicorn.WIDTH

        self.fireflies = [self.create_firefly() for _ in range(10)]

    def create_firefly(self):
        return {
            "age": 0.0,
            "blue": random.randint(0, 50),
            "brightness": 0.0,
            "green": random.randint(150, 255),
            "life": random.uniform(30.0, 60.0),
            "phase_offset": random.uniform(0, 2 * math.pi),
            "red": random.randint(150, 255),
            "x": random.uniform(0, self.width),
            "y": random.uniform(0, self.height),
        }

    def reset_firefly(self, firefly):
        firefly.update(self.create_firefly())

    async def update_firefly(self, firefly):
        firefly["age"] += 0.1
        firefly["brightness"] = (
            math.sin(firefly["age"] * 2 * math.pi / 10 + firefly["phase_offset"]) + 1
        ) / 2

        if firefly["age"] >= firefly["life"]:
            self.reset_firefly(firefly)

        pen = self.graphics.create_pen(
            int(firefly["red"] * firefly["brightness"]),
            int(firefly["green"] * firefly["brightness"]),
            int(firefly["blue"] * firefly["brightness"]),
        )
        self.graphics.set_pen(pen)
        self.graphics.pixel(int(firefly["x"]), int(firefly["y"]))

    async def update(self):
        self.graphics.set_pen(self.graphics.create_pen(0, 0, 0))
        self.graphics.clear()

        for firefly in self.fireflies:
            await self.update_firefly(firefly)

        self.galacticUnicorn.update(self.graphics)


async def run(galacticUnicorn, graphics, sound_service):
    fireflies = Fireflies(galacticUnicorn, graphics, sound_service)

    while True:
        await fireflies.update()
        await uasyncio.sleep(0.1)
