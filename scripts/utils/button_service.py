# Cody Tolene
# Apache License 2.0

import uasyncio


class ButtonService:
    def __init__(self, view_service):
        self.galactic_unicorn = view_service.galactic_unicorn
        self.sound_service = view_service.sound_service
        self.view_service = view_service
        self.views = view_service.get_views()
        self.wifi_service = view_service.wifi_service

        # Initialize button states
        self.button_states = {
            "A": False,
            "B": False,
            "C": False,
            "D": False,
            "VOLUME_UP": False,
            "VOLUME_DOWN": False,
            "BRIGHTNESS_UP": False,
            "BRIGHTNESS_DOWN": False,
            "SLEEP": False,
        }

        # Device states
        self.is_device_on = True
        self.previous_brightness = self.galactic_unicorn.get_brightness()

    async def run(self):
        view_keys = list(self.views.keys())

        while True:
            # Handle button presses
            if self.is_device_on:
                await self.handle_button_a(view_keys)
                await self.handle_button_b(view_keys)
                await self.handle_button_c()
                await self.handle_button_d()
                await self.handle_volume_up()
                await self.handle_volume_down()
                await self.handle_brightness_up()
                await self.handle_brightness_down()

            # Handle sleep button (device on/off)
            await self.handle_sleep()

            # Sleep for a short period to debounce button presses
            await uasyncio.sleep(0.1)

    async def handle_button_a(self, view_keys):
        if self.galactic_unicorn.is_pressed(self.galactic_unicorn.SWITCH_A):
            if not self.button_states["A"]:
                self.button_states["A"] = True
                await self.sound_service.stop_all_sounds()
                current_index = view_keys.index(self.view_service.current_view_key)
                self.view_service.current_view_key = view_keys[
                    (current_index - 1) % len(view_keys)
                ]
                await self.view_service.switch_view()
        else:
            self.button_states["A"] = False

    async def handle_button_b(self, view_keys):
        if self.galactic_unicorn.is_pressed(self.galactic_unicorn.SWITCH_B):
            if not self.button_states["B"]:
                self.button_states["B"] = True
                await self.sound_service.stop_all_sounds()
                current_index = view_keys.index(self.view_service.current_view_key)
                self.view_service.current_view_key = view_keys[
                    (current_index + 1) % len(view_keys)
                ]
                await self.view_service.switch_view()
        else:
            self.button_states["B"] = False

    async def handle_button_c(self):
        if self.galactic_unicorn.is_pressed(self.galactic_unicorn.SWITCH_C):
            if not self.button_states["C"]:
                self.button_states["C"] = True
        else:
            self.button_states["C"] = False

    async def handle_button_d(self):
        if self.galactic_unicorn.is_pressed(self.galactic_unicorn.SWITCH_D):
            if not self.button_states["D"]:
                self.button_states["D"] = True
        else:
            self.button_states["D"] = False

    async def handle_volume_up(self):
        if self.galactic_unicorn.is_pressed(self.galactic_unicorn.SWITCH_VOLUME_UP):
            if not self.button_states["VOLUME_UP"]:
                self.button_states["VOLUME_UP"] = True
                await self.sound_service.volume_up()
        else:
            self.button_states["VOLUME_UP"] = False

    async def handle_volume_down(self):
        if self.galactic_unicorn.is_pressed(self.galactic_unicorn.SWITCH_VOLUME_DOWN):
            if not self.button_states["VOLUME_DOWN"]:
                self.button_states["VOLUME_DOWN"] = True
                await self.sound_service.volume_down()
        else:
            self.button_states["VOLUME_DOWN"] = False

    async def handle_brightness_up(self):
        if self.galactic_unicorn.is_pressed(self.galactic_unicorn.SWITCH_BRIGHTNESS_UP):
            if not self.button_states["BRIGHTNESS_UP"]:
                self.button_states["BRIGHTNESS_UP"] = True
                current_brightness = self.galactic_unicorn.get_brightness()
                if current_brightness < 0.1:
                    new_brightness = 0.25
                else:
                    new_brightness = min(current_brightness + 0.25, 1.0)
                self.galactic_unicorn.set_brightness(new_brightness)
        else:
            self.button_states["BRIGHTNESS_UP"] = False

    async def handle_brightness_down(self):
        if self.galactic_unicorn.is_pressed(
            self.galactic_unicorn.SWITCH_BRIGHTNESS_DOWN
        ):
            if not self.button_states["BRIGHTNESS_DOWN"]:
                self.button_states["BRIGHTNESS_DOWN"] = True
                current_brightness = self.galactic_unicorn.get_brightness()
                new_brightness = max(current_brightness - 0.25, 0.1)
                self.galactic_unicorn.set_brightness(new_brightness)
        else:
            self.button_states["BRIGHTNESS_DOWN"] = False

    async def handle_sleep(self):
        if self.galactic_unicorn.is_pressed(self.galactic_unicorn.SWITCH_SLEEP):
            if not self.button_states["SLEEP"]:
                self.button_states["SLEEP"] = True
                if self.is_device_on:
                    self.previous_brightness = self.galactic_unicorn.get_brightness()
                    self.galactic_unicorn.set_brightness(0)
                    await self.sound_service.toggle_mute()
                    self.view_service.clear_screen()
                    self.is_device_on = False
                else:
                    self.galactic_unicorn.set_brightness(self.previous_brightness)
                    await self.sound_service.toggle_mute()
                    self.is_device_on = True
        else:
            self.button_states["SLEEP"] = False
