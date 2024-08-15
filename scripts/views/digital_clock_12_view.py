# Cody Tolene
# Apache License 2.0

import uasyncio
import urequests
from time import localtime

from utils.options_service import OptionKeys


class DigitalClock12:
    def __init__(
        self,
        galactic_unicorn,
        options_service,
        pico_graphics,
        sound_service,
        wifi_service,
    ):
        self.colors = [
            (255, 255, 255),  # White
            (255, 0, 0),  # Red
            (0, 255, 0),  # Green
            (0, 0, 255),  # Blue
            (255, 255, 0),  # Yellow
            (0, 255, 255),  # Light Blue
            (255, 0, 255),  # Pink
        ]
        self.button_states = {"C": False, "D": False}
        self.color_index = 0  # Start with white
        self.galactic_unicorn = galactic_unicorn
        self.options_service = options_service
        self.pico_graphics = pico_graphics
        self.pico_graphics.set_font("bitmap8")
        self.sound_service = sound_service
        self.height = galactic_unicorn.HEIGHT
        self.width = galactic_unicorn.WIDTH
        self.wifi_service = wifi_service

        # Initialize hour, minute, second, and AM/PM
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.am_pm = "AM"  # Default to AM

        # Set the time zone, default to Central Time (CST/CDT)
        self.time_zone = options_service.get_option(
            OptionKeys.TIME_ZONE, "America/Chicago"
        )
        self.display_message("Loading")
        self.fetch_internet_time()

    def display_message(self, message):
        self.pico_graphics.set_pen(0)
        self.pico_graphics.clear()

        current_color = self.colors[self.color_index]
        self.pico_graphics.set_pen(self.pico_graphics.create_pen(*current_color))

        text_width = self.pico_graphics.measure_text(message, 1)
        x = (self.width - text_width) // 2
        y = (self.height - 8) // 2  # Assuming text height is 8 pixels

        self.pico_graphics.text(message, x, y, scale=1)
        self.galactic_unicorn.update(self.pico_graphics)

    def fetch_internet_time(self):
        if not self.wifi_service.is_connected():
            print("No Wi-Fi available.")
            self.fallback_to_local_time()
            return

        try:
            url = f"http://worldtimeapi.org/api/timezone/{self.time_zone}"
            response = urequests.get(url)
            data = response.json()

            # Use the 'datetime' field directly from the API
            datetime_str = data["datetime"][
                :19
            ]  # Extract datetime string in the format "YYYY-MM-DDTHH:MM:SS"

            # year = int(datetime_str[:4])
            # month = int(datetime_str[5:7])
            # day = int(datetime_str[8:10])

            # Parse the time string
            hour = int(datetime_str[11:13])
            minute = int(datetime_str[14:16])
            second = int(datetime_str[17:19])

            # Handle AM/PM conversion
            self.am_pm = "AM" if hour < 12 else "PM"
            hour = hour % 12
            if hour == 0:
                hour = 12

            # Set the hour, minute, and second
            self.hour = hour
            self.minute = minute
            self.second = second

            response.close()

        except Exception as e:
            print(f"Error fetching time: {e}")
            self.fallback_to_local_time()

    def fallback_to_local_time(self):
        current_time = localtime()
        hour_24 = current_time[3]  # Hours in 24-hour format
        self.minute = current_time[4]  # Minutes
        self.second = current_time[5]  # Seconds

        # Convert 24-hour format to 12-hour format and set AM/PM
        self.am_pm = "AM" if hour_24 < 12 else "PM"
        self.hour = hour_24 % 12
        if self.hour == 0:
            self.hour = 12  # Midnight or Noon is represented as 12

    def adjust_time(self, direction):
        # Reset seconds to zero on time adjustment
        self.second = 0

        if direction == "up":
            self.minute += 1
            if self.minute > 59:
                self.minute = 0
                self.hour += 1

                # Toggle AM/PM if we pass 11:59 AM or PM
                if self.hour == 12 and self.minute == 0:
                    self.am_pm = "AM" if self.am_pm == "PM" else "PM"
                elif self.hour > 12:
                    self.hour = 1

        elif direction == "down":
            self.minute -= 1
            if self.minute < 0:
                self.minute = 59
                self.hour -= 1

            # Ensure hour stays within 1-12 for 12-hour format
            if self.hour < 1:
                self.hour = 12
                # Toggle AM/PM when rolling back from 1:00 AM to 12:59 PM or vice versa
                self.am_pm = "AM" if self.am_pm == "PM" else "PM"

            # Check the transition from 12:00 AM to 11:59 PM correctly
            if self.hour == 11 and self.minute == 59:
                self.am_pm = "AM" if self.am_pm == "PM" else "PM"

    async def handle_button_presses(self):
        while True:
            # Handle color cycling buttons
            if self.galactic_unicorn.is_pressed(self.galactic_unicorn.SWITCH_C):
                if not self.button_states["C"]:
                    self.button_states["C"] = True
                    self.color_index = (self.color_index - 1) % len(self.colors)
            else:
                self.button_states["C"] = False

            if self.galactic_unicorn.is_pressed(self.galactic_unicorn.SWITCH_D):
                if not self.button_states["D"]:
                    self.button_states["D"] = True
                    self.color_index = (self.color_index + 1) % len(self.colors)
            else:
                self.button_states["D"] = False

            # Handle volume buttons for time adjustment
            if self.galactic_unicorn.is_pressed(self.galactic_unicorn.SWITCH_VOLUME_UP):
                self.adjust_time("up")

            if self.galactic_unicorn.is_pressed(
                self.galactic_unicorn.SWITCH_VOLUME_DOWN
            ):
                self.adjust_time("down")

            await uasyncio.sleep(0.1)  # Check button presses every 100ms

    async def update_clock(self):
        while True:
            self.second += 1
            if self.second > 59:
                self.second = 0
                self.minute += 1
            if self.minute > 59:
                self.minute = 0
                self.hour += 1

                # Check if it's time to toggle AM/PM
                if self.hour == 12:
                    self.am_pm = "AM" if self.am_pm == "PM" else "PM"

            # Ensure the hour stays within 12-hour bounds
            if self.hour > 12:
                self.hour = 1

            await self.update_display()
            await uasyncio.sleep(1)  # Clock ticks every second

    async def update_display(self):
        self.pico_graphics.set_pen(0)
        self.pico_graphics.clear()

        # Time string
        time_str = "{:02}:{:02}:{:02} {}".format(
            self.hour, self.minute, self.second, self.am_pm
        )

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

    async def run(self):
        # Run clock and button handling concurrently
        await uasyncio.gather(self.update_clock(), self.handle_button_presses())


async def run(
    galactic_unicorn, options_service, pico_graphics, sound_service, wifi_service
):
    digital_clock_12 = DigitalClock12(
        galactic_unicorn, options_service, pico_graphics, sound_service, wifi_service
    )

    # Start clock and button handling
    await digital_clock_12.run()
