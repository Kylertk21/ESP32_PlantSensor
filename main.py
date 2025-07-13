from machine import Pin, I2C
from oled_lib import SSD1306_I2C
from moisture_lib import read_moisture
import time
from datetime import datetime
import network, urequests
SENSOR_ID= 1
API_URL = "http://192.168.0.19:5000/api/sensor"

SSID = "Die_Online"
PASSWORD = "AKConquest420!"

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("connecting to network...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    print("connected:", wlan.ifconfig())


def post_data(water_value):
    try:
        payload = {
            "sensor_id": SENSOR_ID,
                "readings": {
                "water": water_value,
                "time": datetime.now()
                
            }
        }
        headers = {'Content-Type': 'application/json'}
        response = urequests.post(API_URL, data=payload, headers=headers)
        print(response.text)
        response.close()
    except Exception as e:
        print("Error", e)

while True:
    moisture = read_moisture()
    oled.fill(0)
    oled.text(moisture,0 , 0)
    oled.show()
    time.sleep(1)