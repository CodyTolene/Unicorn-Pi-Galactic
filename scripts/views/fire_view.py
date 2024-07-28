# Cody Tolene
# MIT License
# https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/examples/pico_unicorn/vertical-fire.py

import random
import micropython
import uasyncio
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY


async def run(galacticUnicorn, graphics):
    fire_colours = [
        graphics.create_pen(0, 0, 0),
        graphics.create_pen(20, 20, 20),
        graphics.create_pen(180, 30, 0),
        graphics.create_pen(220, 160, 0),
        graphics.create_pen(255, 255, 180),
    ]

    width = galacticUnicorn.HEIGHT + 2
    height = galacticUnicorn.WIDTH + 4
    heat = [[0.0 for y in range(height)] for x in range(width)]
    base_damping_factor = 0.97
    fire_spawns = 1

    @micropython.native
    def update():
        _heat = heat

        for x in range(width):
            _heat[x][height - 1] = 0.0
            _heat[x][height - 2] = 0.0

        for c in range(fire_spawns):
            x = random.randint(width // 2 - 1, width // 2 + 1)
            _heat[x][height - 1] = 1.0
            _heat[x + 1][height - 1] = 1.0
            _heat[x - 1][height - 1] = 1.0
            _heat[x][height - 2] = 1.0
            _heat[x + 1][height - 2] = 1.0
            _heat[x - 1][height - 2] = 1.0

        damping_factor = base_damping_factor + random.uniform(-0.02, 0.02)
        factor = damping_factor / 5.0
        for y in range(height - 3, -1, -1):
            for x in range(1, width - 1):
                sum_heat_y1 = _heat[x][y + 1]
                sum_heat_y2 = _heat[x][y + 2]
                sum_heat_x1y1 = _heat[x - 1][y + 1]
                sum_heat_x2y1 = _heat[x + 1][y + 1]

                _heat[x][y] += sum_heat_y1 + sum_heat_y2 + sum_heat_x1y1 + sum_heat_x2y1
                _heat[x][y] *= factor

    @micropython.native
    def draw():
        _graphics = graphics
        _heat = heat
        _set_pen = graphics.set_pen
        _pixel = graphics.pixel
        _fire_colours = fire_colours

        for y in range(galacticUnicorn.WIDTH):
            for x in range(galacticUnicorn.HEIGHT):
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
                _pixel(y, galacticUnicorn.HEIGHT - x - 1)

        galacticUnicorn.update(_graphics)

    while True:
        update()
        draw()
        await uasyncio.sleep(1.0 / 60)


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
