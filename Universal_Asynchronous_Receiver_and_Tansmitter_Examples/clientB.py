from UART_Python_Lib import *

my_transmission = MyTransmissionProtocol("/dev/ttyUSB1")

my_transmission.write_json({
    "me": 21,
    "you": 21,
    "someone": 100
})
exit()

while 1:
    byte = my_transmission.read_safely()
    print(byte)
    sleep(0.5)
