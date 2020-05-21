import serial
import time
import datetime

DEBUG = 0

class LCDUart():
    def __init__(self):
        self.serialport = serial.Serial('/dev/serial0', baudrate=9600, timeout=3.0)
        self.current_line = 1

    def lcd_config(self):
        # config the Baud rate
        self.serialport.write(b'\xfe\x61\x04')
        # display on
        self.serialport.write(b'\xfe\x41')
        # config contrast
        self.serialport.write(b'\xfe\x52\x20')
        # config backlight brightness
        self.serialport.write(b'\xfe\x53\x05')

    def lcd_clear(self):
        self.serialport.write(b'\xfe\x51')

    def lcd_write(self, c):
        if c=='\n':
            if 1==self.current_line:
                self.serialport.write(b'\xfe\x45\x40')
            elif 2==self.current_line:
                self.serialport.write(b'\xfe\x45\x14')
            elif 3==self.current_line:
                self.serialport.write(b'\xfe\x45\x54')
            elif 4==self.current_line:
                self.serialport.write(b'\xfe\x45\x00')
            self.current_line +=1
            if 4<self.current_line:
                self.current_line = 1
        else:
            self.serialport.write(c.encode())
        
    def lcd_display_temperature(self, t, pos=0x41):
        str_t = "Temp: %0.1f " % t
        if DEBUG:
            print(str_t)
        cmd = bytearray(b'\xfe\x45')
        cmd.append(pos)
        self.serialport.write(cmd)
        self.serialport.write(str_t.encode())
        # display unit
        self.serialport.write(b'\xdf\x43')
        
    def lcd_display_humidity(self, h, pos=0x15):
        str_h = "Humd: %0.1f %%" % h
        if DEBUG:
            print(str_h)
        cmd = bytearray(b'\xfe\x45')
        cmd.append(pos)
        self.serialport.write(cmd)
        self.serialport.write(str_h.encode())
        
    def lcd_display_pressure(self, p, pos=0x55):
        str_p = "Pres: %0.1f hPa" % p
        if DEBUG:
            print(str_p)
        cmd = bytearray(b'\xfe\x45')
        cmd.append(pos)
        self.serialport.write(cmd)
        self.serialport.write(str_p.encode())

    def lcd_display_info(self, pos=0x00):
        currentDT = datetime.datetime.now()
        str = currentDT.strftime("%Y/%m/%d %H:%M:%S")
        #str = "Designed by CRS"
        if DEBUG:
            print(str)
        cmd = bytearray(b'\xfe\x45')
        cmd.append(pos)
        self.serialport.write(cmd)
        self.serialport.write(str.encode())
        
    def lcd_display_sensor_data(self):
        # lcd_clear()
        lcd_display_temperature(bme280.temperature)
        lcd_display_humidity(bme280.humidity)
        lcd_display_pressure(bme280.pressure)
        lcd_display_info()
        
