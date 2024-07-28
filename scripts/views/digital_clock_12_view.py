# Cody Tolene
# Apache License 2.0

import uasyncio
import time
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY


async def run(galacticUnicorn, graphics):
    width = galacticUnicorn.WIDTH
    height = galacticUnicorn.HEIGHT

    colors = [
        (255, 255, 255),  # White
        (255, 0, 0),  # Red
        (0, 255, 0),  # Green
        (0, 0, 255),  # Blue
        (255, 255, 0),  # Yellow
        (0, 255, 255),  # Light Blue
        (255, 0, 255),  # Pink
    ]
    color_index = 0  # Start with white

    # Set a monospaced font
    graphics.set_font("bitmap8")

    buttonStates = {
        "C": False,
        "D": False,
    }

    while True:
        if galacticUnicorn.is_pressed(galacticUnicorn.SWITCH_C):
            if not buttonStates["C"]:
                buttonStates["C"] = True
                # Cycle to the previous color
                color_index = (color_index - 1) % len(colors)
        else:
            buttonStates["C"] = False

        if galacticUnicorn.is_pressed(galacticUnicorn.SWITCH_D):
            if not buttonStates["D"]:
                buttonStates["D"] = True
                # Cycle to the next color
                color_index = (color_index + 1) % len(colors)
        else:
            buttonStates["D"] = False

        graphics.set_pen(0)
        graphics.clear()

        current_time = time.localtime()
        hour = current_time[3]
        minute = current_time[4]
        second = current_time[5]
        am_pm = "AM" if hour < 12 else "PM"
        hour = hour % 12
        if hour == 0:
            hour = 12

        time_str = "{:02}:{:02}:{:02} {}".format(
            hour, minute, second, am_pm  # Hour  # Minute  # Seconds  # AM/PM
        )

        # Adjust color
        current_color = colors[color_index]
        graphics.set_pen(graphics.create_pen(*current_color))

        # Calculate the maximum scale that fits both the width and height
        max_text_width = graphics.measure_text(time_str, 1)
        max_text_height = 6  # Height of the font
        scale_x = width // max_text_width
        scale_y = height // max_text_height
        scale = min(scale_x, scale_y)

        # Center the text
        text_width = graphics.measure_text(time_str, scale)
        x = (width - text_width) // 2  # Center the text horizontally
        y = (height - max_text_height * scale) // 2  # Center the text vertically

        # Display the left-aligned time centered on the display
        graphics.text(time_str, x, y, scale=scale)
        galacticUnicorn.update(graphics)

        await uasyncio.sleep(0.1)  # Adjust the speed of updating


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
