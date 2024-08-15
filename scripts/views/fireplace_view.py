# Cody Tolene
# Apache License 2.0

import random
import uasyncio

from utils.sounds import FireplaceSound


class Fireplace:
    def __init__(
        self,
        galactic_unicorn,
        options_service,
        pico_graphics,
        sound_service,
        wifi_service,
    ):
        self.galactic_unicorn = galactic_unicorn
        self.height = galactic_unicorn.HEIGHT + 2
        self.options_service = options_service
        self.pico_graphics = pico_graphics
        self.sound_service = FireplaceSound(galactic_unicorn, sound_service)
        self.width = galactic_unicorn.WIDTH

        self.fire_colours = [
            pico_graphics.create_pen(0, 0, 0),
            pico_graphics.create_pen(20, 20, 20),
            pico_graphics.create_pen(180, 30, 0),
            pico_graphics.create_pen(220, 160, 0),
            pico_graphics.create_pen(255, 255, 180),
        ]
        self.heat = [[0.0 for _ in range(self.height)] for _ in range(self.width)]
        self.sound_service.play()

    async def update(self):
        _heat = self.heat
        _graphics = self.pico_graphics
        _set_pen = self.pico_graphics.set_pen
        _pixel = self.pico_graphics.pixel
        _fire_colours = self.fire_colours

        for x in range(self.width):
            _heat[x][self.height - 1] = random.uniform(0.3, 0.6)
            _heat[x][self.height - 2] = random.uniform(0.3, 0.6)

        # Increase damping factor to reduce flame height
        factor = 0.16
        for y in range(self.height - 3, -1, -1):
            for x in range(1, self.width - 1):
                sum_heat_y = _heat[x][y]
                sum_heat_y1 = _heat[x][y + 1]
                sum_heat_y2 = _heat[x][y + 2]
                sum_heat_x1y1 = _heat[x - 1][y + 1]
                sum_heat_x2y1 = _heat[x + 1][y + 1]

                sum_heat_y = sum_heat_y + sum_heat_y1 + sum_heat_y2
                sum_heat_x = sum_heat_x1y1 + sum_heat_x2y1

                sum_heat = sum_heat_y + sum_heat_x

                _heat[x][y] = sum_heat * factor

        for y in range(self.galactic_unicorn.HEIGHT):
            for x in range(self.galactic_unicorn.WIDTH):
                value = _heat[x][y + 2]
                if value < 0.15:
                    _set_pen(_fire_colours[0])
                elif value < 0.3:
                    _set_pen(_fire_colours[1])
                elif value < 0.45:
                    _set_pen(_fire_colours[2])
                elif value < 0.6:
                    _set_pen(_fire_colours[3])
                else:
                    _set_pen(_fire_colours[4])
                _pixel(x, y)

        self.galactic_unicorn.update(_graphics)


async def run(
    galactic_unicorn, options_service, pico_graphics, sound_service, wifi_service
):
    fireplace = Fireplace(
        galactic_unicorn, options_service, pico_graphics, sound_service, wifi_service
    )

    while True:
        await fireplace.update()
        await uasyncio.sleep(0.1)
