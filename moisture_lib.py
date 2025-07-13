from machine import ADC, Pin
import time
AOUT_PIN = 34

def read_moisture():
    moisture_sensor = ADC(Pin(AOUT_PIN))
    moisture_sensor.width(ADC.WIDTH_12BIT)
    moisture_sensor.atten(ADC.ATTN_0DB)

    while True:
        time.sleep(0.5)
        value = moisture_sensor.read()
        return "{value}%".format(value=value)

