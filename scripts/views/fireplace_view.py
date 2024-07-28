# Cody Tolene
# Apache License 2.0

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

    width = galacticUnicorn.WIDTH
    height = galacticUnicorn.HEIGHT + 2

    heat = [[0.0 for y in range(height)] for x in range(width)]
    damping_factor = 0.80  # Increased damping factor to reduce flame height

    @micropython.native  # noqa: F821
    def update():
        _heat = heat

        # Clear the bottom rows and then add new fire seeds to them
        for x in range(width):
            _heat[x][height - 1] = random.uniform(0.3, 0.6)  # Lower initial intensity
            _heat[x][height - 2] = random.uniform(0.3, 0.6)

        factor = damping_factor / 5.0
        for y in range(height - 3, -1, -1):  # Ensure y doesn't go out of bounds
            for x in range(1, width - 1):
                sum_heat_y = _heat[x][y]
                sum_heat_y1 = _heat[x][y + 1]
                sum_heat_y2 = _heat[x][y + 2]
                sum_heat_x1y1 = _heat[x - 1][y + 1]
                sum_heat_x2y1 = _heat[x + 1][y + 1]

                sum_heat_y = sum_heat_y + sum_heat_y1 + sum_heat_y2
                sum_heat_x = sum_heat_x1y1 + sum_heat_x2y1

                sum_heat = sum_heat_y + sum_heat_x

                _heat[x][y] = sum_heat * factor

    @micropython.native  # noqa: F821
    def draw():
        _graphics = graphics
        _heat = heat
        _set_pen = graphics.set_pen
        _pixel = graphics.pixel
        _fire_colours = fire_colours

        for y in range(galacticUnicorn.HEIGHT):
            for x in range(galacticUnicorn.WIDTH):
                value = _heat[x][y + 2]  # Adjust indexing to stay within bounds
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

        galacticUnicorn.update(_graphics)

    while True:
        update()
        draw()
        await uasyncio.sleep(1.0 / 10)


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
