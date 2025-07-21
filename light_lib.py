# bh1750.py
import time
import struct

class BH1750:
    PWR_DOWN = 0x00
    PWR_ON = 0x01
    RESET = 0x07
    CONT_HIRES_MODE = 0x10

    def __init__(self, i2c, addr=0x23):
        self.i2c = i2c
        self.addr = addr
        self.buf = bytearray(2)

    def luminance(self, mode=CONT_HIRES_MODE):
        self.i2c.writeto(self.addr, bytes([mode]))
        time.sleep(0.180)
        self.i2c.readfrom_into(self.addr, self.buf)
        result = (self.buf[0] << 8 | self.buf[1]) / 1.2
        return result

    @staticmethod
    def map_value(value):
        if value >= 25000:
            return "Full Sun"
        elif 3000 <= value < 25000:
            return "Partial sun/shade"
        elif 100 <= value < 3000:
            return "Shade"
        else:
            return "Darkness"
