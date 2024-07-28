# Cody Tolene
# Apache License 2.0

import random
import uasyncio
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY

MAX_DOTS = 50


class Dot:
    def __init__(self, x, y, color, stopping):
        self.x = x
        self.y = y
        self.color = color
        self.stopping = stopping

    def move(self, height):
        if self.stopping or (self.y < height - 1 and random.random() < 0.1):
            self.stopping = True
            self.color = self.dim_color(0.9)
        else:
            self.y += 1

    def dim_color(self, factor):
        return tuple(max(0, int(c * factor)) for c in self.color)

    def is_faded_out(self):
        return self.color == (0, 0, 0)


async def run(galacticUnicorn, graphics):
    width = galacticUnicorn.WIDTH
    height = galacticUnicorn.HEIGHT

    BRIGHT_GREEN = (0, 255, 0)
    MEDIUM_GREEN = (0, 128, 0)
    DARK_GREEN = (0, 64, 0)
    GREEN_VARIATIONS = [BRIGHT_GREEN, MEDIUM_GREEN, DARK_GREEN]

    def clear():
        graphics.set_pen(graphics.create_pen(0, 0, 0))
        graphics.clear()

    def create_random_dot():
        x = random.randint(0, width - 1)
        color = random.choice(GREEN_VARIATIONS)
        return Dot(x, 0, color, False)

    def draw_dots(dots):
        for dot in dots:
            if 0 <= dot.x < width and 0 <= dot.y < height:
                graphics.set_pen(graphics.create_pen(*dot.color))
                graphics.pixel(dot.x, dot.y)

    dots = []
    while True:
        clear()
        if len(dots) < MAX_DOTS and random.random() < 0.85:
            new_dot = create_random_dot()
            dots.append(new_dot)

        for dot in dots:
            dot.move(height)

        dots = [dot for dot in dots if dot.y < height and not dot.is_faded_out()]
        draw_dots(dots)
        galacticUnicorn.update(graphics)

        # print(f"Active dots: {len(dots)}")

        await uasyncio.sleep(0.1)


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
