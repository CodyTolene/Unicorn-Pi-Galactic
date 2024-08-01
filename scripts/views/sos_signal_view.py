# Cody Tolene
# Apache License 2.0

import uasyncio
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY


class SOSSignal:
    def __init__(self, galacticUnicorn, graphics):
        self.galacticUnicorn = galacticUnicorn
        self.graphics = graphics
        self.white = graphics.create_pen(255, 255, 255)
        self.black = graphics.create_pen(0, 0, 0)

    async def draw_dot(self):
        self.graphics.set_pen(self.white)
        self.graphics.clear()
        self.galacticUnicorn.update(self.graphics)
        await uasyncio.sleep(0.3)
        self.graphics.set_pen(self.black)
        self.graphics.clear()
        self.galacticUnicorn.update(self.graphics)
        await uasyncio.sleep(0.3)

    async def draw_dash(self):
        self.graphics.set_pen(self.white)
        self.graphics.clear()
        self.galacticUnicorn.update(self.graphics)
        await uasyncio.sleep(0.9)
        self.graphics.set_pen(self.black)
        self.graphics.clear()
        self.galacticUnicorn.update(self.graphics)
        await uasyncio.sleep(0.3)

    async def draw_s(self):
        for _ in range(3):
            await self.draw_dot()
        await uasyncio.sleep(0.3)

    async def draw_o(self):
        for _ in range(3):
            await self.draw_dash()
        await uasyncio.sleep(0.3)

    async def update(self):
        await self.draw_s()
        await self.draw_o()
        await self.draw_s()
        await uasyncio.sleep(1.5)


async def run(galacticUnicorn, graphics):
    sos_signal = SOSSignal(galacticUnicorn, graphics)

    while True:
        await sos_signal.update()


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
