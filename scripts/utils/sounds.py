# Cody Tolene
# Apache License 2.0
#
# Contains code from here under the MIT License:
# https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/examples/galactic_unicorn

import random

from galactic import Channel


class CelebrationSound:
    def __init__(self, galacticUnicorn, sound_service):
        self.galacticUnicorn = galacticUnicorn
        self.notes = [784, 880, 988, 1047, 1175, 988, 1047, 880, 784, -1, 800]
        self.sound_service = sound_service

        self.channels = self.set_channels()

    def set_channels(self):
        channels = [self.galacticUnicorn.synth_channel(0)]
        channels[0].configure(
            waveforms=Channel.SQUARE + Channel.TRIANGLE,
            attack=0.01,
            decay=0.1,
            sustain=0.7,
            release=0.2,
            volume=self.sound_service.get_current_volume(),
        )
        return channels

    def play(self, bpm=480, repeat=False):
        self.channels = self.set_channels()
        self.sound_service.play_notes(
            [self.notes], self.channels, bpm=bpm, repeat=repeat
        )


class CelebrationSound2:
    def __init__(self, galacticUnicorn, sound_service):
        self.galacticUnicorn = galacticUnicorn
        self.notes = [523, 587, 659, 698, 784, 880, 988, 1047, -1]
        self.sound_service = sound_service

        self.channels = self.set_channels()

    def set_channels(self):
        channels = [self.galacticUnicorn.synth_channel(0)]
        channels[0].configure(
            waveforms=Channel.SQUARE + Channel.TRIANGLE,
            attack=0.01,
            decay=0.1,
            sustain=0.7,
            release=0.2,
            volume=self.sound_service.get_current_volume(),
        )
        return channels

    def play(self, bpm=360, repeat=False):
        self.channels = self.set_channels()
        self.sound_service.play_notes(
            [self.notes], self.channels, bpm=bpm, repeat=repeat
        )


class CricketSound:
    def __init__(self, galacticUnicorn, sound_service):
        self.galacticUnicorn = galacticUnicorn
        self.sound_service = sound_service
        self.channels = self.set_channels()

    def set_channels(self):
        channels = [self.galacticUnicorn.synth_channel(0)]
        channels[0].configure(
            waveforms=Channel.SINE,
            attack=0.005,
            decay=0.02,
            sustain=0.0,
            release=0.02,
            volume=self.sound_service.get_current_volume() * 0.4,
        )
        return channels

    def play(self, repeat=False):
        self.channels = self.set_channels()

        chirp_frequency = random.randint(2000, 2050)
        chirp_pattern = [
            chirp_frequency,
            0,
            chirp_frequency,
            0,
            chirp_frequency,
            0,
            0,
            0,
            0,
            0,
        ]
        chirp_sequence = chirp_pattern * random.randint(2, 3)
        silence_duration = random.randint(180, 420)
        chirp_sequence.extend([0] * silence_duration)
        random_bpm = random.randint(1500, 3000)

        self.sound_service.play_notes(
            [chirp_sequence], self.channels, bpm=random_bpm, repeat=repeat
        )


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

    def __init__(self, galacticUnicorn, sound_service):
        self.galacticUnicorn = galacticUnicorn
        self.sound_service = sound_service

        self.channels = self.set_channels()

    def set_channels(self):
        channels = [
            self.galacticUnicorn.synth_channel(i) for i in range(len(self.music_notes))
        ]
        channels[0].configure(
            waveforms=Channel.TRIANGLE + Channel.SQUARE,
            attack=0.016,
            decay=0.168,
            sustain=0xAFFF / 65535,
            release=0.168,
            volume=self.sound_service.get_current_volume(),
        )
        channels[1].configure(
            waveforms=Channel.SINE + Channel.SQUARE,
            attack=0.038,
            decay=0.300,
            sustain=0,
            release=0,
            volume=self.sound_service.get_current_volume(),
        )
        channels[2].configure(
            waveforms=Channel.NOISE,
            attack=0.005,
            decay=0.010,
            sustain=16000 / 65535,
            release=0.100,
            volume=self.sound_service.get_current_volume(),
        )
        channels[3].configure(
            waveforms=Channel.NOISE,
            attack=0.005,
            decay=0.005,
            sustain=8000 / 65535,
            release=0.040,
            volume=self.sound_service.get_current_volume(),
        )
        channels[4].configure(
            waveforms=Channel.SQUARE,
            attack=0.010,
            decay=0.100,
            sustain=0,
            release=0.500,
            volume=self.sound_service.get_current_volume(),
        )
        return channels

    def play(self, bpm=700, repeat=True):
        self.channels = self.set_channels()
        self.sound_service.play_notes(
            self.music_notes, self.channels, bpm=bpm, repeat=repeat
        )


