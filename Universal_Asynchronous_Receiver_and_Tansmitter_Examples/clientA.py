from UART_Python_Lib import *

my_transmission = MyTransmissionProtocol("/dev/ttyUSB0")

#sleep(3)
print(my_transmission.read_json())
exit()

i = 255
while 1:
    i -= 1

    my_transmission.write_safely(hex_to_bytes(text_to_hex(str(i)+"yingshaoxo")))

    if i == 0:
        i = 255
