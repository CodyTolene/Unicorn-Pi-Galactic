# Cody Tolene
# Apache License 2.0

import uasyncio


class SOSSignal:
    def __init__(
        self,
        galactic_unicorn,
        options_service,
        pico_graphics,
        sound_service,
        wifi_service,
    ):
        self.black = pico_graphics.create_pen(0, 0, 0)
        self.galactic_unicorn = galactic_unicorn
        self.options_service = options_service
        self.pico_graphics = pico_graphics
        self.sound_service = sound_service
        self.white = pico_graphics.create_pen(255, 255, 255)
        self.wifi_service = wifi_service

    async def draw_dot(self):
        self.pico_graphics.set_pen(self.white)
        self.pico_graphics.clear()
        self.galactic_unicorn.update(self.pico_graphics)
        await uasyncio.sleep(0.3)
        self.pico_graphics.set_pen(self.black)
        self.pico_graphics.clear()
        self.galactic_unicorn.update(self.pico_graphics)
        await uasyncio.sleep(0.3)

    async def draw_dash(self):
        self.pico_graphics.set_pen(self.white)
        self.pico_graphics.clear()
        self.galactic_unicorn.update(self.pico_graphics)
        await uasyncio.sleep(0.9)
        self.pico_graphics.set_pen(self.black)
        self.pico_graphics.clear()
        self.galactic_unicorn.update(self.pico_graphics)
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


async def run(
    galactic_unicorn, options_service, pico_graphics, sound_service, wifi_service
):
    sos_signal = SOSSignal(
        galactic_unicorn, options_service, pico_graphics, sound_service, wifi_service
    )

    while True:
        await sos_signal.update()
