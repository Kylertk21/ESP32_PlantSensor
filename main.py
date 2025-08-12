from machine import Pin, I2C
import machine
from oled_lib import SSD1306_I2C
from moisture_lib import read_moisture
from light_lib import BH1750
import time
import network, urequests
SENSOR_ID= "Basil"
API_URL = "http://192.168.0.19:5000/api/sensor"

SSID = "Die_Online"
PASSWORD = "AKConquest420!"
wlan = network.WLAN(network.STA_IF)
ip_address = wlan.ifconfig()[0]

i2c = I2C(0, scl=Pin(21), sda=Pin(22))
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

def connect_wifi():
    wlan.active(True)
    if not wlan.isconnected():
        print("connecting to network...")
        wlan.connect(SSID, PASSWORD)

        for _ in range(10):
            if wlan.isconnected():
                break
            time.sleep(1)
        else:
            print("Failed to connect")
            return False

    print("connected:", wlan.ifconfig())
    return True

def read_light():
    light_sensor = BH1750(i2c)
    lux = light_sensor.luminance()
    relative_light = light_sensor.map_value(lux)
    return relative_light


def post_data(water_value, sunlight_value):
    try:
        payload = {
            "sensor_id": SENSOR_ID,
                "readings": {
                "water": water_value,
                "sunlight": sunlight_value,
            }
        }
        headers = {'Content-Type': 'application/json'}
        response = urequests.post(API_URL, json=payload, headers=headers)
        print(response.text)
        response.close()
        return True
    except Exception as e:
        print("Error", e)
        return False

def populate_screen(moisture_value, light_value, connected, posted):
    oled.fill(0)
    oled.text(f"{SSID if connected else 'No Conn'}", 0, 0)
    oled.text(f"IP: {ip_address if connected else ""}", 0, 50)
    oled.text("U" if posted else "N", 100, 0)
    oled.text(f"M: {moisture_value}", 0, 20)
    oled.text(f"L: {light_value}", 0, 30)
    oled.show()

wifi_connected = connect_wifi()

while True:
    light = read_light()
    moisture = read_moisture()
    post_success = post_data(moisture, light)
    populate_screen(moisture, light, wifi_connected, post_success)

    sleep_time = 600 * 1000 #10 mins
    machine.deepsleep(sleep_time)