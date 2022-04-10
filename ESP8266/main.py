import machine
import time

RED_LED = machine.Pin(14, machine.Pin.OUT)

import connection
try:
    s = connection.connect('###.###.###.###')
    while True:
        msg = connection.get_message(s)
        
except:
    while True:
        RED_LED.value(1)
        time.sleep(1)
        RED_LED.value(0)
        time.sleep(1)