# Cody Tolene
# Apache License 2.0

import uasyncio
import time
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY


async def run(galacticUnicorn, graphics):
    width = galacticUnicorn.WIDTH
    height = galacticUnicorn.HEIGHT

    # Brightness and color settings
    brightness_levels = [0.3, 0.6, 1.0]
    colors = [
        (255, 255, 255),  # White
        (255, 0, 0),  # Red
        (0, 255, 0),  # Green
        (0, 0, 255),  # Blue
        (255, 255, 0),  # Yellow
        (0, 255, 255),  # Light Blue
        (255, 0, 255),  # Pink
    ]
    brightness_index = 1
    color_index = 0

    # Set a monospaced font
    graphics.set_font("bitmap8")

    while True:
        graphics.set_pen(0)
        graphics.clear()

        current_time = time.localtime()
        time_str = "{:02}:{:02}:{:02}".format(
            current_time[3],  # Hour
            current_time[4],  # Minute
            current_time[5],  # Seconds
        )

        current_color = colors[color_index]  # Todo make dynamic
        brightness = brightness_levels[brightness_index]
        adjusted_color = tuple(int(c * brightness) for c in current_color)

        graphics.set_pen(graphics.create_pen(*adjusted_color))

        max_text_width = graphics.measure_text(time_str, 1)
        max_text_height = 6  # Height of the font
        scale_x = width // max_text_width
        scale_y = height // max_text_height
        scale = min(scale_x, scale_y)

        # Center the text horizontally and vertically
        text_width = graphics.measure_text(time_str, scale)
        x = (width - text_width) // 2
        y = (height - max_text_height * scale) // 2

        graphics.text(time_str, x, y, scale=scale)
        galacticUnicorn.update(graphics)

        await uasyncio.sleep(0.5)


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
