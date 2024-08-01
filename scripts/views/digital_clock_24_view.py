# Cody Tolene
# Apache License 2.0

import uasyncio
import time
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY


class DigitalClock24:
    def __init__(self, galacticUnicorn, graphics, music):
        self.button_states = {"C": False, "D": False}
        self.color_index = 0  # Start with white
        self.colors = [
            (255, 255, 255),  # White
            (255, 0, 0),  # Red
            (0, 255, 0),  # Green
            (0, 0, 255),  # Blue
            (255, 255, 0),  # Yellow
            (0, 255, 255),  # Light Blue
            (255, 0, 255),  # Pink
        ]
        self.galacticUnicorn = galacticUnicorn
        self.graphics = graphics
        self.graphics.set_font("bitmap8")
        self.height = galacticUnicorn.HEIGHT
        self.music = music
        self.width = galacticUnicorn.WIDTH

    def on_button_press(self):
        if self.galacticUnicorn.is_pressed(self.galacticUnicorn.SWITCH_C):
            if not self.button_states["C"]:
                self.button_states["C"] = True
                # Cycle to the previous color
                self.color_index = (self.color_index - 1) % len(self.colors)
        else:
            self.button_states["C"] = False

        if self.galacticUnicorn.is_pressed(self.galacticUnicorn.SWITCH_D):
            if not self.button_states["D"]:
                self.button_states["D"] = True
                # Cycle to the next color
                self.color_index = (self.color_index + 1) % len(self.colors)
        else:
            self.button_states["D"] = False

    async def update(self):
        self.on_button_press()
        self.graphics.set_pen(0)
        self.graphics.clear()

        # Time string
        current_time = time.localtime()
        hour = current_time[3]
        minute = current_time[4]
        second = current_time[5]
        time_str = "{:02}:{:02}:{:02}".format(hour, minute, second)

        # Color
        current_color = self.colors[self.color_index]
        self.graphics.set_pen(self.graphics.create_pen(*current_color))

        # Scale
        max_text_width = self.graphics.measure_text(time_str, 1)
        max_text_height = 6  # Height of the font
        scale_x = self.width // max_text_width
        scale_y = self.height // max_text_height
        scale = min(scale_x, scale_y)

        # Text position
        text_width = self.graphics.measure_text(time_str, scale)
        x = (self.width - text_width) // 2  # Center the text horizontally
        y = (self.height - max_text_height * scale) // 2  # Center the text vertically

        # Display
        self.graphics.text(time_str, x, y, scale=scale)
        self.galacticUnicorn.update(self.graphics)


async def run(galacticUnicorn, graphics, music):
    digital_clock_24 = DigitalClock24(galacticUnicorn, graphics, music)

    while True:
        await digital_clock_24.update()
        await uasyncio.sleep(0.1)


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
