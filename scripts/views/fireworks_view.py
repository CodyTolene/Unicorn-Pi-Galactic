# Cody Tolene
# Apache License 2.0

import random
import uasyncio

from utils.sounds import FireworkSound


class Firework:
    def __init__(
        self,
        galactic_unicorn,
        options_service,
        pico_graphics,
        sound_service,
        wifi_service,
    ):
        self.galactic_unicorn = galactic_unicorn
        self.height = galactic_unicorn.HEIGHT
        self.options_service = options_service
        self.pico_graphics = pico_graphics
        self.sound_service = FireworkSound(galactic_unicorn, sound_service)
        self.width = galactic_unicorn.WIDTH
        self.wifi_service = wifi_service

        self.launch_x = (
            random.randint(self.width // 4, 3 * self.width // 4)
            if random.random() < 0.8
            else random.randint(1, self.width - 2)
        )

        self.explosion_x = self.launch_x
        self.explosion_y = self.height // 2
        self.brightness = random.uniform(0.5, 1.0)
        self.color = pico_graphics.create_pen(
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

    async def update(self):
        if self.stage == "launch":
            if self.y > self.height // 2:
                self.pico_graphics.set_pen(self.color)
                self.pico_graphics.pixel(self.launch_x, self.y)
                self.y -= 1
            else:
                self.stage = "explode"
                self.sound_service.play()
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
                            self.pico_graphics.set_pen(
                                self.pico_graphics.create_pen(
                                    brightness * (p["color"] >> 16 & 0xFF) // 255,
                                    brightness * (p["color"] >> 8 & 0xFF) // 255,
                                    brightness * (p["color"] & 0xFF) // 255,
                                )
                            )
                            self.pico_graphics.pixel(int(p["x"]), int(p["y"]))


async def run(
    galactic_unicorn, options_service, pico_graphics, sound_service, wifi_service
):
    fireworks = []
    while True:
        pico_graphics.set_pen(pico_graphics.create_pen(0, 0, 0))
        pico_graphics.clear()

        if random.random() < 0.1:
            fireworks.append(
                Firework(
                    galactic_unicorn,
                    options_service,
                    pico_graphics,
                    sound_service,
                    wifi_service,
                )
            )

        for firework in fireworks:
            await firework.update()

        filtered_fireworks = []
        for firework in fireworks:
            has_life = any(p["life"] > 0 for p in firework.particles)
            is_launching = firework.stage == "launch"
            if has_life or is_launching:
                filtered_fireworks.append(firework)
        fireworks = filtered_fireworks

        galactic_unicorn.update(pico_graphics)
        await uasyncio.sleep(0.1)
