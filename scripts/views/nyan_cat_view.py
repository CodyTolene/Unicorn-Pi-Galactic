# Cody Tolene
# Apache License 2.0

import uasyncio
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY


class NyanCat:
    def __init__(self, galacticUnicorn, graphics, sound):
        self.frame_index = 0
        self.galacticUnicorn = galacticUnicorn
        self.graphics = graphics
        self.sound = sound

    def display_frame(self, frame):
        for y, row in enumerate(frame):
            for x, char in enumerate(row):
                color = color_key.get(char, (0, 0, 0))
                pen = self.graphics.create_pen(*color)
                self.graphics.set_pen(pen)
                self.graphics.pixel(x, y)
        self.galacticUnicorn.update(self.graphics)

    async def update(self):
        self.graphics.set_pen(self.graphics.create_pen(0, 0, 0))
        self.graphics.clear()

        self.display_frame(frames[self.frame_index])
        self.frame_index = (self.frame_index + 1) % len(frames)


async def run(galacticUnicorn, graphics, sound):
    nyan_cat = NyanCat(galacticUnicorn, graphics, sound)

    while True:
        await nyan_cat.update()
        await uasyncio.sleep(0.1)


color_key = {
    "R": (255, 0, 0),  # Red
    "O": (255, 165, 0),  # Orange
    "Y": (255, 255, 0),  # Yellow
    "G": (0, 255, 0),  # Green
    "B": (0, 0, 255),  # Blue
    "I": (75, 0, 130),  # Indigo
    "V": (238, 130, 238),  # Violet
    "W": (255, 255, 255),  # White
    "C": (0, 255, 255),  # Cyan
    "P": (255, 192, 203),  # Pink
    " ": (0, 0, 0),  # Black (space)
}