class ExampleRandomMusic:
    def __init__(self, galacticUnicorn, sound_service):
        self.sound_service = sound_service
        self.notes = []
        self.galacticUnicorn = galacticUnicorn
        self.channels = self.set_channels()

        for _ in range(8):  # 8 channels
            channel_notes = []
            for _ in range(16):  # Range of 16 notes per channel
                # Randomly select a low-frequency note or silence (-1)
                note = random.choice([220, 330, 440, -1])
                channel_notes.append(note)
            self.notes.append(channel_notes)

    def set_channels(self):
        channels = [self.galacticUnicorn.synth_channel(i) for i in range(8)]
        for channel in channels:
            channel.configure(
                waveforms=Channel.SINE,
                attack=0.01,
                decay=0.1,
                sustain=0.5,
                release=0.5,
                volume=self.sound_service.get_current_volume(),
            )
        return channels

    def play(self, bpm=60, repeat=True):
        self.channels = self.set_channels()
        self.sound_service.play_notes(self.notes, self.channels, bpm=bpm, repeat=repeat)


class ExplosionSound:
    def __init__(self, galacticUnicorn, sound_service):
        self.galacticUnicorn = galacticUnicorn
        self.notes = [600, 700, 800, 900, 1000]
        self.sound_service = sound_service

        self.channels = self.set_channels()

    def set_channels(self):
        channels = [self.galacticUnicorn.synth_channel(0)]
        channels[0].configure(
            waveforms=Channel.NOISE,
            attack=0.01,
            decay=0.4,
            sustain=0.2,
            release=0.5,
            volume=self.sound_service.get_current_volume(),
        )
        return channels

    def play(self, bpm=120, repeat=False):
        self.channels = self.set_channels()
        explosion = random.choice(self.notes)
        self.sound_service.play_notes(
            [[explosion]], self.channels, bpm=bpm, repeat=repeat
        )


class FireplaceSound:
    def __init__(self, galacticUnicorn, sound_service):
        self.galacticUnicorn = galacticUnicorn
        self.sound_service = sound_service
        self.channels = self.set_channels()

    def set_channels(self):
        channels = [self.galacticUnicorn.synth_channel(0)]
        channels[0].configure(
            waveforms=Channel.NOISE,
            attack=0,
            decay=0,
            sustain=0.1,
            release=0,
            volume=self.sound_service.get_current_volume() * 0.3,
        )

        return channels

    def play(self, repeat=True):
        self.channels = self.set_channels()
        random_bpm = random.randint(120, 480)
        white_noise_note = [2000] * random.randint(2, 12)
        self.sound_service.play_notes(
            [white_noise_note], self.channels, bpm=random_bpm, repeat=repeat
        )


