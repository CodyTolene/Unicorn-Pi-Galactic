# Cody Tolene
# Apache License 2.0

import random
import uasyncio


class DigitalRain:
    def __init__(
        self,
        galactic_unicorn,
        options_service,
        pico_graphics,
        sound_service,
        wifi_service,
    ):
        self.dots = []
        self.galactic_unicorn = galactic_unicorn
        self.pico_graphics = pico_graphics
        self.height = galactic_unicorn.HEIGHT
        self.options_service = options_service
        self.sound_service = sound_service
        self.width = galactic_unicorn.WIDTH
        self.wifi_service = wifi_service

        self.MAX_DOTS = 50
        BRIGHT_GREEN = (0, 255, 0)
        MEDIUM_GREEN = (0, 128, 0)
        DARK_GREEN = (0, 64, 0)
        self.GREEN_VARIATIONS = [BRIGHT_GREEN, MEDIUM_GREEN, DARK_GREEN]

    def clear(self):
        self.pico_graphics.set_pen(self.pico_graphics.create_pen(0, 0, 0))
        self.pico_graphics.clear()

    def create_dot(self, x, y, color, stopping=False):
        return {"x": x, "y": y, "color": color, "stopping": stopping}

    def move_dot(self, dot):
        if dot["stopping"] or (dot["y"] < self.height - 1 and random.random() < 0.1):
            dot["stopping"] = True
            dot["color"] = self.dim_color(dot["color"], 0.9)
        else:
            dot["y"] += 1

    def dim_color(self, color, factor):
        return tuple(max(0, int(c * factor)) for c in color)

    def is_faded_out(self, dot):
        return dot["color"] == (0, 0, 0)

    def create_random_dot(self):
        x = random.randint(0, self.width - 1)
        color = random.choice(self.GREEN_VARIATIONS)
        return self.create_dot(x, 0, color)

    def draw_dots(self):
        for dot in self.dots:
            if 0 <= dot["x"] < self.width and 0 <= dot["y"] < self.height:
                self.pico_graphics.set_pen(self.pico_graphics.create_pen(*dot["color"]))
                self.pico_graphics.pixel(dot["x"], dot["y"])

    async def update(self):
        self.clear()
        if len(self.dots) < self.MAX_DOTS and random.random() < 0.85:
            new_dot = self.create_random_dot()
            self.dots.append(new_dot)

        for dot in self.dots:
            self.move_dot(dot)

        self.dots = [
            dot
            for dot in self.dots
            if dot["y"] < self.height and not self.is_faded_out(dot)
        ]
        self.draw_dots()
        self.galactic_unicorn.update(self.pico_graphics)


async def run(
    galactic_unicorn, options_service, pico_graphics, sound_service, wifi_service
):
    digital_rain = DigitalRain(
        galactic_unicorn, options_service, pico_graphics, sound_service, wifi_service
    )

    while True:
        await digital_rain.update()
        await uasyncio.sleep(0.1)
