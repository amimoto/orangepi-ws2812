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

import spidev
import time
import datetime
import math

from izaber import initialize, config

SEND_HZ = int(4/1.05e-6)

# Precalculate all the byte values to bytestrings for
# fast lookup to send over the SPI bus
spi_bytes = []
for i in range(256):
    entry_bytes = bytes()
    for bit in range(3,-1,-1):
        v = 0b10001000 \
            | ((i>>(2*bit+1)&1) and 0b01100000 or 0) \
            | ((i>>(2*bit)&1) and 0b00000110 or 0)
        entry_bytes += bytes([v])
    spi_bytes.append(entry_bytes)

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

        h = h/255*360
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
        return bytes() \
                + spi_bytes[self.g] \
                + spi_bytes[self.r] \
                + spi_bytes[self.b]

    def __str__(self):
        return f"{self.r},{self.g},{self.b}"

class Strip:
    def __init__(self,spi,leds):
        self.leds = list(map(LED, range(leds)))
        self.spi = spi

    def commit(self):
        self.spi.xfer(bytes(self), SEND_HZ)

    def set_all_rgb(self,r,g,b):
        for led in self.leds:
            led.set_rgb(r,g,b)

    def set_all_hsv(self,h,s,v):
        for led in self.leds:
            led.set_hsv(h,s,v)

    def __bytes__(self):
        tx = bytes([0,0])
        for rgb in self.leds:
            tx += bytes(rgb)
        return tx

    def __getitem__(self,i):
        return self.leds[i]

    def __setitem__(self,i,v):
        self.leds[i] = v

if __name__ == "__main__":
    spi = spidev.SpiDev()
    spi.open(1,0)

    strip = Strip(spi,8)

    i = 0
    while True:
        strip[0].set_hsv(i,255,50)
        strip[1].set_hsv(i+60,255,50)
        strip.commit()
        time.sleep(0.001)
        i += 0.1

