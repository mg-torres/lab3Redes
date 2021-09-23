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


# input
#Archivos a enviar
file1 = "Archivos/Archivo1_100MB.pptx"
file2 = "Archivos/Archivo2_250MB.pptx"

#Nombre archivos a enviar
filename1 = "Archivos/Archivo1_100MB.pptx"
filename2 = "Archivos/Archivo2_250MB.pptx"

#Tamaño de los archivos
filesize1 = os.path.getsize(file1)
filesize2 = os.path.getsize(file2)

print("Seleccione el archivo que desea enviar")
print("Presione 1 para enviar el archivo de 100MB")
print("Presione 2 para enviar el archivo de 250MB")
input1 = int(input())

if(input1==1):
        filename = filename1
        filesize = filesize1
elif(input1==2):
        filename = filename2
        filesize = filesize2

print(filename)
try:

    # Send data

    sock.send(f"{filename}{SEPARATOR}{filesize}".encode())
    #message = b'This is the message.  It will be repeated.'
    print('sending {!r}'.format(filename))
    #sock.sendall(message)

    #amount_received = 0
    #amount_expected = len()

    #while amount_received < amount_expected:
        #data = sock.recv(16)
        #amount_received += len(data)
        #print('received {!r}'.format(data))

    # start sending the file
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in
            # busy networks
            sock.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))


finally:
    print('closing socket')
    sock.close()
