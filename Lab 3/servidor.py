import socket
import sys
import os

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_address = ('', 10015)
sock.bind(server_address)
print('starting up on {} port {}'.format(*sock.getsockname()))
sock.listen(25)

# Separator
SEPARATOR = "SEPARATOR"

#Archivos a enviar
file1 = "Archivos/PRUEBA.txt"
file2 = "Archivos/Archivo2_250MB.pptx"

#Nombre archivos a enviar
filename1 = "PRUEBA.txt"
filename2 = "Archivo2_250MB.pptx"

#TamaÃ±o de los archivos
filesize1 = os.path.getsize(file1)
filesize2 = os.path.getsize(file2)

#Array vacio de conecciones
conexiones = []

#Función envío de archivos
def archivo(connections, num_archivo):
    if (num_archivo == 1):
        for c in connections:
            c.send(f"{filename1}{SEPARATOR}{filesize1}".encode())
            with open(file1, "rb") as f:
                while True:
                    bytes_read = f.read(1024)
                    if not bytes_read:
                        break
                    c.send(bytes_read)
            c.send('Finalizado'.encode())
    elif (num_clientes == 2):
        for c in connections:
            c.send(f"{filename2}{SEPARATOR}{filesize2}".encode())
            with open(file2, "rb") as f:
                while True:
                    bytes_read = f.read(1024)
                    if not bytes_read:
                        break
                    c.sendall(bytes_read)

while True:
    print('waiting for a connection')
    num_archivo = int(input('¿Qué archivo desea enviar? (1: 100MB, 2: 250MB)'))
    num_clientes = int(input('¿A cuantos clientes desea enviar el archivo?'))
    connection, client_address = sock.accept()
    try:
        while True:
            data = connection.recv(1024)
            print('received {!r}'.format(data))
            mensaje=data.decode('utf-8')
            if mensaje == ('Listo para recibir'):
                conexiones.append(connection)
            if len(conexiones) >= num_clientes:
                archivo(conexiones, num_archivo)
    finally:
        connection.close()