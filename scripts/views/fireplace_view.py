# Cody Tolene
# Apache License 2.0

import random
import uasyncio

from utils.sounds import FireplaceSound


class Fireplace:
    def __init__(self, graphics, galacticUnicorn, sound_service):
        self.galacticUnicorn = galacticUnicorn
        self.graphics = graphics
        self.height = galacticUnicorn.HEIGHT + 2
        self.sound_service = FireplaceSound(galacticUnicorn, sound_service)
        self.width = galacticUnicorn.WIDTH

        self.fire_colours = [
            graphics.create_pen(0, 0, 0),
            graphics.create_pen(20, 20, 20),
            graphics.create_pen(180, 30, 0),
            graphics.create_pen(220, 160, 0),
            graphics.create_pen(255, 255, 180),
        ]
        self.heat = [[0.0 for _ in range(self.height)] for _ in range(self.width)]
        self.sound_service.play()

    async def update(self):
        _heat = self.heat
        _graphics = self.graphics
        _set_pen = self.graphics.set_pen
        _pixel = self.graphics.pixel
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

        for y in range(self.galacticUnicorn.HEIGHT):
            for x in range(self.galacticUnicorn.WIDTH):
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

        self.galacticUnicorn.update(_graphics)


async def run(galacticUnicorn, graphics, sound_service):
    fireplace = Fireplace(graphics, galacticUnicorn, sound_service)

    while True:
        await fireplace.update()
        await uasyncio.sleep(0.1)
