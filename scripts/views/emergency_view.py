# Cody Tolene
# Apache License 2.0

import uasyncio
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY


class Emergency:
    def __init__(self, galacticUnicorn, graphics):
        self.galacticUnicorn = galacticUnicorn
        self.graphics = graphics
        self.red = graphics.create_pen(255, 0, 0)
        self.blue = graphics.create_pen(0, 0, 255)
        self.current_color = self.red

    async def update(self):
        self.graphics.set_pen(self.current_color)
        self.graphics.clear()
        self.galacticUnicorn.update(self.graphics)
        self.current_color = self.blue if self.current_color == self.red else self.red


async def run(galacticUnicorn, graphics):
    emergency = Emergency(galacticUnicorn, graphics)

    while True:
        await emergency.update()
        await uasyncio.sleep(0.5)


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
