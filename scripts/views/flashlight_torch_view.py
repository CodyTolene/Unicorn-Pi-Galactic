# Cody Tolene
# Apache License 2.0

import uasyncio


class FlashlightTorch:
    def __init__(self, galactic_unicorn, pico_graphics, sound_service):
        self.galactic_unicorn = galactic_unicorn
        self.pico_graphics = pico_graphics
        self.sound_service = sound_service
        self.white = pico_graphics.create_pen(255, 255, 255)

    async def update(self):
        self.pico_graphics.set_pen(self.white)
        self.pico_graphics.clear()
        self.galactic_unicorn.update(self.pico_graphics)


async def run(galactic_unicorn, pico_graphics, sound_service):
    flashlight_torch = FlashlightTorch(galactic_unicorn, pico_graphics, sound_service)

    while True:
        await flashlight_torch.update()
        await uasyncio.sleep(0.1)
