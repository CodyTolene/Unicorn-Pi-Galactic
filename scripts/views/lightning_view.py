# Cody Tolene
# Apache License 2.0

import uasyncio
import random
from galactic import Channel
from utils.music import play_notes


class Lightning:
    def __init__(self, width, height, graphics, gu):
        self.graphics = graphics
        self.width = width
        self.height = height
        self.gu = gu
        self.flash = False
        self.flash_duration = 0
        self.bolts = []
        self.channels = [self.gu.synth_channel(0)]
        self.configure_channel()
        self.lightning_notes = [random.randint(500, 5000) for _ in range(10)]

    def configure_channel(self):
        # Configure sound channel
        self.channels[0].configure(
            waveforms=Channel.NOISE,
            attack=0.005,
            decay=0.010,
            sustain=65535 / 65535,
            release=0.100,
            volume=65535 / 65535,
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

    async def play_lightning_sound(self):
        # Randomly vary the BPM around 600 or 480
        bpm = random.choice([random.randint(550, 650), random.randint(430, 530)])
        play_notes(
            self.gu, [self.lightning_notes], self.channels, bpm=bpm, repeat=False
        )


async def run(galacticUnicorn, graphics):
    width = galacticUnicorn.WIDTH
    height = galacticUnicorn.HEIGHT
    lightning = Lightning(
        width, height, graphics, galacticUnicorn
    )  # Create Lightning effect

    while True:
        graphics.set_pen(graphics.create_pen(0, 0, 0))  # Clear the screen
        graphics.clear()

        await lightning.update()  # Update the Lightning effect

        galacticUnicorn.update(graphics)  # Update the display
        await uasyncio.sleep(0.1)  # Pause before the next update
