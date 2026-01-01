#!/usr/bin/env python3

from PIL import Image, ImageDraw

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

