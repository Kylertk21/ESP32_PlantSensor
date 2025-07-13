from machine import ADC, Pin
import time
AOUT_PIN = 15

def read_moisture():
    moisture_sensor = ADC(Pin(AOUT_PIN))
    moisture_sensor.width(ADC.WIDTH_12BIT)
    moisture_sensor.atten(ADC.ATTN_11DB)

    while True:
        time.sleep(0.5)
        value = moisture_sensor.read()
        return "Moisture: {}".format(value)
