# Cody Tolene
# Apache License 2.0

import uasyncio
from machine import Timer
from galactic import GalacticUnicorn, Channel
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY

volume = 0.5  # Set initial volume to 0.5
previous_volume = 0.5


# Create and play music on the Pimoroni Galactic Unicorn.
def play_notes(
    galacticUnicorn,  # Instance of GalacticUnicorn.
    musicNotes,  # List of note sequences for each channel.
    channels,  # List of configured synth channels.
    bpm,  # Beats per minute for the music.
    repeat=False,  # Boolean for optional repeat when song ends.
):
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
                timer.deinit()
                galacticUnicorn.stop_playing()

    def tick(timer):
        next_beat()

    timer = Timer(-1)
    timer.init(freq=bpm / 60, mode=Timer.PERIODIC, callback=tick)

    galacticUnicorn.play_synth()
    return timer


# Temporarily toggle all sounds on or off.
async def toggle_mute(galacticUnicorn):
    global previous_volume
    global volume
    if volume == 0.0:
        volume = previous_volume
    else:
        previous_volume = volume
        volume = 0.0
    galacticUnicorn.set_volume(volume)


# Decrease all channel volumes.
async def volume_down(galacticUnicorn):
    global volume
    # print("Volume down")
    volume = max(volume - 0.1, 0.0)
    galacticUnicorn.set_volume(volume)


# Increase all channel volumes.
async def volume_up(galacticUnicorn):
    global volume
    # print("Volume up")
    volume = min(volume + 0.1, 1.0)
    galacticUnicorn.set_volume(volume)


# Stop all currently playing sounds.
async def stop_all_sounds(galacticUnicorn):
    galacticUnicorn.stop_playing()


async def play_example_rain(galacticUnicorn, graphics):
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
        volume=18000 / 65535,
    )

    # Create and play rain sound
    channels = [channel]
    play_notes(galacticUnicorn, [musicNotes], channels, bpm=820, repeat=True)

    # Wait for 3 seconds
    await uasyncio.sleep(3)

    # Volume up
    await volume_up(galacticUnicorn)
    await volume_up(galacticUnicorn)
    await volume_up(galacticUnicorn)
    await volume_up(galacticUnicorn)
    await volume_up(galacticUnicorn)

    # Wait for 3 seconds
    await uasyncio.sleep(3)

    # Volume down
    await volume_down(galacticUnicorn)
    await volume_down(galacticUnicorn)
    await volume_down(galacticUnicorn)
    await volume_down(galacticUnicorn)
    await volume_down(galacticUnicorn)

    # Wait for 5 seconds
    await uasyncio.sleep(5)

    # And then stop all sounds
    await stop_all_sounds(galacticUnicorn)


# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    # Test the rain sound example
    uasyncio.run(play_example_rain(galacticUnicorn, graphics))
