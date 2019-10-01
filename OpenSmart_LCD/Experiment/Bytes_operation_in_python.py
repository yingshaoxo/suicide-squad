import binascii


def bytes_to_hex(a_byte, length=2):
    return str(binascii.hexlify(a_byte))[2:-1]


def hex_to_bytes(hex_string):
    return binascii.unhexlify(hex_string)


def int_to_hex(integer, length=None):
    if length != None:
        hex_string = ('{:0'+str(length)+'X}').format(integer)
    else:
        hex_string = hex(integer)[2:]
        if (len(hex_string) % 2 == 1):
            hex_string = "0" + hex_string
    return hex_string


def hex_to_int(hex_string):
    return int(hex_string, 16)


def int_to_bytes(integer, length=None):
    hex_string = int_to_hex(integer, length)
    return hex_to_bytes(hex_string)


def bytes_to_int(a_byte):
    hex_string = bytes_to_hex(a_byte)
    return hex_to_int(hex_string)


def text_to_hex(text):
    length = len(text) * 2
    bytes_ = binascii.hexlify(text.encode("ascii", "ignore"))
    result = str(bytes_)
    result = result[2:][:-1]
    return result
