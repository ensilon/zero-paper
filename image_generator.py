#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
import requests
import re

# 1. Create a blank image (or open an existing one)
#    Mode "RGB", size (width, height), white background color
img = Image.new('RGB', (264, 176), color = (255, 255, 255))

# 2. Get a drawing context
draw = ImageDraw.Draw(img)

# 3. Load the TrueType font and specify the size
#    Replace 'path/to/your/font.ttf' with the actual path to your font file
try:
    font_path = "fonts/google/WalterTurncoat-Regular.ttf"
    font_size = 20
    icon_path = "fonts/fa/Font Awesome 7 Free-Solid-900.otf"
    icon_size = 20
    # The truetype function loads the font object
    font = ImageFont.truetype(font_path, font_size)
    icon = ImageFont.truetype(icon_path, icon_size)
    font_l = ImageFont.truetype(font_path, font_size + 10)
    icon_l = ImageFont.truetype(icon_path, icon_size + 10)
except IOError:
    print(f"Error: Could not load font at {font_path}. Using default font.")
    # Fallback to a default bitmap font if the file is not found (limited functionality)
    font = ImageFont.load_default()

# 4. Define text properties and draw the text
text = "Meadowbrook"
text_color = (0, 0, 0) # Black color
position = (10, 10) # Starting position (top-left corner of the text's bounding box)

draw.text(position, text, fill=text_color, font=font)
draw.text( (220, 10), "\uF1EB", fill=text_color,  font=icon)
draw.text( (190, 10), '\uF05E', fill=text_color,  font=icon)

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
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    description = data['weather'][0]['description']
    
    if re.search("cloud", description, flags=re.IGNORECASE):
        draw.text ((120,60), "\uF0C2", fill=text_color, font=icon_l)
    else:
        draw.text ((120,60), "\uF186", fill=text_color, font=icon_l)

    
    draw.text ((22,55), f"{temperature}", fill=text_color, font=font_l)
    print(f"temp {temperature} / hum {humidity} / {description}")
except Exception as e:
    print(e)
    
# 5. Save or display the image
img.save("output_image_with_text.png")
img.show() # Opens the image in the system's default image viewer

