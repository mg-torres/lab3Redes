import socket
import sys


def get_constants(prefix):
    """Create a dictionary mapping socket module
    constants to their names.
    """
    return {
        getattr(socket, n): n
        for n in dir(socket)
        if n.startswith(prefix)
    }


families = get_constants('AF_')
types = get_constants('SOCK_')
protocols = get_constants('IPPROTO_')

# Create a TCP/IP socket
#TODO Organizar los puertos y la dircción
sock = socket.create_connection(('localhost', 10000))
#sock = socket.create_connection(('localhost', 10000))
#sock = socket.create_connection(('localhost', 10000))
#sock = socket.create_connection(('localhost', 10000))
#sock = socket.create_connection(('localhost', 10000))

#sock = socket.create_connection(('localhost', 10000))
#sock = socket.create_connection(('localhost', 10000))
#sock = socket.create_connection(('localhost', 10000))
#sock = socket.create_connection(('localhost', 10000))
#sock = socket.create_connection(('localhost', 10000))

#sock = socket.create_connection(('localhost', 10000))
#sock = socket.create_connection(('localhost', 10000))
#sock = socket.create_connection(('localhost', 10000))
#sock = socket.create_connection(('localhost', 10000))
#sock = socket.create_connection(('localhost', 10000))

#sock = socket.create_connection(('localhost', 10000))
#sock = socket.create_connection(('localhost', 10000))
#sock = socket.create_connection(('localhost', 10000))
#sock = socket.create_connection(('localhost', 10000))
#sock = socket.create_connection(('localhost', 10000))

#sock = socket.create_connection(('localhost', 10000))
#sock = socket.create_connection(('localhost', 10000))
#sock = socket.create_connection(('localhost', 10000))
#sock = socket.create_connection(('localhost', 10000))
#sock = socket.create_connection(('localhost', 10000))


print('Family  :', families[sock.family])
print('Type    :', types[sock.type])
print('Protocol:', protocols[sock.proto])
print()

try:

    # Send data
    message = b'This is the message.  It will be repeated.'
    print('sending {!r}'.format(message))
    sock.sendall(message)

    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print('received {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()