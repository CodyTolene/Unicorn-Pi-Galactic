# Cody Tolene
# Apache License 2.0

import uasyncio

from galactic import GalacticUnicorn, Channel
from machine import Timer
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY


# A class for playing sound on the Pimoroni Galactic Unicorn.
class Sound:
    def __init__(self, galacticUnicorn):
        self.current_timer = None
        self.galacticUnicorn = galacticUnicorn
        self.previous_volume = galacticUnicorn.get_volume()

    def play_notes(
        self,
        musicNotes,  # List of note sequences for each channel.
        channels,  # List of configured synth channels.
        bpm,  # Beats per minute for the sound.
        repeat=False,  # Boolean for optional repeat when song ends.
    ):
        # Ensure any previous timer is deinitialized
        if self.current_timer:
            self.current_timer.deinit()
            self.current_timer = None

        # Length of the song in beats.
        song_length = max(len(track) for track in musicNotes)
        beat = 0  # Current beat in the song.

        def next_beat():
            nonlocal beat
            for i in range(len(musicNotes)):
                if beat < len(musicNotes[i]):
                    if musicNotes[i][beat] > 0:
                        channels[i].frequency(musicNotes[i][beat])
                        channels[i].trigger_attack()
                    elif musicNotes[i][beat] == -1:
                        channels[i].trigger_release()
            beat = beat + 1
            if beat >= song_length:
                if repeat:
                    beat = 0
                else:
                    if self.current_timer:
                        self.current_timer.deinit()
                        self.current_timer = None
                    self.galacticUnicorn.stop_playing()

        def tick(timer):
            next_beat()

        self.current_timer = Timer(-1)
        self.current_timer.init(freq=bpm / 60, mode=Timer.PERIODIC, callback=tick)

        self.galacticUnicorn.play_synth()
        return self.current_timer

    # Temporarily toggle all sounds on or off.
    async def toggle_mute(self):
        current_volume = self.get_current_volume()

        if current_volume == 0.0:
            current_volume = self.previous_volume
        else:
            self.previous_volume = current_volume
            current_volume = 0.0

        self.galacticUnicorn.set_volume(current_volume)

    # Decrease all channel volumes.
    async def volume_down(self):
        self.galacticUnicorn.adjust_volume(-0.1)

    # Increase all channel volumes.
    async def volume_up(self):
        self.galacticUnicorn.adjust_volume(0.1)

    # Stop all currently playing sounds.
    async def stop_all_sounds(self):
        if self.current_timer:
            self.current_timer.deinit()
            self.current_timer = None
        self.galacticUnicorn.stop_playing()
        for i in range(8):  # Assuming 8 channels
            channel = self.galacticUnicorn.synth_channel(i)
            channel.trigger_release()

    # Getter for the current volume
    def get_current_volume(self):
        return self.galacticUnicorn.get_volume()


async def play_example_rain(galacticUnicorn, graphics, sound):
    # Rain sound frequencies (white noise-like)
    musicNotes = [800, 810, 820]

    # Configure channels
    channel = galacticUnicorn.synth_channel(0)
    channel.configure(
        waveforms=Channel.NOISE,
        attack=0.005,
        decay=0.500,
        sustain=0,
        release=0.100,
        volume=sound.get_current_volume(),
    )

    # Create and play rain sound
    channels = [channel]
    sound.play_notes([musicNotes], channels, bpm=820, repeat=True)

    # Wait for 3 seconds
    await uasyncio.sleep(3)

    # Volume up
    await sound.volume_up()
    await sound.volume_up()
    await sound.volume_up()
    await sound.volume_up()
    await sound.volume_up()

    # Wait for 3 seconds
    await uasyncio.sleep(3)

    # Volume down
    await sound.volume_down()
    await sound.volume_down()
    await sound.volume_down()
    await sound.volume_down()
    await sound.volume_down()

    # Wait for 5 seconds
    await uasyncio.sleep(5)

    # And then stop all sounds
    await sound.stop_all_sounds()


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    sound = Sound(galacticUnicorn)
    uasyncio.run(play_example_rain(galacticUnicorn, graphics, sound))
