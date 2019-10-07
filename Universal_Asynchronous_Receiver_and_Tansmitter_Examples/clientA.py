from UART_Python_Lib import *

my_transmission = MyTransmissionProtocol("/dev/ttyUSB0")

print(my_transmission.read_json())
sleep(3)

my_transmission.write_safely(b"hi! yingshaoxo")
sleep(3)

while 1:
    byte = my_transmission.read_safely()
    print(byte)
