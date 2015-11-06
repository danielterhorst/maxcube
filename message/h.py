from . import Message


class H(Message):
    """
    The H-messages provides header information, sent upon connecting to the Cube.

    More info: https://github.com/Bouni/max-cube-protocol/blob/master/H-Message.md
    """

    @staticmethod
    def parse(message):
        """
        Simple ASCII message seperated by comma's.
        """

        parts = message.split(',')

        return {
            'serial': parts[0],
            'address': parts[1],
            'firmware_version': parts[2],
        }
