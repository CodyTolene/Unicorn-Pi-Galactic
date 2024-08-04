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
        self.galactic_unicorn = galactic_unicorn
        self.height = galactic_unicorn.HEIGHT
        self.options_service = options_service
        self.pico_graphics = pico_graphics
        self.sound_service = sound_service
        self.width = galactic_unicorn.WIDTH
        self.wifi_service = wifi_service

        self.stock_symbols = self.load_stock_symbols()
        self.api_key = self.options_service.get_option(OptionKeys.STOCK_FINNHUB_API_KEY)
        self.colors = [
            (255, 255, 255),  # White
            (255, 0, 0),  # Red
            (0, 255, 0),  # Green
            (0, 0, 255),  # Blue
            (255, 255, 0),  # Yellow
            (0, 255, 255),  # Light Blue
            (255, 0, 255),  # Pink
        ]
        self.color_index = 0
        self.button_states = {"C": False, "D": False}
        self.pico_graphics.set_font("bitmap3")  # Ensure this is the smallest font
        # No longer managing Wi-Fi directly in this class

    def load_stock_symbols(self):
        # Load stock symbols from the options JSON file
        symbols = self.options_service.get_option(OptionKeys.STOCK_SYMBOLS, [])
        return symbols[:4]  # Limit to 4 symbols

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
                    stock_data[symbol] = data.get(
                        "c", "N/A"
                    )  # 'c' is the current price
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

    async def update(self):
        self.on_button_press()
        self.pico_graphics.set_pen(0)
        self.pico_graphics.clear()

        if not self.wifi_service.is_connected():
            self.display_message("No Wi-Fi")
        else:
            stock_data = self.fetch_stock_data()
            self.display_stock_data(stock_data)

        self.galactic_unicorn.update(self.pico_graphics)

    def display_message(self, message):
        self.pico_graphics.set_pen(
            self.pico_graphics.create_pen(255, 0, 0)
        )  # Red pen for message
        text_width = self.pico_graphics.measure_text(message, 0.5)  # Smaller text scale
        x = (self.width - text_width) // 2  # Center the text horizontally
        y = (self.height - 4) // 2  # Center the text vertically
        self.pico_graphics.text(message, x, y, scale=0.5)

    def display_stock_data(self, stock_data):
        current_color = self.colors[self.color_index]
        self.pico_graphics.set_pen(self.pico_graphics.create_pen(*current_color))

        # Define quadrants for each stock symbol
        quadrant_width = self.width // 2
        quadrant_height = self.height // 2

        positions = [
            (0, 0),  # Top-left
            (quadrant_width, 0),  # Top-right
            (0, quadrant_height),  # Bottom-left
            (quadrant_width, quadrant_height),  # Bottom-right
        ]

        text_scale = 0.5  # Smaller scale

        for index, (symbol, price) in enumerate(stock_data.items()):
            symbol_str = f"{symbol}"
            price_str = f"{price}"

            # Calculate positions for symbol and price to ensure they fit
            x, y = positions[index]
            symbol_text_width = self.pico_graphics.measure_text(symbol_str, text_scale)
            price_text_width = self.pico_graphics.measure_text(price_str, text_scale)

            # Position symbol and price
            symbol_x = int(x + (quadrant_width - symbol_text_width) / 2)
            symbol_y = int(y + 1)  # Slight offset from the top

            price_x = int(x + (quadrant_width - price_text_width) / 2)
            price_y = int(symbol_y + 4)  # Place below the symbol

            self.pico_graphics.text(symbol_str, symbol_x, symbol_y, scale=text_scale)
            self.pico_graphics.text(price_str, price_x, price_y, scale=text_scale)


async def run(
    galactic_unicorn, options_service, pico_graphics, sound_service, wifi_service
):
    stock_display = StockDisplay(
        galactic_unicorn, options_service, pico_graphics, sound_service, wifi_service
    )

    while True:
        await stock_display.update()
        await uasyncio.sleep(10)  # Update every 10 seconds
