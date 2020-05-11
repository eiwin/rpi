
import serial

serialport = serial.Serial('/dev/serial0', baudrate=9600, timeout=3.0)

while True:
    str = input('say something: ')
    serialport.write(str.encode())
    rcv = serialport.read(4).decode("utf-8")
    print(rcv)
    if('exit'==rcv):
        break
    #serialport.write(("You sent:" + repr(rcv)).encode())
