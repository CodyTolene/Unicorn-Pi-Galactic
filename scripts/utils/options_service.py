# Cody Tolene
# Apache License 2.0

import json


class OptionKeys:
    WIFI_SSID = "wifi_ssid"
    WIFI_PASSWORD = "wifi_password"
    STOCKS_FINNHUB_API_KEY = "stocks_finnhub_api_key"
    STOCKS_SCROLL_SPEED = "stocks_scroll_speed"
    STOCKS_SYMBOLS = "stocks_symbols"
    STOCKS_UPDATE_AFTER_X_SCROLLS = "stocks_update_after_x_scrolls"
    STOCKS_UPDATE_MESSAGE = "stocks_update_message"
    TIME_ZONE = "time_zone"


class OptionsService:
    def __init__(self):
        self.json_file_path = "/options.json"
        self.options = self.load_options()

    def load_options(self):
        try:
            with open(self.json_file_path, "r") as f:
                data = json.load(f)
                # Ensure the current booleans are correctly parsed
                data[OptionKeys.STOCKS_UPDATE_MESSAGE] = self.parse_boolean(
                    data.get(OptionKeys.STOCKS_UPDATE_MESSAGE, False)
                )
                return data
        except OSError:
            self.save_options(self.default_options())
            return self.default_options()
        except ValueError:
            self.save_options(self.default_options())
            return self.default_options()

    def save_options(self, options):
        try:
            with open(self.json_file_path, "w") as f:
                json.dump(options, f)
        except OSError as e:
            print(f"Error writing to {self.json_file_path}: {e}")

    def get_option(self, key: OptionKeys, default=None):
        return self.options.get(key, default)

    def set_option(self, key: OptionKeys, value):
        self.options[key] = value
        self.save_options(self.options)

    def parse_boolean(self, value):
        # Handle booleans that might be stored as strings or other types
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("true", "yes", "1")
        return bool(value)

    def default_options(self):
        return {
            OptionKeys.WIFI_SSID: "",
            OptionKeys.WIFI_PASSWORD: "",
            OptionKeys.STOCKS_FINNHUB_API_KEY: "",
            OptionKeys.STOCKS_SCROLL_SPEED: 0.75,
            OptionKeys.STOCKS_SYMBOLS: ["NVDA", "AMD", "MSFT", "GOOGL"],
            OptionKeys.STOCKS_UPDATE_AFTER_X_SCROLLS: 3,
            OptionKeys.STOCKS_UPDATE_MESSAGE: True,
            OptionKeys.TIME_ZONE: "America/Chicago",
        }