class FireworkSound:
    def __init__(self, galacticUnicorn, sound_service):
        self.galacticUnicorn = galacticUnicorn
        self.sound_service = sound_service

        self.channels = self.set_channels()

        self.explosion_sounds = [
            [800, 850, 900, 950, 1000, -1, -1],
            [1000, 1050, 1100, 1150, 1200, -1, -1],
            [600, 650, 700, 750, 800, -1, -1],
            [1100, 1150, 1200, 1250, 1300, -1, -1],
            [700, 750, 800, 850, 900, -1, -1],
        ]

    def set_channels(self):
        channels = [self.galacticUnicorn.synth_channel(0)]
        channels[0].configure(
            waveforms=Channel.NOISE,
            attack=0.005,
            decay=0.500,
            sustain=0,
            release=0.100,
            volume=self.sound_service.get_current_volume(),
        )
        return channels

    def play(self, bpm=700, repeat=False):
        self.channels = self.set_channels()
        selected_sound = random.choice(self.explosion_sounds)
        self.sound_service.play_notes(
            [selected_sound], self.channels, bpm=bpm, repeat=repeat
        )


class RaindropsSound:
    def __init__(self, galacticUnicorn, sound_service):
        self.notes = [800, 810, 820]
        self.sound_service = sound_service
        self.galacticUnicorn = galacticUnicorn
        self.channels = self.set_channels()

    def set_channels(self):
        channels = [self.galacticUnicorn.synth_channel(0)]
        channels[0].configure(
            waveforms=Channel.NOISE,
            attack=0.005,
            decay=0.500,
            sustain=0,
            release=0.100,
            volume=self.sound_service.get_current_volume(),
        )
        return channels

    def play(self, bpm=820, repeat=True):
        self.channels = self.set_channels()
        self.sound_service.play_notes(
            [self.notes], self.channels, bpm=bpm, repeat=repeat
        )


class SirenSound:
    def __init__(self, galacticUnicorn, sound_service):
        self.galacticUnicorn = galacticUnicorn
        self.sound_service = sound_service
        self.channels = self.set_channels()

        self.tone_a = 600
        self.tone_b = 700
        self.siren_notes = [self.tone_a, 0, 0, 0, self.tone_b, 0, 0, 0]

    def set_channels(self):
        channels = [self.galacticUnicorn.synth_channel(0)]
        channels[0].configure(
            waveforms=Channel.SINE + Channel.TRIANGLE,
            attack=0.01,
            decay=0.1,
            sustain=0.8,
            release=0.1,
            volume=self.sound_service.get_current_volume(),
        )
        return channels

    def play(self, bpm=240, repeat=True):
        self.channels = self.set_channels()
        self.sound_service.play_notes(
            [self.siren_notes], self.channels, bpm=bpm, repeat=repeat
        )

    def play_tone_a(self, bpm=240, repeat=True):
        self.channels = self.set_channels()
        self.sound_service.play_notes(
            [[self.tone_a, 0, 0, 0]], self.channels, bpm=bpm, repeat=repeat
        )

    def play_tone_b(self, bpm=240, repeat=True):
        self.channels = self.set_channels()
        self.sound_service.play_notes(
            [[self.tone_b, 0, 0, 0]], self.channels, bpm=bpm, repeat=repeat
        )


class ThunderSound:
    def __init__(self, galacticUnicorn, sound_service):
        self.galacticUnicorn = galacticUnicorn
        self.sound_service = sound_service

        self.channels = self.set_channels()

    def set_channels(self):
        channels = [self.galacticUnicorn.synth_channel(0)]
        channels[0].configure(
            waveforms=Channel.NOISE,
            attack=0.005,
            decay=0.010,
            sustain=65535 / 65535,
            release=0.100,
            volume=self.sound_service.get_current_volume(),
        )
        return channels

    # Plays a random thunder sound
    def play(self, repeat=False):
        self.channels = self.set_channels()
        random_notes = [random.randint(500, 5000) for _ in range(10)]
        random_bpm = random.choice([random.randint(550, 650), random.randint(430, 530)])
        self.sound_service.play_notes(
            [random_notes], self.channels, bpm=random_bpm, repeat=repeat
        )
