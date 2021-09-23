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
#sock = socket.create_conn…
[5:51 p. m., 23/9/2021] Maria Gabriela Torres 🦀: import socket
import sys
import os

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_address = ('', 10002)
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

#Array vacio de conecciones
conexiones = []

#Función envío de archivos
def archivo(connections, num_archivo):
    print("funcion archivo")
    if (num_archivo == 1):
        for c in connections:
            c.send(f"{filename1}{SEPARATOR}{filesize1}".encode())
            print("envia el archivo 1")
            with open(file1, "rb") as f:
                while True:
                    bytes_read = f.read(1024)
                    if not bytes_read:
                        break
                    c.sendall(bytes_read)
    elif (num_clientes == 2):
        for c in connections:
            c.send(f"{filename2}{SEPARATOR}{filesize2}".encode())
            print("envia el archivo 2")
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
                print("crea la conexión")
            if len(conexiones) >= num_clientes:
                archivo(conexiones, num_archivo)
                print("archivo conexiones")
    finally:
        connection.close()