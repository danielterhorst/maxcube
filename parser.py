from message.m import M
from message.l import L
from message.h import H


MESSAGE_TYPE_MAP = {
    'M': M,
    'L': L,
    'H': H
}


def parse(message):
    data = {}

    # Max! protocol seperates lines by \n
    for line in message.split():

        # Message type is always the first index of the string received
        message_type = line[0]

        if message_type not in MESSAGE_TYPE_MAP:
            continue

        # Clip the first and the last two bytes (removing the M: and CR+LF)
        _, encoded = line.strip().split(b':', 2)

        data[message_type] = MESSAGE_TYPE_MAP.get(message_type).parse(encoded)

    return data
