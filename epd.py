#!/usr/bin/env python3

from epaper import epaper

class EPD:
    def __init__(self):
        self.epd27 = epaper('epd2in7_V2').EPD()

    def start(self):
        self.epd27.init()
        self.epd27.Clear()

    def refresh(self, image):
        self.epd27.Clear()
        self.epd27.display(epd.getbuffer(image))
