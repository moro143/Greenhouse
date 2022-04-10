import dht
import machine

def temperature_humidity(pin_num=5):
    d = dht.DHT11(machine.Pin(pin_num))
    d.measure()
    temp = d.temperature()
    hum = d.humidity()
    return temp, hum

def soil_humidity(pin_num=0):
    adc = machine.ADC(pin_num)
    result = adc.read()
    return result