# Cody Tolene
# Apache License 2.0

import uasyncio
import time


class DigitalClock24:
    def __init__(
        self,
        galactic_unicorn,
        options_service,
        pico_graphics,
        sound_service,
        wifi_service,
    ):
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
        self.galactic_unicorn = galactic_unicorn
        self.options_service = options_service
        self.pico_graphics = pico_graphics
        self.pico_graphics.set_font("bitmap8")
        self.height = galactic_unicorn.HEIGHT
        self.sound_service = sound_service
        self.width = galactic_unicorn.WIDTH
        self.wifi_service = wifi_service

    def on_button_press(self):
        if self.galactic_unicorn.is_pressed(self.galactic_unicorn.SWITCH_C):
            if not self.button_states["C"]:
                self.button_states["C"] = True
                # Cycle to the previous color
                self.color_index = (self.color_index - 1) % len(self.colors)
        else:
            self.button_states["C"] = False

        if self.galactic_unicorn.is_pressed(self.galactic_unicorn.SWITCH_D):
            if not self.button_states["D"]:
                self.button_states["D"] = True
                # Cycle to the next color
                self.color_index = (self.color_index + 1) % len(self.colors)
        else:
            self.button_states["D"] = False

    async def update(self):
        self.on_button_press()
        self.pico_graphics.set_pen(0)
        self.pico_graphics.clear()

        # Time string
        current_time = time.localtime()
        hour = current_time[3]
        minute = current_time[4]
        second = current_time[5]
        time_str = "{:02}:{:02}:{:02}".format(hour, minute, second)

        # Color
        current_color = self.colors[self.color_index]
        self.pico_graphics.set_pen(self.pico_graphics.create_pen(*current_color))

        # Scale
        max_text_width = self.pico_graphics.measure_text(time_str, 1)
        max_text_height = 6  # Height of the font
        scale_x = self.width // max_text_width
        scale_y = self.height // max_text_height
        scale = min(scale_x, scale_y)

        # Text position
        text_width = self.pico_graphics.measure_text(time_str, scale)
        x = (self.width - text_width) // 2  # Center the text horizontally
        y = (self.height - max_text_height * scale) // 2  # Center the text vertically

        # Display
        self.pico_graphics.text(time_str, x, y, scale=scale)
        self.galactic_unicorn.update(self.pico_graphics)


async def run(
    galactic_unicorn, options_service, pico_graphics, sound_service, wifi_service
):
    digital_clock_24 = DigitalClock24(
        galactic_unicorn, options_service, pico_graphics, sound_service, wifi_service
    )

    while True:
        await digital_clock_24.update()
        await uasyncio.sleep(0.1)
