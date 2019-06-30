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

from ws2812 import *

from izaber import initialize, config

from PIL import Image, ImageFilter, ImageFont, ImageDraw

if __name__ == "__main__":
    spi = spidev.SpiDev()
    spi.open(1,0)

    LEDS = 121
    strip = Strip(spi,LEDS)

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

    while True:
        im = Image.new("RGB",(w+12,11), "black")
        d = ImageDraw.Draw(im)

        now = datetime.datetime.now()
        r=g=b=50
        d.text((0,0), now.strftime("%H"), font=fnt, fill=(r,g,b))
        d.text((0,6), now.strftime("%M"), font=fnt, fill=(r,g,b))

        for x in range(11):
            for y in range(11):
                (r,g,b) = im.getpixel((x,y))

                if r==0 and b==0 and g==0:
                    offset = x * 2 + y * 2
                    frame[x][y].set_hsv((counter+offset)%360,255,20)
                else:
                    frame[x][y].r = r
                    frame[x][y].g = g
                    frame[x][y].b = b


        strip.commit()
        time.sleep(.01)
        counter += 1


