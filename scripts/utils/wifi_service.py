# Cody Tolene
# Apache License 2.0

import network
import uasyncio


class WiFiService:
    def __init__(self, options_service):
        self.ssid = options_service.get_option("wifi_ssid")
        self.password = options_service.get_option("wifi_password")
        self.wlan = network.WLAN(network.STA_IF)

    async def connect(self):
        if not self.ssid or not self.password:
            print("No Wi-Fi credentials, skipping connection. Some views may not work!")
            return

        self.wlan.active(True)
        if not self.wlan.isconnected():
            print("Connecting to network...")
            try:
                self.wlan.connect(
                    self.ssid.encode("utf-8"), self.password.encode("utf-8")
                )
                max_wait = 20  # 20 seconds
                while max_wait > 0 and not self.wlan.isconnected():
                    print("Waiting for connection...")
                    await uasyncio.sleep(1)
                    max_wait -= 1
            except Exception as e:
                print(f"Error connecting to Wi-Fi: {e}")
                return

        if self.wlan.isconnected():
            print("Connected to Wi-Fi")
            print("Network config:", self.wlan.ifconfig())
            return
        else:
            print("Failed to connect to Wi-Fi")
            return

    def is_connected(self):
        return self.wlan.isconnected()
