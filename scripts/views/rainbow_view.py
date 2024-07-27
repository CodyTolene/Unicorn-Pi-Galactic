# MIT License
# https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/examples/pico_unicorn/rainbow.py

import uasyncio
import math
from galactic import GalacticUnicorn


async def run(galacticUnicorn, graphics):
    width = galacticUnicorn.WIDTH
    # height = galacticUnicorn.HEIGHT

    hue_offset = 0.0
    stripe_width = 3.0
    speed = 1.0
    animate = True
    phase = 0

    hue_map = [from_hsv(x / width, 1.0, 1.0) for x in range(width)]

    while True:
        if animate:
            phase += speed

        draw(graphics, hue_map, hue_offset, phase, stripe_width, galacticUnicorn)

        # Handle button presses for view-specific controls
        if galacticUnicorn.is_pressed(GalacticUnicorn.SWITCH_VOLUME_UP):
            hue_offset += 0.01
            hue_offset = 1.0 if hue_offset > 1.0 else hue_offset

        if galacticUnicorn.is_pressed(GalacticUnicorn.SWITCH_VOLUME_DOWN):
            hue_offset -= 0.01
            hue_offset = 0.0 if hue_offset < 0.0 else hue_offset

        if galacticUnicorn.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_UP):
            galacticUnicorn.adjust_brightness(+0.01)

        if galacticUnicorn.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_DOWN):
            galacticUnicorn.adjust_brightness(-0.01)

        if galacticUnicorn.is_pressed(GalacticUnicorn.SWITCH_SLEEP):
            animate = False

        if galacticUnicorn.is_pressed(GalacticUnicorn.SWITCH_A):
            speed += 0.05
            speed = 10.0 if speed > 10.0 else speed
            animate = True

        if galacticUnicorn.is_pressed(GalacticUnicorn.SWITCH_B):
            speed -= 0.05
            speed = 0.0 if speed < 0.0 else speed
            animate = True

        if galacticUnicorn.is_pressed(GalacticUnicorn.SWITCH_C):
            stripe_width += 0.05
            stripe_width = 10.0 if stripe_width > 10.0 else stripe_width

        if galacticUnicorn.is_pressed(GalacticUnicorn.SWITCH_D):
            stripe_width -= 0.05
            stripe_width = 1.0 if stripe_width < 1.0 else stripe_width

        await uasyncio.sleep(1.0 / 60)


def from_hsv(h, s, v):
    i = math.floor(h * 6.0)
    f = h * 6.0 - i
    v *= 255.0
    p = v * (1.0 - s)
    q = v * (1.0 - f * s)
    t = v * (1.0 - (1.0 - f) * s)

    i = int(i) % 6
    if i == 0:
        return int(v), int(t), int(p)
    if i == 1:
        return int(q), int(v), int(p)
    if i == 2:
        return int(p), int(v), int(t)
    if i == 3:
        return int(p), int(q), int(v)
    if i == 4:
        return int(t), int(p), int(v)
    if i == 5:
        return int(v), int(p), int(q)


def draw(graphics, hue_map, hue_offset, phase, stripe_width, galacticUnicorn):
    width = galacticUnicorn.WIDTH
    height = galacticUnicorn.HEIGHT
    phase_percent = phase / 15

    for x in range(width):
        colour = hue_map[int((x + (hue_offset * width)) % width)]
        for y in range(height):
            v = (math.sin((x + y) / stripe_width + phase_percent) + 1.5) / 2.5
            graphics.set_pen(
                graphics.create_pen(
                    int(colour[0] * v), int(colour[1] * v), int(colour[2] * v)
                )
            )
            graphics.pixel(x, y)

    galacticUnicorn.update(graphics)


# This section of code is only for testing.
if __name__ == "__main__":
    from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY

    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
