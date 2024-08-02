# Cody Tolene
# Apache License 2.0

import uasyncio
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY


class FlashlightTorch:
    def __init__(self, galacticUnicorn, graphics, sound):
        self.galacticUnicorn = galacticUnicorn
        self.graphics = graphics
        self.sound = sound
        self.white = graphics.create_pen(255, 255, 255)

    async def update(self):
        self.graphics.set_pen(self.white)
        self.graphics.clear()
        self.galacticUnicorn.update(self.graphics)


async def run(galacticUnicorn, graphics, sound):
    flashlight_torch = FlashlightTorch(galacticUnicorn, graphics, sound)

    while True:
        await flashlight_torch.update()
        await uasyncio.sleep(0.1)


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
