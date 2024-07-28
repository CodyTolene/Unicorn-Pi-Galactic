# Cody Tolene
# Apache License 2.0

import uasyncio
import random
from galactic import GalacticUnicorn, Channel
from machine import Timer


class Lightning:
    def __init__(self, width, height, graphics, gu, timer):
        self.graphics = graphics
        self.width = width
        self.height = height
        self.gu = gu
        self.timer = timer
        self.flash = False
        self.flash_duration = 0
        self.bolts = []
        self.channels = [self.gu.synth_channel(0)]
        self.configure_channel()

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
                self.play_lightning_sound()

        for bolt in self.bolts:
            for x, y in bolt:
                self.graphics.set_pen(self.graphics.create_pen(255, 255, 255))
                self.graphics.pixel(x, y)

    def play_lightning_sound(self):
        self.gu.play_synth()
        self.channels[0].trigger_attack()
        self.timer.init(
            freq=1, mode=Timer.ONE_SHOT, callback=lambda t: self.release_sound()
        )

    def release_sound(self):
        self.channels[0].trigger_release()
        self.gu.stop_playing()


async def run(galacticUnicorn, graphics):
    width = galacticUnicorn.WIDTH
    height = galacticUnicorn.HEIGHT
    timer = Timer(-1)  # Create a timer for managing sound release
    lightning = Lightning(
        width, height, graphics, galacticUnicorn, timer
    )  # Create Lightning effect

    while True:
        graphics.set_pen(graphics.create_pen(0, 0, 0))  # Clear the screen
        graphics.clear()

        await lightning.update()  # Update the Lightning effect

        galacticUnicorn.update(graphics)  # Update the display
        await uasyncio.sleep(0.1)  # Pause before the next update


# This section of code is only for testing.
if __name__ == "__main__":
    from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY

    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
