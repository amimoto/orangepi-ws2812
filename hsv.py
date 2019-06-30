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

# These didn'tw ork
# SEND_HZ = 3700000
# SEND_HZ = 3900000
# SEND_HZ = 4000000
# SEND_HZ = 4100000
# SEND_HZ = 3400000
# SEND_HZ = 3800000
# SEND_HZ = 3750000
# SEND_HZ = 3800000
# SEND_HZ = 7600000

# But this did
SEND_HZ = 6000000

# Precalculate all the byte values to bytestrings for
# fast lookup to send over the SPI bus
SEND_0 = bytes([0b1000000])
SEND_1 = bytes([0b1111110])

spi_bytes = []
for i in range(256):
    entry_bytes = bytes()
    for bit in range(7,-1,-1):
        entry_bytes += SEND_1 if (i>>(bit))&1 else SEND_0
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
        tx = bytes([0])
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

    LEDS = 121

    strip = Strip(spi,LEDS)
    i = 229
    i = 233
    i = 0

    leds_up_to = 1
    while True:
        print(i)

        leds_up_to = int(i / 2)+1
        if leds_up_to > LEDS:
            leds_up_to = LEDS

        for j in range(LEDS):
            if j > leds_up_to:
                strip[j].set_rgb(0,0,0)
            else:
                strip[j].set_hsv((i+j*2)%360,255,20)

        strip.commit()
        #time.sleep(0.01)
        #time.sleep(1)
        #time.sleep(0.1)
        i += 1

