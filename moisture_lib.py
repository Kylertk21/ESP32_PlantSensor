from machine import ADC, Pin
import time
AOUT_PIN = 34

def map_value(value):
    wet_value = 1500
    dry_value = 3200
    
    moisture_percent = (dry_value - value) * 100// (dry_value - wet_value)
    moisture_percent = max(0, min(100, moisture_percent))
    
    if moisture_percent >= 80:
        label = "Wet"
    elif moisture_percent >= 50:
        label = "Moist / Wet"
    elif moisture_percent >= 35:
        label = "Moist"
    elif moisture_percent >= 20:
        label = "Dry / Moist"
    else:
        label = "Dry"

    print(moisture_percent)
    return label


def read_moisture():
    moisture_sensor = ADC(Pin(AOUT_PIN))
    moisture_sensor.width(ADC.WIDTH_12BIT)
    moisture_sensor.atten(ADC.ATTN_11DB)

    while True:
        time.sleep(1)
        value = moisture_sensor.read()
        label = map_value(value)

        return label

    '''
    1500- very wet
    1600+ wet
    2800+ pretty wet
    3000+ dry
    3200+ very dry 
    '''

