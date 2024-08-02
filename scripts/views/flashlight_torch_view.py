# Cody Tolene
# Apache License 2.0

import uasyncio


class FlashlightTorch:
    def __init__(self, galacticUnicorn, graphics, sound_service):
        self.galacticUnicorn = galacticUnicorn
        self.graphics = graphics
        self.sound_service = sound_service
        self.white = graphics.create_pen(255, 255, 255)

    async def update(self):
        self.graphics.set_pen(self.white)
        self.graphics.clear()
        self.galacticUnicorn.update(self.graphics)


async def run(galacticUnicorn, graphics, sound_service):
    flashlight_torch = FlashlightTorch(galacticUnicorn, graphics, sound_service)

    while True:
        await flashlight_torch.update()
        await uasyncio.sleep(0.1)
