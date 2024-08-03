# Cody Tolene
# Apache License 2.0

import json


class OptionsService:
    def __init__(self, json_file_path="/options.json"):
        self.json_file_path = json_file_path
        self.options = self.load_options()

    def load_options(self):
        try:
            with open(self.json_file_path, "r") as f:
                data = json.load(f)
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

    def get_option(self, key, default=None):
        return self.options.get(key, default)

    def set_option(self, key, value):
        self.options[key] = value
        self.save_options(self.options)

    def default_options(self):
        # Define default options
        return {"wifi_ssid": None, "wifi_password": None}
