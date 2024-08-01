# Cody Tolene
# Apache License 2.0

import random
import uasyncio
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY


class DigitalRain:
    def __init__(self, galacticUnicorn, graphics):
        self.galacticUnicorn = galacticUnicorn
        self.graphics = graphics
        self.width = galacticUnicorn.WIDTH
        self.height = galacticUnicorn.HEIGHT
        self.dots = []

    def clear(self):
        self.graphics.set_pen(self.graphics.create_pen(0, 0, 0))
        self.graphics.clear()

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
        color = random.choice(GREEN_VARIATIONS)
        return self.create_dot(x, 0, color)

    def draw_dots(self):
        for dot in self.dots:
            if 0 <= dot["x"] < self.width and 0 <= dot["y"] < self.height:
                self.graphics.set_pen(self.graphics.create_pen(*dot["color"]))
                self.graphics.pixel(dot["x"], dot["y"])

    async def update(self):
        self.clear()
        if len(self.dots) < MAX_DOTS and random.random() < 0.85:
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
        self.galacticUnicorn.update(self.graphics)


async def run(galacticUnicorn, graphics):
    digital_rain = DigitalRain(galacticUnicorn, graphics)

    while True:
        await digital_rain.update()
        await uasyncio.sleep(0.1)


MAX_DOTS = 50
BRIGHT_GREEN = (0, 255, 0)
MEDIUM_GREEN = (0, 128, 0)
DARK_GREEN = (0, 64, 0)
GREEN_VARIATIONS = [BRIGHT_GREEN, MEDIUM_GREEN, DARK_GREEN]

# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
