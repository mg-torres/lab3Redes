import socket
import sys
import os
import logging
from datetime import datetime
import hashlib

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_address = ('', 10008)
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

#Tamaño de los archivos
filesize1 = os.path.getsize(file1)
filesize2 = os.path.getsize(file2)

#Array vacio de conecciones
conexiones = []

#Array vacio con tiempos de entrega del archivo
tiempos = []

#Nombre log
LOG_FILENAME = datetime.now().strftime('D:/log/logfile_%Y_%m_%d_%H_%M_%S.log')

#Variable para cerrar servidor
fin = False;

#Función envío de archivos
def archivo(connections, num_archivo):
    if (num_archivo == 1):
        success = True
        for c in connections:
            start_time = datetime.now()
            c.send(f"{filename1}{SEPARATOR}{filesize1}".encode())
            md5(c, file1)
            with open(file1, "rb") as f:
                while True:
                    bytes_read = f.read(1024)
                    if not bytes_read:
                        end_time = datetime.now()
                        time = end_time - start_time
                        tiempos.append(time)
                        break
                    c.send(bytes_read)
        log(filename1, filesize1, success, tiempos)
        fin = True
    elif (num_archivo == 2):
        success = True
        for c in connections:
            start_time = datetime.now()
            c.send(f"{filename2}{SEPARATOR}{filesize2}".encode())
            md5(c, file1)
            with open(file2, "rb") as f:
                while True:
                    bytes_read = f.read(1024)
                    if not bytes_read:
                        end_time = datetime.now()
                        time = end_time - start_time
                        tiempos.append(time)
                        break
                    c.send(bytes_read)
        log(filename1, filesize1, success, tiempos)
        fin = True

def md5(connection, fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    connection.send(hash_md5.hexdigest().encode())

def log(filename, filesize, success, tiempos):
    logging.basicConfig(LOG_FILENAME, encoding='utf-8', level=logging.INFO)
    logging.info('Nombre archivo:' + filename)
    logging.info('Tamaño archivo:' + filesize)
    if (success):
        logging.info('Archivo fue entregado exitosamente')
    else:
        logging.info('Archivo no fue entregado exitosamente')
    logging.info('Archivo fue entregado exitosamente')
    i=1
    for t in tiempos:
        logging.info('Tiempo de transferencia archivo # ' + i + ': '+ t + " milisegundos")
        i+=1
    logging.info('Número de paquetes enviados:')
    logging.info('Valor total en bytes enviado: ')


while True:
    conexiones = []
    tiempos = []
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
                break
    finally:
        connection.close()
    if fin:
        break