# Cody Tolene
# Apache License 2.0

from machine import Timer


# A class for playing sound on the Pimoroni Galactic Unicorn.
class SoundService:
    def __init__(self, galactic_unicorn):
        self.current_timer = None
        self.galactic_unicorn = galactic_unicorn

        self.galactic_unicorn.set_volume(0.2)
        self.previous_volume = galactic_unicorn.get_volume()

    def play_notes(
        self,
        notes,  # List of note sequences for each channel.
        channels,  # List of configured synth channels.
        bpm,  # Beats per minute for the sound_service.
        repeat=False,  # Boolean for optional repeat when song ends.
    ):
        # Ensure any previous timer is deinitialized
        if self.current_timer:
            self.current_timer.deinit()
            self.current_timer = None

        # Length of the song in beats.
        song_length = max(len(track) for track in notes)
        beat = 0  # Current beat in the song.

        def next_beat():
            nonlocal beat
            for i in range(len(notes)):
                if beat < len(notes[i]):
                    frequency = notes[i][beat]
                    if frequency > 0:
                        channels[i].frequency(frequency)
                        channels[i].trigger_attack()
                    elif frequency == -1:
                        channels[i].trigger_release()
            beat += 1
            if beat >= song_length:
                if repeat:
                    beat = 0
                else:
                    if self.current_timer:
                        self.current_timer.deinit()
                        self.current_timer = None
                    self.galactic_unicorn.stop_playing()

        def tick(timer):
            next_beat()

        self.current_timer = Timer(-1)
        self.current_timer.init(freq=bpm / 60, mode=Timer.PERIODIC, callback=tick)

        self.galactic_unicorn.play_synth()
        return self.current_timer

    # Temporarily toggle all sounds on or off.
    async def toggle_mute(self):
        current_volume = self.get_current_volume()

        if current_volume == 0.0:
            current_volume = self.previous_volume
        else:
            self.previous_volume = current_volume
            current_volume = 0.0

        self.galactic_unicorn.set_volume(current_volume)

    # Decrease all channel volumes.
    async def volume_down(self):
        self.galactic_unicorn.adjust_volume(-0.1)

    # Increase all channel volumes.
    async def volume_up(self):
        self.galactic_unicorn.adjust_volume(0.1)

    # Stop all currently playing sounds.
    async def stop_all_sounds(self):
        if self.current_timer:
            self.current_timer.deinit()
            self.current_timer = None
        self.galactic_unicorn.stop_playing()
        for i in range(8):  # Assuming 8 channels
            channel = self.galactic_unicorn.synth_channel(i)
            channel.trigger_release()

    # Getter for the current volume
    def get_current_volume(self):
        return self.galactic_unicorn.get_volume()
