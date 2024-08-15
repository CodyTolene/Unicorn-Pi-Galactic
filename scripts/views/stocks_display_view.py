# Cody Tolene
# Apache License 2.0

import uasyncio
import urequests
import gc

from utils.options_service import OptionKeys


class StocksDisplay:
    def __init__(
        self,
        galactic_unicorn,
        options_service,
        pico_graphics,
        sound_service,
        wifi_service,
    ):
        self.api_key = options_service.get_option(OptionKeys.STOCKS_FINNHUB_API_KEY)
        self.button_states = {"C": False, "D": False}
        self.color_index = 0
        self.colors = [
            (0, 255, 0),  # Green
            (255, 255, 255),  # White
            (255, 0, 0),  # Red
            (0, 0, 255),  # Blue
            (255, 255, 0),  # Yellow
            (0, 255, 255),  # Light Blue
            (255, 0, 255),  # Pink
        ]
        self.galactic_unicorn = galactic_unicorn
        self.height = galactic_unicorn.HEIGHT
        self.width = galactic_unicorn.WIDTH
        self.options_service = options_service
        self.pico_graphics = pico_graphics
        self.pico_graphics.set_font("bitmap6")
        self.sound_service = sound_service
        self.stock_data = {}
        self.wifi_service = wifi_service

        self.stocks_update_message = options_service.get_option(
            OptionKeys.STOCKS_UPDATE_MESSAGE, True
        )
        self.stocks_scroll_speed = options_service.get_option(
            OptionKeys.STOCKS_SCROLL_SPEED, 0.5
        )
        self.stocks_symbols = options_service.get_option(OptionKeys.STOCKS_SYMBOLS, [])
        self.text_position_x = self.width

        text_height_px = 5.0
        self.text_position_y = int(self.height / text_height_px)
        self.full_text_width = 0

        # Set to 1.0 = 5 pixels, 2.0 = 11 pixels
        # Notice: No other sizes seem to be supported.
        # See: https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/modules/picographics/README.md#text
        self.text_scale = 1.0 if text_height_px == 5 else 2.0

        # New variable for controlling update frequency
        self.update_after_x_scrolls = options_service.get_option(
            OptionKeys.STOCKS_UPDATE_AFTER_X_SCROLLS, 3
        )
        self.scroll_counter = 0

    def fetch_stock_data(self):
        if not self.api_key:
            print("API key is missing.")
            return None  # Return None to indicate no data due to missing API key

        # Clear the existing stock data before fetching
        self.stock_data.clear()

        for symbol in self.stocks_symbols:
            try:
                url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={self.api_key}"
                response = urequests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    self.stock_data[symbol] = data.get("c", "N/A")  # Current price
                else:
                    error_status_code_message = "Error: " + str(response.status_code)
                    print(error_status_code_message)
                    self.display_message(error_status_code_message)
                    return None

                response.close()
                gc.collect()  # Collect garbage after each response

            except Exception as e:
                print(f"Error fetching data for {symbol}: {e}")
                self.stock_data[symbol] = "Error"

        gc.collect()  # Additional garbage collection to free memory
        return self.stock_data

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

    async def update_display(self):
        running = True
        while running:
            self.on_button_press()
            self.pico_graphics.set_pen(0)
            self.pico_graphics.clear()

            if not self.wifi_service.is_connected():
                self.display_message("No Wi-Fi")
                running = False
            elif not self.api_key:
                self.display_message("No API Key")
                running = False
            else:
                if not self.stock_data:
                    self.display_message("Loading")
                    self.galactic_unicorn.update(self.pico_graphics)
                    self.stock_data = self.fetch_stock_data()

                if self.stock_data:
                    self.display_stock_data()
                else:
                    # Error fetching results, halt
                    running = False

            self.galactic_unicorn.update(self.pico_graphics)

            # Default scroll speed is moving 1 pixel every 0.1 seconds
            base_scroll_time_per_pixel = 0.1
            # Calculate an adjustment factor based on the user's scroll speed
            adjustment_factor = 0.25 / self.stocks_scroll_speed
            # Apply the adjustment factor to the base scroll time
            scroll_speed = base_scroll_time_per_pixel * adjustment_factor
            # Sleep for the calculated time
            await uasyncio.sleep(scroll_speed)

            # Check if the text has fully scrolled off the screen
            if self.text_position_x < -self.full_text_width:
                self.scroll_counter += 1  # Increment scroll counter

                # Refresh the data only after X scrolls
                if self.scroll_counter >= self.update_after_x_scrolls:
                    if self.stocks_update_message:
                        self.display_message("Updating")
                        self.galactic_unicorn.update(self.pico_graphics)

                    self.stock_data = self.fetch_stock_data()

                    # If data was fetched successfully, reset the scroll counter
                    if self.stock_data:
                        self.scroll_counter = 0  # Reset scroll counter

                # Reset text position for the next scroll
                self.text_position_x = self.width

    def display_message(self, message):
        current_color = self.colors[self.color_index]
        self.pico_graphics.set_pen(self.pico_graphics.create_pen(*current_color))

        text_width = self.pico_graphics.measure_text(message, self.text_scale)

        # Center the text horizontally
        x = (self.width - text_width) // 2

        self.pico_graphics.text(message, x, self.text_position_y, scale=self.text_scale)

    def display_stock_data(self):
        current_color = self.colors[self.color_index]
        self.pico_graphics.set_pen(self.pico_graphics.create_pen(*current_color))

        full_text = "  ".join(
            f"{symbol}: {price}" for symbol, price in self.stock_data.items()
        )

        # Measure the full text width
        self.full_text_width = self.pico_graphics.measure_text(
            full_text, self.text_scale
        )

        # Move the text leftward
        self.text_position_x -= 1

        # Display the text
        self.pico_graphics.text(
            full_text, self.text_position_x, self.text_position_y, scale=self.text_scale
        )


async def run(
    galactic_unicorn, options_service, pico_graphics, sound_service, wifi_service
):
    stock_display = StocksDisplay(
        galactic_unicorn, options_service, pico_graphics, sound_service, wifi_service
    )

    # Start the display update loop
    await stock_display.update_display()
