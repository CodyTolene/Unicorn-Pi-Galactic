# Cody Tolene
# MIT License
# https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/examples/pico_unicorn/vertical-fire.py

import random
import micropython
import uasyncio


class Fire:
    def __init__(
        self,
        galactic_unicorn,
        options_service,
        pico_graphics,
        sound_service,
        wifi_service,
    ):
        self.base_damping_factor = 0.97
        self.fire_colours = [
            pico_graphics.create_pen(0, 0, 0),
            pico_graphics.create_pen(20, 20, 20),
            pico_graphics.create_pen(180, 30, 0),
            pico_graphics.create_pen(220, 160, 0),
            pico_graphics.create_pen(255, 255, 180),
        ]
        self.fire_spawns = 1
        self.galactic_unicorn = galactic_unicorn
        self.options_service = options_service
        self.pico_graphics = pico_graphics
        self.height = galactic_unicorn.WIDTH + 4
        self.sound_service = sound_service
        self.width = galactic_unicorn.HEIGHT + 2
        self.wifi_service = wifi_service

        self.heat = [[0.0 for _ in range(self.height)] for _ in range(self.width)]

    @micropython.native
    async def update(self):
        _heat = self.heat

        for x in range(self.width):
            _heat[x][self.height - 1] = 0.0
            _heat[x][self.height - 2] = 0.0

        for _ in range(self.fire_spawns):
            x = random.randint(self.width // 2 - 1, self.width // 2 + 1)
            _heat[x][self.height - 1] = 1.0
            _heat[x + 1][self.height - 1] = 1.0
            _heat[x - 1][self.height - 1] = 1.0
            _heat[x][self.height - 2] = 1.0
            _heat[x + 1][self.height - 2] = 1.0
            _heat[x - 1][self.height - 2] = 1.0

        damping_factor = self.base_damping_factor + random.uniform(-0.02, 0.02)
        factor = damping_factor / 5.0
        for y in range(self.height - 3, -1, -1):
            for x in range(1, self.width - 1):
                sum_heat_y1 = _heat[x][y + 1]
                sum_heat_y2 = _heat[x][y + 2]
                sum_heat_x1y1 = _heat[x - 1][y + 1]
                sum_heat_x2y1 = _heat[x + 1][y + 1]

                _heat[x][y] += sum_heat_y1 + sum_heat_y2 + sum_heat_x1y1 + sum_heat_x2y1
                _heat[x][y] *= factor

        _graphics = self.pico_graphics
        _set_pen = self.pico_graphics.set_pen
        _pixel = self.pico_graphics.pixel
        _fire_colours = self.fire_colours

        for y in range(self.galactic_unicorn.WIDTH):
            for x in range(self.galactic_unicorn.HEIGHT):
                value = _heat[x + 1][y + 1]
                if value < 0.15:
                    _set_pen(_fire_colours[0])
                elif value < 0.25:
                    _set_pen(_fire_colours[1])
                elif value < 0.35:
                    _set_pen(_fire_colours[2])
                elif value < 0.45:
                    _set_pen(_fire_colours[3])
                else:
                    _set_pen(_fire_colours[4])
                _pixel(y, self.galactic_unicorn.HEIGHT - x - 1)

        self.galactic_unicorn.update(_graphics)


async def run(
    galactic_unicorn, options_service, pico_graphics, sound_service, wifi_service
):
    fire = Fire(
        galactic_unicorn, options_service, pico_graphics, sound_service, wifi_service
    )

    while True:
        await fire.update()
        await uasyncio.sleep(1.0 / 60)
