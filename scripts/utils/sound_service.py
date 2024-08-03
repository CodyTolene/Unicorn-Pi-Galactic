# Cody Tolene
# Apache License 2.0

from machine import Timer


# A class for playing sound on the Pimoroni Galactic Unicorn.
class SoundService:
    def __init__(self, galacticUnicorn):
        self.current_timer = None
        self.galacticUnicorn = galacticUnicorn
        self.previous_volume = galacticUnicorn.get_volume()

        # Set the initial volume
        self.galacticUnicorn.set_volume(0.2)

    def play_notes(
        self,
        musicNotes,  # List of note sequences for each channel.
        channels,  # List of configured synth channels.
        bpm,  # Beats per minute for the sound_service.
        repeat=False,  # Boolean for optional repeat when song ends.
    ):
        """Play notes in the old format."""
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
                    frequency = musicNotes[i][beat]
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
