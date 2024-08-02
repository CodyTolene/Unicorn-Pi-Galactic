import random

from galactic import Channel


class ExampleMusic:
    # fmt: off
    melody_notes = [
        147, 0, 0, 0, 0, 0, 0, 0, 175, 0, 196, 0, 220, 0, 262, 0, 247, 0, 0, 0, 0, 0, 0, 0,
        -1, 0, 0, 0, 0, 0, 0, 0, 175, 0, 0, 0, 0, 0, 0, 0, 175, 0, 196, 0, 220, 0, 262, 0,
        330, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 349, 0, 0, 0, 0, 0, 0, 0, 349, 0,
        330, 0, 294, 0, 220, 0, 262, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 247, 0, 0,
        0, 0, 0, 0, 0, 247, 0, 220, 0, 196, 0, 147, 0, 175, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0,
        0, 0, 0, 0
    ]
    rhythm_notes = [
        294, 0, 440, 0, 587, 0, 440, 0, 294, 0, 440, 0, 587, 0, 440, 0, 294, 0, 440, 0, 587,
        0, 440, 0, 294, 0, 440, 0, 587, 0, 440, 0, 294, 0, 440, 0, 587, 0, 440, 0, 294, 0,
        440, 0, 587, 0, 440, 0, 392, 0, 523, 0, 659, 0, 523, 0, 392, 0, 523, 0, 659, 0, 523,
        0, 698, 0, 587, 0, 440, 0, 587, 0, 698, 0, 587, 0, 440, 0, 587, 0, 523, 0, 440, 0,
        330, 0, 440, 0, 523, 0, 440, 0, 330, 0, 440, 0, 349, 0, 294, 0, 220, 0, 294, 0, 349,
        0, 294, 0, 220, 0, 294, 0, 262, 0, 247, 0, 220, 0, 175, 0, 165, 0, 147, 0, 131, 0,
        98, 0
    ]
    drum_beats = [
        500, -1, 0, 0, 0, 0, 0, 0, 6000, 0, -1, 0, 0, 0, 500, -1, 500, -1, 0, 0, 0, 0, 0, 0,
        6000, 0, -1, 0, 0, 0, 0, 0, 500, -1, 0, 0, 0, 0, 0, 0, 6000, 0, -1, 0, 0, 0, 500, -1,
        500, -1, 0, 0, 0, 0, 0, 0, 6000, 0, -1, 0, 0, 0, 0, 0, 500, -1, 0, 0, 0, 0, 0, 0, 6000,
        0, -1, 0, 0, 0, 500, -1, 500, -1, 0, 0, 0, 0, 0, 0, 6000, 0, -1, 0, 0, 0, 0, 0, 500,
        -1, 0, 0, 0, 0, 0, 0, 6000, 0, -1, 0, 0, 0, 500, -1, 500, -1, 0, 0, 0, 0, 0, 0, 6000,
        0, -1, 0, 0, 0, 0, 0
    ]
    hi_hat = [
        20000, -1, 20000, -1, 20000, -1, 20000, -1, 20000, -1, 20000, -1, 20000, -1, 20000,
        -1, 20000, -1, 20000, -1, 20000, -1, 20000, -1, 20000, -1, 20000, -1, 20000, -1,
        20000, -1, 20000, -1, 20000, -1, 20000, -1, 20000, -1, 20000, -1, 20000, -1, 20000,
        -1, 20000, -1, 20000, -1, 20000, -1, 20000, -1, 20000, -1, 20000, -1, 20000, -1,
        20000, -1, 20000, -1, 20000, -1, 20000, -1, 20000, -1, 20000, -1, 20000, -1, 20000,
        -1, 20000, -1, 20000, -1, 20000, -1, 20000, -1, 20000, -1, 20000, -1, 20000, -1,
        20000, -1, 20000, -1, 20000, -1, 20000, -1, 20000, -1, 20000, -1, 20000, -1, 20000,
        -1
    ]
    bass_notes = [
        50, -1, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 50, -1, 50, -1, 0, 0, 0, 0, 0, 0, 0, -1,
        0, 0, 0, 0, 0, 0, 50, -1, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 50, -1, 50, -1, 0, 0,
        0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 50, -1, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 50,
        -1, 50, -1, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 50, -1, 0, 0, 0, 0, 0, 0, 0,
        -1, 0, 0, 0, 0, 50, -1, 50, -1, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0
    ]
    # fmt: on
    music_notes = [melody_notes, rhythm_notes, drum_beats, hi_hat, bass_notes]

    def __init__(self, galacticUnicorn, sound):
        self.channels = [
            galacticUnicorn.synth_channel(i) for i in range(len(self.music_notes))
        ]
        self.channels[0].configure(
            waveforms=Channel.TRIANGLE + Channel.SQUARE,
            attack=0.016,
            decay=0.168,
            sustain=0xAFFF / 65535,
            release=0.168,
            volume=sound.get_current_volume(),
        )
        self.channels[1].configure(
            waveforms=Channel.SINE + Channel.SQUARE,
            attack=0.038,
            decay=0.300,
            sustain=0,
            release=0,
            volume=sound.get_current_volume(),
        )
        self.channels[2].configure(
            waveforms=Channel.NOISE,
            attack=0.005,
            decay=0.010,
            sustain=16000 / 65535,
            release=0.100,
            volume=sound.get_current_volume(),
        )
        self.channels[3].configure(
            waveforms=Channel.NOISE,
            attack=0.005,
            decay=0.005,
            sustain=8000 / 65535,
            release=0.040,
            volume=sound.get_current_volume(),
        )
        self.channels[4].configure(
            waveforms=Channel.SQUARE,
            attack=0.010,
            decay=0.100,
            sustain=0,
            release=0.500,
            volume=sound.get_current_volume(),
        )
        self.sound = sound

    def play(self):
        self.sound.play_notes(self.music_notes, self.channels, bpm=700, repeat=True)


class ThunderSound:
    def __init__(self, galacticUnicorn, sound):
        self.channels = [galacticUnicorn.synth_channel(0)]
        self.channels[0].configure(
            waveforms=Channel.NOISE,
            attack=0.005,
            decay=0.010,
            sustain=65535 / 65535,
            release=0.100,
            volume=sound.get_current_volume(),
        )
        self.sound = sound

    # Plays a random thunder sound
    async def play(self):
        random_notes = [random.randint(500, 5000) for _ in range(10)]
        random_bpm = random.choice([random.randint(550, 650), random.randint(430, 530)])
        self.sound.play_notes(
            [random_notes], self.channels, bpm=random_bpm, repeat=False
        )
