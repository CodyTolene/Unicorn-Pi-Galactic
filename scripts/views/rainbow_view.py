# Cody Tolene
# Apache License 2.0
#
# Contains code from here under the MIT License:
# https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/examples/galactic_unicorn

import uasyncio
import math

from galactic import GalacticUnicorn
from utils.sounds import ExampleMusic


class Rainbow:
    def __init__(self, galactic_unicorn, pico_graphics, sound_service):
        self.galactic_unicorn = galactic_unicorn
        self.pico_graphics = pico_graphics
        self.height = galactic_unicorn.HEIGHT
        self.hue_offset = 0.0
        self.sound_service = ExampleMusic(galactic_unicorn, sound_service)
        self.phase = 0
        self.speed = 1.0
        self.stripe_width = 3.0
        self.width = galactic_unicorn.WIDTH

        self.hue_map = [
            self.from_hsv(x / self.width, 1.0, 1.0) for x in range(self.width)
        ]
        self.sound_service.play()

    @staticmethod
    def from_hsv(h, s, v):
        i = math.floor(h * 6.0)
        f = h * 6.0 - i
        v *= 255.0
        p = v * (1.0 - s)
        q = v * (1.0 - f * s)
        t = v * (1.0 - (1.0 - f) * s)

        i = int(i) % 6
        if i == 0:
            return int(v), int(t), int(p)
        if i == 1:
            return int(q), int(v), int(p)
        if i == 2:
            return int(p), int(v), int(t)
        if i == 3:
            return int(p), int(q), int(v)
        if i == 4:
            return int(t), int(p), int(v)
        if i == 5:
            return int(v), int(p), int(q)

    def draw(self):
        phase_percent = self.phase / 15

        for x in range(self.width):
            colour = self.hue_map[
                int((x + (self.hue_offset * self.width)) % self.width)
            ]
            for y in range(self.height):
                v = (math.sin((x + y) / self.stripe_width + phase_percent) + 1.5) / 2.5
                self.pico_graphics.set_pen(
                    self.pico_graphics.create_pen(
                        int(colour[0] * v), int(colour[1] * v), int(colour[2] * v)
                    )
                )
                self.pico_graphics.pixel(x, y)

        self.galactic_unicorn.update(self.pico_graphics)

    def on_button_press(self):
        if self.galactic_unicorn.is_pressed(GalacticUnicorn.SWITCH_C):
            self.stripe_width += 0.05
            self.stripe_width = 10.0 if self.stripe_width > 10.0 else self.stripe_width
            # self.hue_offset += 0.01
            # self.hue_offset = 1.0 if self.hue_offset > 1.0 else self.hue_offset

        if self.galactic_unicorn.is_pressed(GalacticUnicorn.SWITCH_D):
            self.stripe_width -= 0.05
            self.stripe_width = 1.0 if self.stripe_width < 1.0 else self.stripe_width
            # self.hue_offset -= 0.01
            # self.hue_offset = 0.0 if self.hue_offset < 0.0 else self.hue_offset

    async def update(self):
        self.phase += self.speed
        self.pico_graphics.set_pen(0)
        self.pico_graphics.clear()
        self.draw()
        self.on_button_press()


async def run(galactic_unicorn, pico_graphics, sound_service):
    rainbow = Rainbow(galactic_unicorn, pico_graphics, sound_service)

    while True:
        await rainbow.update()
        await uasyncio.sleep(0.1)
