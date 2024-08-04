import uasyncio
import urequests
import gc

from utils.options_service import OptionKeys


class StockDisplay:
    def __init__(
        self,
        galactic_unicorn,
        options_service,
        pico_graphics,
        sound_service,
        wifi_service,
    ):
        self.api_key = options_service.get_option(OptionKeys.STOCK_FINNHUB_API_KEY)
        self.button_states = {"C": False, "D": False}
        self.color_index = 0
        self.colors = [
            (255, 255, 255),  # White
            (255, 0, 0),  # Red
            (0, 255, 0),  # Green
            (0, 0, 255),  # Blue
            (255, 255, 0),  # Yellow
            (0, 255, 255),  # Light Blue
            (255, 0, 255),  # Pink
        ]
        self.fetch_interval = 30  # Update data every 30 seconds
        self.galactic_unicorn = galactic_unicorn
        self.height = galactic_unicorn.HEIGHT
        self.options_service = options_service
        self.pico_graphics = pico_graphics
        self.pico_graphics.set_font("bitmap3")
        self.sound_service = sound_service
        self.stock_data = {}
        self.width = galactic_unicorn.WIDTH
        self.wifi_service = wifi_service

        self.stock_symbols = options_service.get_option(OptionKeys.STOCK_SYMBOLS, [])
        self.text_position = self.width

    def fetch_stock_data(self):
        if not self.api_key:
            print("API key is missing.")
            return {symbol: "API key missing" for symbol in self.stock_symbols}

        stock_data = {}
        for symbol in self.stock_symbols:
            try:
                url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={self.api_key}"
                response = urequests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    stock_data[symbol] = data.get("c", "N/A")  # Current price
                else:
                    stock_data[symbol] = "Error: " + str(response.status_code)

                response.close()
                del response  # Free memory
                gc.collect()  # Collect garbage to free memory

            except Exception as e:
                print(f"Error fetching data for {symbol}: {e}")
                stock_data[symbol] = "Error"

        print(stock_data)
        return stock_data

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
        while True:
            self.on_button_press()
            self.pico_graphics.set_pen(0)
            self.pico_graphics.clear()

            if not self.wifi_service.is_connected():
                self.display_message("No Wi-Fi")
            else:
                self.display_stock_data()

            self.galactic_unicorn.update(self.pico_graphics)
            scroll_speed = 0.05
            await uasyncio.sleep(scroll_speed)

    async def fetch_data_periodically(self):
        while True:
            self.stock_data = self.fetch_stock_data()
            await uasyncio.sleep(self.fetch_interval)

    def display_message(self, message):
        self.pico_graphics.set_pen(self.pico_graphics.create_pen(255, 0, 0))
        text_width = self.pico_graphics.measure_text(message, 0.5)

        # Center the text horizontally
        x = (self.width - text_width) // 2
        # Center the text vertically
        y = (self.height - 4) // 2

        self.pico_graphics.text(message, x, y, scale=0.5)

    def display_stock_data(self):
        current_color = self.colors[self.color_index]
        self.pico_graphics.set_pen(self.pico_graphics.create_pen(*current_color))

        text_scale = 0.4
        full_text = "  ".join(
            f"{symbol}: {price}" for symbol, price in self.stock_data.items()
        )

        # Measure the full text width
        full_text_width = self.pico_graphics.measure_text(full_text, text_scale)

        # Move the text leftward
        self.text_position -= 1

        # Reset the text position when the entire text has scrolled past
        if self.text_position < -full_text_width:
            self.text_position = self.width

        self.pico_graphics.text(full_text, self.text_position, 0, scale=text_scale)


async def run(
    galactic_unicorn, options_service, pico_graphics, sound_service, wifi_service
):
    stock_display = StockDisplay(
        galactic_unicorn, options_service, pico_graphics, sound_service, wifi_service
    )

    # Run both `update_display` and `fetch_data_periodically`
    await uasyncio.gather(
        stock_display.update_display(), stock_display.fetch_data_periodically()
    )
