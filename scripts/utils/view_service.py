# Cody Tolene
# Apache License 2.0

import uasyncio
import json

from collections import OrderedDict

from views import digital_clock_12_view
from views import digital_clock_24_view
from views import digital_rain_view
from views import dvd_bouncer_view
from views import emergency_view
from views import fire_view
from views import fireflies_view
from views import fireplace_view
from views import fireworks_view
from views import flashlight_torch_view
from views import lava_lamp_view
from views import lightning_view
from views import nyan_cat_view
from views import plasma_view
from views import rainbow_view
from views import raindrops_view
from views import snowfall_view
from views import sos_signal_view
from views import stocks_display_view
from views import warp_speed_view
from views import wave_view


class ViewService:
    def __init__(
        self,
        galactic_unicorn,
        options_service,
        pico_graphics,
        sound_service,
        wifi_service,
    ):
        self.default_view_key = "Rainbow"
        self.galactic_unicorn = galactic_unicorn
        self.options_service = options_service
        self.pico_graphics = pico_graphics
        self.sound_service = sound_service
        self.view_index_file = "/current_view.json"
        self.wifi_service = wifi_service

        self.current_view_key = self.load_current_view_index()
        starting_view = self.get_current_view()
        self.current_view_task = uasyncio.create_task(starting_view)

    def clear_screen(self):
        self.pico_graphics.set_pen(0)  # Black
        self.pico_graphics.clear()  # Clear the screen
        self.galactic_unicorn.update(self.pico_graphics)

    def get_current_view(self):
        views = self.get_views()
        try:
            return views[self.current_view_key](
                self.galactic_unicorn,
                self.options_service,
                self.pico_graphics,
                self.sound_service,
                self.wifi_service,
            )
        except KeyError:
            self.current_view_key = self.default_view_key
            self.save_current_view_index(self.default_view_key)
            return self.get_current_view()

    def get_views(self):
        return OrderedDict(
            [
                ("DVD Bouncer", dvd_bouncer_view.run),
                ("Digital Clock 12-Hour", digital_clock_12_view.run),
                ("Digital Clock 24-Hour", digital_clock_24_view.run),
                ("Digital Rain", digital_rain_view.run),
                ("Emergency", emergency_view.run),
                ("Fire", fire_view.run),
                ("Fireflies", fireflies_view.run),
                ("Fireplace", fireplace_view.run),
                ("Fireworks", fireworks_view.run),
                ("Flashlight Torch", flashlight_torch_view.run),
                ("Lava Lamp", lava_lamp_view.run),
                ("Lightning", lightning_view.run),
                ("Nyan Cat", nyan_cat_view.run),
                ("Plasma", plasma_view.run),
                ("Rainbow", rainbow_view.run),
                ("Raindrops", raindrops_view.run),
                ("SOS", sos_signal_view.run),
                ("Snowfall", snowfall_view.run),
                ("Stocks Display", stocks_display_view.run),
                ("Warp Speed", warp_speed_view.run),
                ("Wave", wave_view.run),
            ]
        )

    def load_current_view_index(self):
        try:
            with open(self.view_index_file, "r") as f:
                data = json.load(f)
                return data.get("current_view_key", self.default_view_key)
        except OSError:
            return self.default_view_key

    def save_current_view_index(self, key):
        with open(self.view_index_file, "w") as f:
            json.dump({"current_view_key": key}, f)

    async def switch_view(self):
        if self.current_view_task:
            self.current_view_task.cancel()
            try:
                await self.current_view_task
            except uasyncio.CancelledError:
                pass

        views = self.get_views()
        self.clear_screen()
        self.save_current_view_index(self.current_view_key)
        self.current_view_task = uasyncio.create_task(
            views[self.current_view_key](
                self.galactic_unicorn,
                self.options_service,
                self.pico_graphics,
                self.sound_service,
                self.wifi_service,
            )
        )
        return self.current_view_task
