import network
import objects
import settings
import parser


socket = network.get(settings.MAX_CUBE_IP, settings.MAX_CUBE_PORT)

message = network.read(socket)

data = parser.parse(message)

header = data['H']
meta = data['M']
devices = data['L']

cube = objects.Cube(
    address=header['address'],
    serial=header['serial'],
    firmware_version=header['firmware_version']
)

for room in meta['rooms'].values():
    cube.add_room(objects.Room(**room))

for device in meta['devices']:
    device_class = objects.Device.get_device_type(device['type'])
    device = device_class(**device)

    cube.add_device(device)

    if device.address in devices:
        device.__dict__.update(devices[device.address])


print 'cube', cube
print 'cube.devices', cube.devices
print 'cube.rooms', cube.rooms

for room in cube.rooms.values():
    print 'room', room

    for device in room.devices:
        print 'device', device
        print 'device.__dict__', device.__dict__
