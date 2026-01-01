#!/usr/bin/env python3

import epaper
from PIL import Image

print("getting image")
filename = "./output_image_with_text.png"
png = Image.open(filename)


print("getting epd")
epd = epaper.epaper('epd2in7_V2').EPD()

print("init")
epd.init()
print("clear")
epd.Clear()

print("displaying image")
epd.display(epd.getbuffer(png))
