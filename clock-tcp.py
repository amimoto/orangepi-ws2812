#!/usr/bin/python3

"""
Offers support for WS2812 LED LEDs via the hardware SPI MOSI

Uses py-spidev:

```
git clone https://github.com/doceme/py-spidev.git
cd py-spidev
make
make install
```

"""

import time
import datetime
import socket
import math

from izaber import initialize, config

from PIL import Image, ImageFilter, ImageFont, ImageDraw


class LED:
    def __init__(self,r=0,g=0,b=0):
        self.set_rgb(r,g,b)

    def set_rgb(self,r,g,b):
        self.r = r
        self.g = g
        self.b = b

    def set_hsv(self,h=0,s=0,v=0):
        """ Pinched from ActiveState Code » Recipes 
            http://code.activestate.com/recipes/576919-python-rgb-and-hsv-conversion/
        """
        s = float(s/255)
        v = float(v)

        h = h - math.floor(h/360)*360

        h60 = float(h) / 60.0
        h60f = math.floor(h60)
        hi = int(h60f) % 6
        f = h60 - h60f
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        r, g, b = 0, 0, 0
        if hi == 0: r, g, b = v, t, p
        elif hi == 1: r, g, b = q, v, p
        elif hi == 2: r, g, b = p, v, t
        elif hi == 3: r, g, b = p, q, v
        elif hi == 4: r, g, b = t, p, v
        elif hi == 5: r, g, b = v, p, q

        self.r = int(r)
        self.g = int(g)
        self.b = int(b)

    def __bytes__(self):
        return bytes([self.r, self.g, self.b])

    def __str__(self):
        return f"{self.r},{self.g},{self.b}"

class Strip:
    def __init__(self,host,port,leds):
        self.leds = [ LED() for i in range(leds) ]
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host,port))

    def commit(self):
        data = bytes(self)
        self.socket.send(data)

    def set_all_rgb(self,r,g,b):
        for led in self.leds:
            led.set_rgb(r,g,b)

    def set_all_hsv(self,h,s,v):
        for led in self.leds:
            led.set_hsv(h,s,v)

    def __bytes__(self):
        tx = bytes()
        for rgb in self.leds:
            tx += bytes(rgb)
        return tx

    def __getitem__(self,i):
        return self.leds[i]

    def __setitem__(self,i,v):
        self.leds[i] = v

if __name__ == "__main__":
    LEDS = 121
    strip = Strip('10.4.10.96',23,LEDS)

    frame = [
                [
                    strip[x*11+y] for y in range(11)
                ] for x in range(11)
            ]

    for i in range(11):
        if i % 2 == 0:
            frame[i].reverse()

    # From: http://www.vectorilla.com/2010/01/23-totally-free-small-fonts-pixel-fonts/
    fnt = ImageFont.truetype('fonts/notalot/notalot25.ttf', 8)

    w = 10

    counter = 0;
    counter_range = 360

    start_time = datetime.datetime.now()

    while True:
        im = Image.new("RGB",(w+12,11), "black")
        d = ImageDraw.Draw(im)

        now = datetime.datetime.now()
        r=g=b=255
        d.text((0,0), now.strftime("%H"), font=fnt, fill=(r,g,b))
        d.text((0,6), now.strftime("%M"), font=fnt, fill=(r,g,b))

        for x in range(11):
            for y in range(11):
                (r,g,b) = im.getpixel((x,y))

                if r==0 and b==0 and g==0:
                    s = now.second + now.microsecond * 1e-6
                    theta = s/60 * 2 * math.pi + math.pi / 2
                    cx = math.cos(theta) * 4
                    cy = math.sin(theta) * 4
                    offset = 600-math.sqrt((x-5+cx)**2 + (y-5+cy)**2) * 5
                    frame[x][y].set_hsv((counter+offset)%360,255,10)
                else:
                    frame[x][y].r = r
                    frame[x][y].g = g
                    frame[x][y].b = b

        strip.commit()
        counter += 1
        time.sleep(0.02)

        if counter % 100 == 0:
            delta = now - start_time
            fps = counter / delta.total_seconds()
            print(f"FPS: {fps:0.2f}")


