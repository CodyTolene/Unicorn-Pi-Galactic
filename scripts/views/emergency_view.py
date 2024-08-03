# Cody Tolene
# Apache License 2.0

"""
Disclaimer:
This software is provided "as is," without warranty of any kind, express or
implied, including but not limited to the warranties of merchantability,
fitness for a particular purpose, and noninfringement. In no event shall the
authors or copyright holders be liable for any claim, damages, or other
liability, whether in an action of contract, tort, or otherwise, arising from,
out of, or in connection with the software or the use or other dealings in the
software.

The use of emergency lights and/or siren sounds may be inappropriate or illegal
in certain situations or locations. Users are responsible for ensuring
compliance with local laws and regulations and must use this code responsibly.
Use this software at your own risk. The author disclaims all responsibility for
any misuse or adverse effects resulting from the use of this software.
"""

import uasyncio

from utils.sounds import SirenSound


class Emergency:
    def __init__(self, galactic_unicorn, pico_graphics, sound_service):
        self.current_tone = 0
        self.blue = pico_graphics.create_pen(0, 0, 255)
        self.galactic_unicorn = galactic_unicorn
        self.pico_graphics = pico_graphics
        self.sound_service = SirenSound(galactic_unicorn, sound_service)
        self.red = pico_graphics.create_pen(255, 0, 0)

        self.current_color = self.red

    async def play_siren(self):
        if self.current_tone == 0:
            self.sound_service.play_tone_a()
            self.current_tone = 1
        else:
            self.sound_service.play_tone_b()
            self.current_tone = 0

    async def update(self):
        self.pico_graphics.set_pen(self.current_color)
        self.pico_graphics.clear()
        self.galactic_unicorn.update(self.pico_graphics)
        self.current_color = self.blue if self.current_color == self.red else self.red
        await self.play_siren()


async def run(galactic_unicorn, pico_graphics, sound_service):
    emergency = Emergency(galactic_unicorn, pico_graphics, sound_service)

    while True:
        await emergency.update()
        await uasyncio.sleep(1.15)
