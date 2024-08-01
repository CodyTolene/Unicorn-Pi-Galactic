# Cody Tolene
# Apache License 2.0

import random
import uasyncio

from galactic import GalacticUnicorn, Channel
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY
from utils.music import play_notes, volume


class Firework:
    def __init__(self, graphics, galacticUnicorn):
        self.width = galacticUnicorn.WIDTH
        self.height = galacticUnicorn.HEIGHT
        self.graphics = graphics
        self.galacticUnicorn = galacticUnicorn
        self.channels = [galacticUnicorn.synth_channel(0)]
        self.channels[0].configure(
            waveforms=Channel.NOISE,
            attack=0.005,
            decay=0.500,
            sustain=0,
            release=0.100,
            volume=volume,
        )
        self.launch_x = (
            random.randint(self.width // 4, 3 * self.width // 4)
            if random.random() < 0.8
            else random.randint(1, self.width - 2)
        )
        self.explosion_x = self.launch_x
        self.explosion_y = self.height // 2
        self.brightness = random.uniform(0.5, 1.0)
        self.color = graphics.create_pen(
            int(self.brightness * random.randint(100, 255)),
            int(self.brightness * random.randint(100, 255)),
            int(self.brightness * random.randint(100, 255)),
        )
        self.particles = []
        self.stage = "launch"
        self.y = self.height - 1
        self.create_explosion_particles()

    def create_explosion_particles(self):
        explosion_points = [
            (random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(10)
        ]
        for dx, dy in explosion_points:
            self.particles.append(
                {
                    "x": self.explosion_x + dx,
                    "y": self.explosion_y + dy,
                    "dx": dx,
                    "dy": dy,
                    "color": self.color,
                    "life": 1.0,
                }
            )

    def play_explosion_sound(self):
        explosion_sounds = [
            [800, 850, 900, 950, 1000, -1, -1],
            [1000, 1050, 1100, 1150, 1200, -1, -1],
            [600, 650, 700, 750, 800, -1, -1],
            [1100, 1150, 1200, 1250, 1300, -1, -1],
            [700, 750, 800, 850, 900, -1, -1],
        ]
        selected_sound = random.choice(explosion_sounds)
        play_notes(
            self.galacticUnicorn, [selected_sound], self.channels, bpm=700, repeat=False
        )

    async def update(self):
        if self.stage == "launch":
            if self.y > self.height // 2:
                self.graphics.set_pen(self.color)
                self.graphics.pixel(self.launch_x, self.y)
                self.y -= 1
            else:
                self.stage = "explode"
                self.play_explosion_sound()
        elif self.stage == "explode":
            if any(p["life"] > 0 for p in self.particles):
                for p in self.particles:
                    if p["life"] > 0:
                        p["x"] += p["dx"]
                        p["y"] += p["dy"]
                        p["dy"] += 0.05
                        p["life"] -= 0.05
                        width_in_bounds = 0 <= int(p["x"]) < self.width
                        height_in_bounds = 0 <= int(p["y"]) < self.height
                        if width_in_bounds and height_in_bounds:
                            brightness = int(255 * p["life"])
                            self.graphics.set_pen(
                                self.graphics.create_pen(
                                    brightness * (p["color"] >> 16 & 0xFF) // 255,
                                    brightness * (p["color"] >> 8 & 0xFF) // 255,
                                    brightness * (p["color"] & 0xFF) // 255,
                                )
                            )
                            self.graphics.pixel(int(p["x"]), int(p["y"]))


async def run(galacticUnicorn, graphics):
    fireworks = []
    while True:
        graphics.set_pen(graphics.create_pen(0, 0, 0))
        graphics.clear()

        if random.random() < 0.1:
            fireworks.append(Firework(graphics, galacticUnicorn))

        for firework in fireworks:
            await firework.update()

        filtered_fireworks = []
        for firework in fireworks:
            has_life = any(p["life"] > 0 for p in firework.particles)
            is_launching = firework.stage == "launch"
            if has_life or is_launching:
                filtered_fireworks.append(firework)
        fireworks = filtered_fireworks

        galacticUnicorn.update(graphics)
        await uasyncio.sleep(0.1)


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
