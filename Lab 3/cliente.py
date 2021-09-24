import socket
import sys
import tqdm
import os


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

SEPARATOR = "SEPARATOR"
BUFFER_SIZE = 1024 # send 4096 bytes each time step

# Create a TCP/IP socket
#TODO Organizar los puertos y la dircción
sock = socket.create_connection(('localhost', 10008))
#sock = socket.create_connection(('localhost', 10008))
#sock = socket.create_connection(('localhost', 10008))
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

fin = False

while True:
    print("¿Está listo para recibir el archivo? Presione 1 para confirmar o 0 para cancelar")
    input1 = int(input())
    if (input1 == 1):
        message = b'Listo para recibir'
        print('sending {!r}'.format(message))
        sock.sendall(message)

    elif (input1 == 0):
        print("Se cancelará el proceso")
    received = sock.recv(BUFFER_SIZE).decode('ISO-8859-1')
    print(received)
    filename = ""
    filesize = 0
    if('SEPARATOR' in received):
        filename, filesize = received.split(SEPARATOR)
        # remove absolute path if there is
        filename = os.path.basename(filename)
        # convert to integer
        filesize = int(filesize)
    try:
        #progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "w") as f:
            while True:
                # read 1024 bytes from the socket (receive)
                bytes_read = sock.recv(BUFFER_SIZE)
                if not bytes_read:
                    # nothing is received
                    # file transmitting is done
                    fin = True
                    print("no bytes")
                    break
                # write to the file the bytes we just received
                f.write(bytes_read.decode('ISO-8859-1'))
                # update the progress bar
                #progress.update(len(bytes_read))
                print('received {!r}'.format(filename))
    finally:
        f.close()
        print('closing socket')
        sock.close()
        if (fin):
            break