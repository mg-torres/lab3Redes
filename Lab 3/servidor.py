import socket
import os
import logging
from datetime import datetime
import hashlib
import threading
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_address = ('', 10000)
sock.bind(server_address)
print('starting up on {} port {}'.format(*sock.getsockname()))
sock.listen(25)

# Separador
SEPARATOR = "SEPARATOR"

#Archivos a enviar
file1 = "Archivos/PRUEBA.txt"
file2 = "Archivos/archivo1.txt"

#Nombre archivos a enviar
filename1 = "PRUEBA.txt"
filename2 = "archivo1.txt"

#Tamaño de los archivos
filesize1 = os.path.getsize(file1)
filesize2 = os.path.getsize(file2)

#Array vacio de conecciones
conexiones = []

#Array vacio con tiempos de entrega del archivo
tiempos = []

#Nombre log
LOG_FILENAME = datetime.now().strftime('%Y_%m_%d_%H_%M_%S.log')

#Variable para cerrar servidor
fin = False

#Tamaño del buffer
BUFFER_SIZE = 1024

#Función envío de archivos
def archivo(num_archivo, c):
    nombreArchivo = ''
    tamArchivo = 0
    arch = ''
    if (num_archivo == 1):
        nombreArchivo = filename1
        tamArchivo = filesize1
        arch = file1
    elif (num_archivo == 2):
        nombreArchivo = filename2
        tamArchivo = filesize2
        arch = file2
    start_time = datetime.now()
    c.send(f"{nombreArchivo}{SEPARATOR}{tamArchivo}".encode())
    with open(arch, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                end_time = datetime.now()
                tiempo = end_time - start_time
                tiempos.append(tiempo)
                break
            c.send(bytes_read)
    message = b'Finaliza transmision'
    c.send(message)
    md5(c, arch)
    data = connection.recv(1024)
    mensaje2 = data.decode('utf-8')
    if ('Los valores son iguales' in mensaje2):
        success = True
    elif ('Los valores son diferentes' == mensaje2):
        success = False

#Función de creación y envío de hash
def md5(connection, fname):
    md5 = hashlib.md5()
    with open(fname, 'rb') as f:
        while True:
            data = f.read(BUFFER_SIZE)
            if not data:
                break
            md5.update(data)
    connection.send(md5.hexdigest().encode('ISO-8859-1'))

#Función para crear el log
def log(filenameF, filesize, success, tiempos):
    filename = LOG_FILENAME
    logging.basicConfig(filename = filename, encoding='utf-8', level=logging.INFO)
    logging.info('Nombre archivo:' + filenameF)
    logging.info('Tamaño archivo:' + str(filesize))
    i = 1
    for c in conexiones:
        logging.info('Cliente ' + str(i))
        if (success):
            logging.info('Archivo fue entregado exitosamente')
        else:
            logging.info('Archivo no fue entregado exitosamente')
        for t in tiempos:
            if (tiempos.index(t) == i-1):
                logging.info('Tiempo de transferencia archivo cliente ' + str(i) + ': '+ str(t) + " milisegundos")
        i += 1
    return filename

if __name__ == "__main__":
 while True:
    success = True
    conexiones = []
    tiempos = []
    print('waiting for a connection')
    num_archivo = int(input('¿Qué archivo desea enviar? (1: 100MB, 2: 250MB)'))
    num_clientes = int(input('¿A cuantos clientes desea enviar el archivo?'))
    try:
        while True:
            connection, client_address = sock.accept()
            data = connection.recv(BUFFER_SIZE)
            print('received {!r}'.format(data))
            mensaje=data.decode('utf-8')
            if mensaje == ('Listo para recibir'):
                conexiones.append(connection)
            if len(conexiones) >= num_clientes:
                for c in conexiones:
                    x = threading.Thread(target=archivo, args=(num_archivo, c, ))
                    x.start()
                    time.sleep(1)
                fin = True
                break
    finally:
        nomArchivo = ''
        tamArchivo = 0
        if (num_archivo == 1):
            nomArchivo = filename1
            tamArchivo = filesize1
        elif (num_archivo == 2):
            nomArchivo = filename2
            tamArchivo = filesize2
        filename = log(nomArchivo, tamArchivo, success, tiempos)
        filename = os.path.basename(filename)
        var = os.path.join("./LogsServidor", filename)
        connection.close()
        if fin:
            break