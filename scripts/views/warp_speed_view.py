# Cody Tolene
# Apache License 2.0

import random
import uasyncio


class WarpSpeed:
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
        self.sound_service = sound_service
        self.width = galactic_unicorn.WIDTH
        self.wifi_service = wifi_service

        self.cx = self.width // 2
        self.cy = self.height // 2

        self.startCount = 50
        self.stars = [
            {
                "x": random.uniform(-self.width, self.width),
                "y": random.uniform(-self.height, self.height),
                "speed": random.uniform(0.01, 0.1),
            }
            for _ in range(self.startCount)
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
            self.pico_graphics.set_pen(
                self.pico_graphics.create_pen(brightness, brightness, brightness)
            )
            self.pico_graphics.pixel(sx, sy)

    async def update(self):
        self.pico_graphics.set_pen(self.pico_graphics.create_pen(0, 0, 0))
        self.pico_graphics.clear()

        for star in self.stars:
            await self.update_star(star)

        self.galactic_unicorn.update(self.pico_graphics)


async def run(
    galactic_unicorn, options_service, pico_graphics, sound_service, wifi_service
):
    warp_speed = WarpSpeed(
        galactic_unicorn, options_service, pico_graphics, sound_service, wifi_service
    )

    while True:
        await warp_speed.update()
        await uasyncio.sleep(0.016)
