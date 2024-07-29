# Cody Tolene
# Apache License 2.0

import uasyncio
import random

from utils.music import play_notes
from galactic import Channel


async def run(galacticUnicorn, graphics):
    width = galacticUnicorn.WIDTH
    height = galacticUnicorn.HEIGHT

    # Choose a direction for all raindrops at the start
    direction = random.choice([-0.3, 0.3])

    class Raindrop:
        def __init__(self):
            self.x = random.randint(0, width - 1)
            self.y = random.uniform(0, height - 1)
            self.speed_y = random.uniform(0.3, 0.7)
            self.speed_x = direction
            self.color = graphics.create_pen(0, 0, random.randint(150, 255))

        async def update(self):
            graphics.set_pen(self.color)
            graphics.pixel(int(self.x), int(self.y))
            self.x += self.speed_x
            self.y += self.speed_y
            if self.y >= height or self.x < 0 or self.x >= width:
                self.y = 0
                self.x = random.randint(0, width - 1)

    raindrops = [Raindrop() for _ in range(30)]

    # Configure and play rain sound
    musicNotes = [800, 810, 820]
    channel = galacticUnicorn.synth_channel(0)
    channel.configure(
        waveforms=Channel.NOISE,
        attack=0.005,
        decay=0.500,
        sustain=0,
        release=0.100,
        volume=18000 / 65535,
    )
    channels = [channel]
    play_notes(galacticUnicorn, [musicNotes], channels, bpm=820, repeat=True)

    while True:
        graphics.set_pen(graphics.create_pen(0, 0, 0))
        graphics.clear()

        for raindrop in raindrops:
            await raindrop.update()

        galacticUnicorn.update(graphics)
        await uasyncio.sleep(0.025)
