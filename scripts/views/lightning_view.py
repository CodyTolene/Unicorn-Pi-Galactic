# Cody Tolene
# Apache License 2.0

import uasyncio
import random
from galactic import GalacticUnicorn, Channel
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY


class Lightning:
    def __init__(self, galacticUnicorn, graphics, music):
        self.bolts = []
        self.flash = False
        self.flash_duration = 0
        self.galacticUnicorn = galacticUnicorn
        self.graphics = graphics
        self.height = galacticUnicorn.HEIGHT
        self.music = music
        self.width = galacticUnicorn.WIDTH

        self.channels = [self.galacticUnicorn.synth_channel(0)]
        self.channels[0].configure(
            waveforms=Channel.NOISE,
            attack=0.005,
            decay=0.010,
            sustain=65535 / 65535,
            release=0.100,
            volume=music.volume,
        )

    def create_bolt(self):
        bolt = []
        x = random.randint(0, self.width - 1)
        y = 0
        while y < self.height:
            bolt.append((x, y))
            x += random.choice([-1, 0, 1])
            x = max(0, min(x, self.width - 1))
            y += 1
        return bolt

    async def update(self):
        self.graphics.set_pen(self.graphics.create_pen(0, 0, 0))
        self.graphics.clear()

        if self.flash:
            self.graphics.set_pen(self.graphics.create_pen(255, 255, 255))
            for x in range(self.width):
                for y in range(self.height):
                    self.graphics.pixel(x, y)
            self.flash_duration -= 1
            if self.flash_duration <= 0:
                self.flash = False
                self.bolts = []
        else:
            if random.random() < 0.05:
                self.flash = True
                self.flash_duration = random.randint(1, 3)
                self.bolts = [self.create_bolt() for _ in range(random.randint(1, 3))]
                await self.play_lightning_sound()

        for bolt in self.bolts:
            for x, y in bolt:
                self.graphics.set_pen(self.graphics.create_pen(255, 255, 255))
                self.graphics.pixel(x, y)

        self.galacticUnicorn.update(self.graphics)

    async def play_lightning_sound(self):
        lightning_notes = [random.randint(500, 5000) for _ in range(10)]
        bpm = random.choice([random.randint(550, 650), random.randint(430, 530)])
        self.music.play_notes([lightning_notes], self.channels, bpm=bpm, repeat=False)


async def run(galacticUnicorn, graphics, music):
    lightning = Lightning(galacticUnicorn, graphics, music)

    while True:
        await lightning.update()
        await uasyncio.sleep(0.1)


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
