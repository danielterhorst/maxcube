import base64
import binascii
import decimal
import io

from . import Message


class L(Message):
    """
    The L-message provices device data.

    More info: https://github.com/Bouni/max-cube-protocol/blob/master/L-Message.md
    """

    @staticmethod
    def parse(message):
        """
        Base64 encoded message. Length is in the first byte of the decoded message.
        """

        decoded = io.BytesIO(base64.b64decode(message))

        data = {}

        while True:

            try:
                message_len = ord(decoded.read(1))
            except TypeError:
                break

            message = bytearray(decoded.read(message_len))

            device = {
                'address': binascii.hexlify(message[0:3]),
                '?1': message[3],
                'flags_1': message[4],
                'flags_2': message[5],
                'temperature_setpoint': None,
                'temperature': None
            }

            if message_len > 6:
                device['temperature_setpoint'] = decimal.Decimal(message[7]) / 2

            # WallMountedThermostat
            if message_len == 12:
                device['temperature'] = decimal.Decimal(message[11]) / 10

            # HeatingThermostat
            elif message_len == 11:
                device['valve_position'] = message[6]

                if device['valve_position'] & 3 != 2:
                    device['temperature'] = decimal.Decimal(message[9]) / 10

            data[device['address']] = device

        return data
