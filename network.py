import socket


def get(ip, port):
    """
    Open up a socket connection the eq-3 Max! Cube
    """

    bound_socket = socket.socket()

    # The timeout needed for the Max! Cube to send it's data
    bound_socket.settimeout(2)

    bound_socket.connect((ip, port))

    return bound_socket


def read(bound_socket):
    """
    Keep reading data from the socket until the timeout.
    """

    data = b''

    while True:

        try:
            data += bound_socket.recv(100000)

        except socket.timeout:
            break

    return data
