"""
Device objects for the eq-3 Max! system devices
"""


class Cube(object):
    """
    Definition for a Max!Cube LAN gateway
    """

    def __init__(self, address, serial, firmware_version):
        self.address = address
        self.serial = serial
        self.firmware_version = firmware_version
        self.rooms = {}
        self.devices = []

    def __repr__(self):
        return '<Cube address={} serial={} firmware_version>'.format(self.address, self.serial, self.firmware_version)

    def add_room(self, room):
        self.rooms[room.id] = room
        room.cube = self

    def add_device(self, device):
        self.devices.append(device)
        device.cube = self

        if device.room_id:
            self.rooms[device.room_id].add_device(device)


class Room(object):
    """
    Object container for a room
    """

    def __init__(self, id, address, name):
        self.id = id
        self.address = address
        self.name = name
        self.cube = None
        self.devices = []

    def __repr__(self):
        return '<Room id={} address={} name={}>'.format(self.id, self.address, self.name)

    def add_device(self, device):
        self.devices.append(device)
        device.room = self


class Device(object):
    """
    Object container for a eq-3 Max! device which are defined as subclasses.
    """

    def __init__(self, address, serial, room_id, name, type):
        self.address = address
        self.serial = serial
        self.room_id = room_id
        self.name = name
        self.type = type

    def __repr__(self):
        return '<Device address={} serial={} room_id={} name={}>'.format(
            self.address, self.serial, self.room_id, self.name
        )

    @classmethod
    def get_device_type(cls, type_id):
        """
        Returns correct class based on Max! defice type ID
        """

        return {c.type_id: c for c in cls.__subclasses__()}.get(type_id, cls)


class Valve(Device):
    """
    Valve-like objects like the "eq-3 ax! Radiator Thermostat" and the "eq-3 Max! Wall Thermostat".
    """

    type_id = 2


class Switch(Device):
    """
    Switch-like objects like the "eq-3 Max! ECO switch".
    """

    type_id = 5


class WindowSensor(Device):
    """
    Window sensor object such as the "eq-3 Max Window sensor"
    """

    type_id = 4
