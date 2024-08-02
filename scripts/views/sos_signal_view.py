# Cody Tolene
# Apache License 2.0

import uasyncio


class SOSSignal:
    def __init__(self, galacticUnicorn, graphics, sound_service):
        self.black = graphics.create_pen(0, 0, 0)
        self.galacticUnicorn = galacticUnicorn
        self.graphics = graphics
        self.sound_service = sound_service
        self.white = graphics.create_pen(255, 255, 255)

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


async def run(galacticUnicorn, graphics, sound_service):
    sos_signal = SOSSignal(galacticUnicorn, graphics, sound_service)

    while True:
        await sos_signal.update()
