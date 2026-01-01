#!/usr/bin/env python3

from PIL import ImageFont

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

