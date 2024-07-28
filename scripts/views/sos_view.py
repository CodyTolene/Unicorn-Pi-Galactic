# Cody Tolene
# Apache License 2.0

import uasyncio
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY


async def run(galacticUnicorn, graphics):
    white = graphics.create_pen(255, 255, 255)
    black = graphics.create_pen(0, 0, 0)

    async def draw_sos():
        # S: "· · ·"
        for _ in range(3):
            graphics.set_pen(white)
            graphics.clear()
            galacticUnicorn.update(graphics)
            await uasyncio.sleep(0.3)  # Dot duration
            graphics.set_pen(black)
            graphics.clear()
            galacticUnicorn.update(graphics)
            await uasyncio.sleep(0.3)  # Space between parts of the same letter

        await uasyncio.sleep(0.3)  # Space between letters

        # O: "− − −"
        for _ in range(3):
            graphics.set_pen(white)
            graphics.clear()
            galacticUnicorn.update(graphics)
            await uasyncio.sleep(0.9)  # Dash duration
            graphics.set_pen(black)
            graphics.clear()
            galacticUnicorn.update(graphics)
            await uasyncio.sleep(0.3)  # Space between parts of the same letter

        await uasyncio.sleep(0.3)  # Space between letters

        # S: "· · ·"
        for _ in range(3):
            graphics.set_pen(white)
            graphics.clear()
            galacticUnicorn.update(graphics)
            await uasyncio.sleep(0.3)  # Dot duration
            graphics.set_pen(black)
            graphics.clear()
            galacticUnicorn.update(graphics)
            await uasyncio.sleep(0.3)  # Space between parts of the same letter

    while True:
        await draw_sos()
        await uasyncio.sleep(1.5)  # Space between repetitions of SOS signal


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
