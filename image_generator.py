#!/usr/bin/env python3

import sys
from PIL import Image, ImageDraw, ImageFont
import requests
import re
from icmplib import ping
from datetime import datetime


class Panel:
    def __init__(self):
        # non-margined image size
        img_x = 264
        img_y = 176
        
        # usable area /w margins applied
        margin = 5
        self.max_x = img_x - margin
        self.max_y = img_y
        
        self.img = Image.new('RGB', (img_x, img_y), color = (255, 255, 255))
        
        # 2. Get a drawing context
        self.draw = ImageDraw.Draw(self.img)
        self.text_color = (0, 0, 0) # Black color

    def add(self, coords, content, font=""):
        self.draw.text(coords, content, fill = self.text_color, font = font)
        return self.draw.textlength(content, font = font)

    def estimate(self, content, font=""):
        return self.draw.textlength(content, font = font)

    def save(self):
        self.img.save("output_image_with_text.png")
        
    def save_and_show(self):
        self.save()
        self.img.show() # Opens the image in the system's default image viewer

class Font:
    def __init__(self, path):
        self.path = path
        self.cache = {}
    def size(self, size=20):
        if size in self.cache:
            return self.cache[size]
        try:
            self.cache[size] = ImageFont.truetype(self.path, size)
        except IOError:
            print(f"Error: Could not load font at {self.path}")
            sys.exit(1)
        return self.cache[size]

icosolid = Font("fonts/fa/Font Awesome 7 Free-Solid-900.otf")
icoreg = Font("fonts/fa/Font Awesome 7 Free-Regular-400.otf")
#fontreg = Font("fonts/google/WalterTurncoat-Regular.ttf")
fontreg = Font("fonts/google/Amarante-Regular.ttf")

panel = Panel()
panel.add((5, 5), "Meadowbrook", font=fontreg.size())

host = ping("8.8.8.8", privileged=False)
ico = "\uF1EB"
rtt = int(host.avg_rtt)
txt = f"{rtt}ms"
width = 8 + panel.estimate(ico, font=icosolid.size(28)) + panel.estimate(txt, font=fontreg.size(28))
x = panel.max_x - width
x += panel.add((x, 5), ico, font=icosolid.size(28))
x += 8
x += panel.add((x, 3), txt, font=fontreg.size(28))


# if no ping
#panel.add( (190, 10), '\uF05E', font=icosolid.size())

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
    feels = round(data['main']['feels_like'])
    description = data['weather'][0]['description']
    sunrise = data['sys']['sunrise']
    sunset = data['sys']['sunset']
except Exception as e:
    print(e)

x = 30
x += panel.add ((x, 36), f"{feels}°", font=fontreg.size(70))
x -= 4

if re.search("(broken|few) cloud", description, flags=re.IGNORECASE):
    x += panel.add((x, 50), "\uF0C2", font = icoreg.size(60)) # cloud
    
elif re.search("cloud", description, flags=re.IGNORECASE):
    x += panel.add((x, 50), "\uF0C2", font =icosolid.size(60)) # solid cloud
    
elif re.search("light snow", description, flags=re.IGNORECASE):
    x += panel.add((x, 50), "\uf2dc", font =icoreg.size(60)) # solid snowflake
    
elif re.search("snow", description, flags=re.IGNORECASE):
    x += panel.add((x, 50), "\uf2dc", font =icosolid.size(60)) # snowflake
    
else:
    x += panel.add((x, 50), "\uf057", font =icosolid.size(60))

time = datetime.fromtimestamp(sunrise).strftime('%I:%M %p')
time = time.lstrip("0")
ico = "\uf106" # arrow up
txt = f"{time}"
width = panel.estimate(txt, font = fontreg.size()) + panel.estimate(ico, icosolid.size())
x = panel.max_x - width
x += panel.add((x, 120), txt, font = fontreg.size())
panel.add((x, 120), ico, font = icosolid.size())

time = datetime.fromtimestamp(sunset).strftime('%I:%M %p')
time = time.lstrip("0")
ico = "\uf107" # arrow down
txt = f"{time}"
width = panel.estimate(txt, font = fontreg.size()) + panel.estimate(ico, icosolid.size())
x = panel.max_x - width
x += panel.add((x, 140), txt, font = fontreg.size())
panel.add((x, 140), ico, font = icosolid.size())

time = datetime.now().strftime('%I:%M %p')
panel.add((0, 120), time.lstrip("0"), font = fontreg.size(40))

print(f"temp {temperature} / {description}")

panel.save()


