import uasyncio
import random
import math
from utils.sounds import CricketSound


class Fireflies:
    def __init__(self, galactic_unicorn, pico_graphics, sound_service):
        self.galactic_unicorn = galactic_unicorn
        self.pico_graphics = pico_graphics
        self.height = galactic_unicorn.HEIGHT
        self.sounds = CricketSound(galactic_unicorn, sound_service)
        self.width = galactic_unicorn.WIDTH
        self.fireflies = [self.create_firefly() for _ in range(10)]
        self.chirping_task = None
        self.update_task = None

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

        pen = self.pico_graphics.create_pen(
            int(firefly["red"] * firefly["brightness"]),
            int(firefly["green"] * firefly["brightness"]),
            int(firefly["blue"] * firefly["brightness"]),
        )
        self.pico_graphics.set_pen(pen)
        self.pico_graphics.pixel(int(firefly["x"]), int(firefly["y"]))

    async def update(self):
        while True:
            self.pico_graphics.set_pen(self.pico_graphics.create_pen(0, 0, 0))
            self.pico_graphics.clear()

            for firefly in self.fireflies:
                await self.update_firefly(firefly)

            self.galactic_unicorn.update(self.pico_graphics)
            await uasyncio.sleep(0.1)  # Ensures correct pacing of updates

    async def play_cricket_sound(self):
        while True:
            self.sounds.play()
            await uasyncio.sleep(random.uniform(8, 30))

    def start_chirping(self):
        if self.chirping_task is None:
            self.chirping_task = uasyncio.create_task(self.play_cricket_sound())

    def stop_chirping(self):
        if self.chirping_task is not None:
            self.chirping_task.cancel()
            self.chirping_task = None

    def start_update(self):
        if self.update_task is None:
            self.update_task = uasyncio.create_task(self.update())

    def stop_update(self):
        if self.update_task is not None:
            self.update_task.cancel()
            self.update_task = None


async def run(galactic_unicorn, pico_graphics, sound_service):
    fireflies = Fireflies(galactic_unicorn, pico_graphics, sound_service)
    fireflies.start_update()
    fireflies.start_chirping()

    try:
        while True:
            await uasyncio.sleep(1)
    finally:
        # Stop when exiting scene.
        fireflies.stop_chirping()
        fireflies.stop_update()
