#!/usr/bin/env python3

import sys
from PIL import Image, ImageDraw, ImageFont
import requests
import re
from icmplib import ping


class Panel:
    def __init__(self):
        # 1. Create a blank image (or open an existing one)
        #    Mode "RGB", size (width, height), white background color
        self.max_x = 264
        self.max_y = 176
        self.img = Image.new('RGB', (self.max_x, self.max_y), color = (255, 255, 255))
        
        # 2. Get a drawing context
        self.draw = ImageDraw.Draw(self.img)
        self.text_color = (0, 0, 0) # Black color

    def add(self, coords, content, font=""):
        self.draw.text(coords, content, fill = self.text_color, font = font)
        return self.draw.textlength(content, font = font)

    def estimate(self, content, font=""):
        return self.draw.textlength(content, font = font)

    def save_and_show(self):
        # 5. Save or display the image
        self.img.save("output_image_with_text.png")
        self.img.show() # Opens the image in the system's default image viewer

# 3. Load the TrueType font and specify the size
#    Replace 'path/to/your/font.ttf' with the actual path to your font file
try:
    font_path = "fonts/google/WalterTurncoat-Regular.ttf"
    sicon_path = "fonts/fa/Font Awesome 7 Free-Solid-900.otf"
    ricon_path = "fonts/fa/Font Awesome 7 Free-Regular-400.otf"
    font_size = 20
    
    # The truetype function loads the font object
    font = ImageFont.truetype(font_path, font_size)
    font_l = ImageFont.truetype(font_path, font_size + 10)
    
    sicon = ImageFont.truetype(sicon_path, font_size)
    sicon_l = ImageFont.truetype(sicon_path, font_size + 10)
    
    ricon = ImageFont.truetype(ricon_path, font_size)
    ricon_l = ImageFont.truetype(ricon_path, font_size + 10)
except IOError:
    print(f"Error: Could not load font at {font_path}. Using default font.")
    sys.exit(1)


panel = Panel()
panel.add((10, 10), "Meadowbrook", font=font)

host = ping("8.8.8.8", privileged=False)
ico = "\uF1EB"
rtt = int(host.avg_rtt)
txt = f"{rtt}ms"
width = 8 + panel.estimate(ico, font=sicon) + panel.estimate(txt, font=font)
x = panel.max_x - width
x += panel.add((x, 12), ico, font=sicon)
x += 8
x += panel.add((x, 10), txt, font=font)


# if no ping
#panel.add( (190, 10), '\uF05E', font=sicon)

# weather
owm_apikey = "c236ac822c68d3cfc4b4dc11ac5b3a8c"
lat = "43.451291"
lon = "-80.4927815"
url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={owm_apikey}&units=metric"

try:
    response = requests.get(url)
    response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
    print(response.text)
    data = response.json()
    
    # Extracting relevant information
    temperature = round(data['main']['temp'])
    humidity = data['main']['humidity']
    description = data['weather'][0]['description']
        
    x = 22
    x += panel.add ((x, 55), f"{temperature}°", font=font_l)
    
    if re.search("broken cloud", description, flags=re.IGNORECASE):
        x += panel.add((x, 60), "\uF0C2", font = ricon_l)
        
    elif re.search("cloud", description, flags=re.IGNORECASE):
        x += panel.add((x, 60), "\uF0C2", font =sicon_l)

    else:
        x += panel.add((x, 60), "\uF0C2", font =sicon_l)

    txt = f"{humidity}%"
    ico = "\uF773"
    width = panel.estimate(txt, font = font_l) + panel.estimate(ico, sicon_l)
    x = panel.max_x - width
    x += panel.add ((x, 55), txt, font = font_l)
    x += panel.add ((x, 60), ico, font = sicon_l)

    print(f"temp {temperature} / hum {humidity} / {description}")
except Exception as e:
    print(e)

panel.save_and_show()


