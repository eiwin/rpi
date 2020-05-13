#  Raspberry Pi Master for Arduino Slave
#  i2c_master_pi.py
#  Connects to Arduino via I2C
  
#  DroneBot Workshop 2019
#  https://dronebotworkshop.com
import serial
import time
import datetime
serialport = serial.Serial('/dev/serial0', baudrate=9600, timeout=3.0)

from smbus import SMBus

addr = 0x8 # bus address
bus = SMBus(1) # indicates /dev/ic2-1

import board
import busio
import adafruit_bme280
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

numb = 1

def lcd_config():
    # config the Baud rate
    serialport.write(b'\xfe\x61\x04')
    # display on
    serialport.write(b'\xfe\x41')
    # config contrast
    serialport.write(b'\xfe\x52\x28')
    # config backlight brightness
    serialport.write(b'\xfe\x53\x05')

def lcd_clear():
    serialport.write(b'\xfe\x51')

def lcd_display_temperature(t, pos=0x00):
    str_t = "Temperature: %0.1f " % t
    cmd = bytearray(b'\xfe\x45')
    cmd.append(pos)
    serialport.write(cmd)
    serialport.write(str_t.encode())
    # display unit
    serialport.write(b'\xdf\x43')
    
def lcd_display_humidity(h, pos=0x40):
    str_h = "Humidity: %0.1f %%" % h
    cmd = bytearray(b'\xfe\x45')
    cmd.append(pos)
    serialport.write(cmd)
    serialport.write(str_h.encode())
    
def lcd_display_pressure(p, pos=0x14):
    str_p = "Pressure: %0.1f hPa" % p
    cmd = bytearray(b'\xfe\x45')
    cmd.append(pos)
    serialport.write(cmd)
    serialport.write(str_p.encode())

def lcd_display_info(pos=0x55):
    currentDT = datetime.datetime.now()
    str = currentDT.strftime("%H:%M:%S %Y-%m-%d")
    #str = "Designed by CRS"
    cmd = bytearray(b'\xfe\x45')
    cmd.append(pos)
    serialport.write(cmd)
    serialport.write(str.encode())
    
def lcd_display_sensor_data():
    # lcd_clear()
    lcd_display_temperature(bme280.temperature)
    lcd_display_humidity(bme280.humidity)
    lcd_display_pressure(bme280.pressure)
    lcd_display_info()
    
print ("System running...")
lcd_config()
lcd_clear()

ledstate = "0"
while True:
    #ledstate = input(">>>>   ")
    ledstate = int(ledstate)+1
    if(3<ledstate):
        ledstate = "0"
    ledstate = str(ledstate)
    time.sleep(1)
    lcd_display_sensor_data()
    
    if ledstate == "1":
        bus.write_byte(addr, 0x1) # switch it on
    elif ledstate == "2":
        bus.write_byte(addr, 0x2) # switch it on
    elif ledstate == "3":
        bus.write_byte(addr, 0x3) # switch it on
    elif ledstate == "55":
        bus.write_byte(addr, 0x55) # switch it on
    elif ledstate == "aa":
        bus.write_byte(addr, 0xaa) # switch it on

