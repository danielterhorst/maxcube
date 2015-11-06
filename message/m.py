import io
import base64
import binascii

from . import Message


class M(Message):
    """
    The M-message provides metadata on configured rooms and connected devices.

    More inf: https://github.com/Bouni/max-cube-protocol/blob/master/M-Message.md
    """

    @staticmethod
    def parse(message):
        """
        Base64 encoded message.
        """

        data = {}

        # Clip the first and the last two bytes (removing the M: and CR+LF)
        _, _, encoded = message.strip().split(b',', 2)

        decoded = io.BytesIO(base64.b64decode(encoded))

        data['index'] = ord(decoded.read(1))
        data['count'] = ord(decoded.read(1))

        # Rooms
        data['room_count'] = ord(decoded.read(1))
        data['rooms'] = {}

        for i in range(data['room_count']):

            room_id = ord(decoded.read(1))
            room_name_len = ord(decoded.read(1))
            room_name = decoded.read(room_name_len)
            group_address = binascii.b2a_hex(decoded.read(3))

            data['rooms'][room_id] = {
                'id': room_id,
                'name': room_name,
                'address': group_address
            }

        # Devices
        data['devices_count'] = ord(decoded.read(1))
        data['devices'] = []

        for i in range(data['devices_count']):

            device_type = ord(decoded.read(1))
            device_address = binascii.b2a_hex(decoded.read(3))
            device_serial = decoded.read(10)
            device_name_len = ord(decoded.read(1))
            device_name = decoded.read(device_name_len)
            device_room_id = ord(decoded.read(1))

            data['devices'].append({
                'type': device_type,
                'address': device_address,
                'serial': device_serial,
                'name': device_name,
                'room_id': device_room_id
            })

        # Unknown byte
        data['?1'] = decoded.read(1)

        return data