frames = [
    [
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "OOOOORRRRRRROOOOORRIPPVVVVVVVVVVPP IIIIIIIIIIIIIIIIII",
        "YYYYYOOOOOOYYYYOOYOIPVVVVVVVIIIVVP III IIIIIIIIIIIIII",
        "GGGGGYYYYYYGGGGIIOOIPVVVVVVVIPPIIIIPVVI IIIIIIIIIIIII",
        "CCCCCCCCCCCCCCCBIIIIPVVVVVVIVPVIVIIIIPI IIIIIIIIIIIII",
        "BBBBBBBBBBBBBBBBBBIIIVIVIIVIIIIII IIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIII IIIII IIII     I  IIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
    ],
    [
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIII  I   IIIIIIIIIIIIIIIIIIIII",
        "RRRRRRROOOOORRRRRRRRPPVVVVVVVVVVPP IIIIIIIIIIIIIIIIII",
        "OOOOOOYYYYYYOOOOOOOIPVVVVVVVVIVVVP  II IIIIIIIIIIIIII",
        "YYYYYYGGGGGGYYYYYYGIPVVVVVVVIPPIIIIVPI IIIIIIIIIIIIII",
        "CCCCCCCCCCCCCCG II IPVVVVVVIVPVIPVIVIPI IIIIIIIIIIIII",
        "BBBBBBBBBBBBBBBIIII PPVVVVVVIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIII I   I  II  I   I  IIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
    ],
    [
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIII   I   IIIIIIIIIIIIIIIIIIIII",
        "RRRRRROOOOORRRRRRRRRPPVVVVVVVVVVPP IIIIIIIIIIIIIIIIII",
        "OOOOOYYYYYYOOOOOOYOIPVVVVVVVVIVVVP  II IIIIIIIIIIIIII",
        "YYYYYGGGGGGYYYYYYGGIPVVVVVVVIPPIIIIVPI IIIIIIIIIIIIII",
        "CCCCCCCCCCCCCCGGIIIIPVVVVVVIVPVIPVIVIPI IIIIIIIIIIIII",
        "BBBBBBBBBBBBBBBIIIIIPPVVVVVVIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIII II  I   II II  I  IIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
    ],
    [
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIII      I   IIIIIIIIIIIIIIIIIIIII",
        "OOOOOORRRRRRROOOOORIPPVVVVVVVVVVPP IIIIIIIIIIIIIIIIII",
        "YYYYYYOOOOOOYYYYYYOIPVVVVVVVIVVVVP II IIIIIIIIIIIIIII",
        "GGGGGGYYYYYYGGIIIGOIPVVVVVVIVPIIIIIPP  IIIIIIIIIIIIII",
        "CCCCCCCCCCCCCCBBIIIIPVVVVVIIPPIVPIPIVV IIIIIIIIIIIIII",
        "BBBBBBBBBBBBBBBBBII PPVVVVVIIVIIIIIIII IIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIII III I  I II I   I IIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
    ],
    [
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIII      II  IIIIIIIIIIIIIIIIIIIII",
        "OOOOORRRRRRROOOOORRIPPVVVVVVVVVVPP IIIIIIIIIIIIIIIIII",
        "YYYYYOOOOOOYYYYOOYOIPVVVVVVIIIVVVP II IIIIIIIIIIIIIII",
        "GGGGGYYYYYYGGGGIIOOIPVVVVVVIPPIIIIPPVI IIIIIIIIIIIIII",
        "CCCCCCCCCCCCCCCBIIIIPVVVVVIIPPIIIIIIPV IIIIIIIIIIIIII",
        "BBBBBBBBBBBBBBBBBII PPVVVVVVIIII IIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIII III  I I II     I IIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
    ],
    [
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "RRRRRRROOOOORRRRRRRIPPVVVVVVVVVVPP IIIIIIIIIIIIIIIIII",
        "OOOOOOYYYYYYOOOOOOOIPVVVVVVIIIVVVP II IIIIIIIIIIIIIII",
        "YYYYYYGGGGGGYYG II IPVVVVVVIPPIIIIPPVI IIIIIIIIIIIIII",
        "CCCCCCCCCCCCCCCCIIIIPVVVVVIIPPIIIIIIPV IIIIIIIIIIIIII",
        "BBBBBBBBBBBBBBBBBBIIIIIVVVIIIIII IIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIII     IIII I III IIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
    ],
    [
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "RRRRRROOOOORRRRRRRRIPPVVVVVVVVVVPP IIIIIIIIIIIIIIIIII",
        "OOOOOYYYYYYOOOOOOYOIPVVVVVVVIIIVVP III IIIIIIIIIIIIII",
        "YYYYYGGGGGGYYYGIIGGIPVVVVVVVIPPIIIIPVVI IIIIIIIIIIIII",
        "CCCCCCCCCCCCCCCCIIIIPVVVVVVIVPVIVIIIIPI IIIIIIIIIIIII",
        "BBBBBBBBBBBBBBBBBBIIIIIVIVVIIIIII IIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIII I      III     I  IIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
    ],
    [
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIII  I   IIIIIIIIIIIIIIIIIIIII",
        "OOOOOORRRRRRROOOOORIPPVVVVVVVVVVPP IIIIIIIIIIIIIIIIII",
        "YYYYYYOOOOOOYYYYYYOIPVVVVVVVVIVVVP  II IIIIIIIIIIIIII",
        "GGGGGGYYYYYYGGGGGGGIPVVVVVVVIPPIIIIVPI IIIIIIIIIIIIII",
        "CCCCCCCCCCCCCCIIII IPVVVVVVIVPVIPVIVIPI IIIIIIIIIIIII",
        "BBBBBBBBBBBBBBBIIIIIPPVVVVVVIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIII I   I  II  I III  IIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
    ],
    [
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIII      I   IIIIIIIIIIIIIIIIIIIII",
        "OOOOORRRRRRROOOOORRIPPVVVVVVVVVVPP IIIIIIIIIIIIIIIIII",
        "YYYYYOOOOOOYYYYYYYOIPVVVVVVVVIVVVP  II IIIIIIIIIIIIII",
        "GGGGGYYYYYYGGGGGGYOIPVVVVVVVIPPIIIIVPI IIIIIIIIIIIIII",
        "CCCCCCCCCCCCCCCIIIIIPVVVVVVIVPVIPVIVIPI IIIIIIIIIIIII",
        "BBBBBBBBBBBBBBIIIIIIPPVVVVVVIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIII II  I  IIII I  I  IIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
    ],
    [
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIII  I   IIIIIIIIIIIIIIIIIIIII",
        "RRRRRRROOOOORRRRRRRRPPVVVVVVVVVVPP IIIIIIIIIIIIIIIIII",
        "OOOOOOYYYYYYOOOOOOOIPVVVVVVVIVVVVP II IIIIIIIIIIIIIII",
        "YYYYYYGGGGGGYYOOIO IPVVVVVVIVPIIIIIPP  IIIIIIIIIIIIII",
        "CCCCCCCCCCCCCCCIBIIIPVVVVVIIPPIVPIPIVV IIIIIIIIIIIIII",
        "BBBBBBBBBBBBBBBBBIIIPPVVVVVIIVIIIIIIII IIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIII I   I IIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
    ],
    [
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIII  III  IIIIIIIIIIIIIIIIIIIII",
        "RRRRRROOOOORRRRRRRRRPPVVVVVVVVVVPP IIIIIIIIIIIIIIIIII",
        "OOOOOYYYYYYOOOOOOYOIPVVVVVVIIIVVVP II IIIIIIIIIIIIIII",
        "YYYYYGGGGGGYYYGIIGGIPVVVVVVIPPIIIIPPVI IIIIIIIIIIIIII",
        "CCCCCCCCCCCCCCCCIIIIPVVVVVIIPPIIIIIIPV IIIIIIIIIIIIII",
        "BBBBBBBBBBBBBBBBBIIIPPVVVVVVIIII IIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIII  I I II     I IIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
    ],
]

# This section of code is only for testing.
if __name__ == "__main__":
    galacticUnicorn = GalacticUnicorn()
    graphics = PicoGraphics(display=DISPLAY)
    uasyncio.run(run(galacticUnicorn, graphics))
