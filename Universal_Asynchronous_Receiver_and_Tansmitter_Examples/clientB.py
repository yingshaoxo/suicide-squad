from UART_Python_Lib import *

my_transmission = MyTransmissionProtocol("/dev/ttyUSB1")

my_transmission.write_json({
    "me": 21,
    "you": 21,
    "someone": 100
})

print(my_transmission.read_safely())

i = 255
while 1:
    my_transmission.write_safely(hex_to_bytes(text_to_hex(str(i)+"yingshaoxo")))

    i -= 1
    if i == 0:
        i = 255
