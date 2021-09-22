import socket
import sys
import os

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_address = ('', 10000)
sock.bind(server_address)
print('starting up on {} port {}'.format(*sock.getsockname()))
sock.listen(25)

# Separator
SEPARATOR = " "

#Archivos a enviar
file1 = "Archivos/Archivo1_100MB.pptx"
file2 = "Archivos/Archivo2_250MB.pptx"

#Nombre archivos a enviar
filename1 = "Archivo1_100MB"
filename2 = "Archivo2_250MB"

#Tamaño de los archivos
filesize1 = os.path.getsize(file1)
filesize2 = os.path.getsize(file2)

while True:
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('client connected:', client_address)
        while True:
            data = connection.recv(1024)
            print('received {!r}'.format(data))
            if (data==1):
                connection.send(f"{filename1}{SEPARATOR}{filesize1}".encode())
                with open(file1, "rb") as f:
                    while True:
                        bytes_read = f.read(1024)
                        if not bytes_read:
                            break
                        connection.sendall(bytes_read)
            elif (data==2):
                connection.send(f"{filename2}{SEPARATOR}{filesize2}".encode())
                with open(file2, "rb") as f:
                    while True:
                        bytes_read = f.read(1024)
                        if not bytes_read:
                            break
                        connection.sendall(bytes_read)
            else:
                break
    finally:
        connection.close()

