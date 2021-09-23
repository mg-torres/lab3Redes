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

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step

# Create a TCP/IP socket
#TODO Organizar los puertos y la dircción
sock = socket.create_connection(('localhost', 10002))
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


print("¿Está listo para recibir el archivo? Presione 1 para confirmar o 0 para cancelar")
input1 = int(input())

if(input1==1):
    message = b'Listo para recibir'
    print('sending {!r}'.format(message))
    sock.sendall(message)

elif(input1==0):
        print("Se cancelará el proceso")


try:
    print("recibido0")
    # Recieve data
    received = sock.recv(BUFFER_SIZE).decode()
    print("recibido1")
    filename, filesize = received.split(SEPARATOR)
    # remove absolute path if there is
    filename = os.path.basename(filename)
    # convert to integer
    filesize = int(filesize)
    print("recibido2")
    # start receiving the file from the socket
    # and writing to the file stream
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    print("recibido3")
    with open(filename, "wb") as f:
        while True:
            print("recibido4")
            # read 1024 bytes from the socket (receive)
            bytes_read = sock.recv(BUFFER_SIZE)
            if not bytes_read:
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            print("recibido5")
            # update the progress bar
            progress.update(len(bytes_read))
            print('received {!r}'.format(filename))
            print("recibido6")


finally:
    print('closing socket')
    sock.close()