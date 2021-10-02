import socket
import os
import hashlib
import time
import threading
import logging
from datetime import datetime

#Separador
SEPARATOR = "SEPARATOR"

#Tamaño del buffer
BUFFER_SIZE = 1024

#Nombre log
LOG_FILENAME = datetime.now().strftime('%Y_%m_%d_%H_%M_%S_CLI.log')

#Array vacio de conecciones
conexiones = []

#Array vacio con tiempos de entrega del archivo
tiempos = []

#Variable para cerrar conexiones
fin = False

success = True
filenameF = ''
filesizeF = 0

#Función de creación y envío de hash
def md5(connection, fname, hashrecibido):
    md5 = hashlib.md5()
    with open(fname, 'rb') as f:
        while True:
            data = f.read(BUFFER_SIZE)
            if not data:
                break
            md5.update(data)

    if (format(md5.hexdigest()) == hashrecibido):
        mssg = b'Los valores son iguales'
        success = True
        connection.send(mssg)
    else:
        mssg = b'Los valores son diferentes'
        success = False
        connection.send(mssg)

#Función para crear el log
def log(filenamePrueba, filesizePrueba, success, tiempos):
    filename = LOG_FILENAME
    logging.basicConfig(filename = filename, encoding='utf-8', level=logging.INFO)
    logging.info('Nombre archivo:' + filenamePrueba)
    logging.info('Tamaño archivo:' + str(filesizePrueba))
    i = 1
    print(len(tiempos))
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

#Función para crear los clientes
def createSocket(i, num_clientes):
    sock = socket.create_connection(('localhost', 10000))
    conexiones.append(i)
    while True:
        message = b'Listo para recibir'
        sock.send(message)
        received = sock.recv(BUFFER_SIZE).decode('ISO-8859-1')
        if('SEPARATOR' in received):
            filenameF, filesizeF = received.split(SEPARATOR)
            newFilename = 'Cliente'+str(i+1)+'-Prueba'+str(num_clientes)+'.txt'
            newFilename = os.path.basename(newFilename)
            var=os.path.join("./ArchivoRecibidos", newFilename)
            filesizeF = int(filesizeF)
        try:
            start_time = datetime.now()
            with open(var, "w") as f:
                while True:
                    bytes_read = sock.recv(BUFFER_SIZE)
                    if ('Finaliza transmision' in bytes_read.decode('ISO-8859-1')):
                        end_time = datetime.now()
                        tiempo = end_time - start_time
                        tiempos.append(tiempo)
                        break
                    f.write(bytes_read.decode('ISO-8859-1'))
        finally:
            f.close()
            received = sock.recv(BUFFER_SIZE).decode('ISO-8859-1')
            md5(sock,var,received)
            fin = True
            print('closing socket')
            sock.close()
            if (fin):
                break

if __name__ == "__main__":
    while True:
        num_clientes = int(input('¿Cuantos clientes recibirán el archivo?'))
        try:
            while True:
                for i in range (num_clientes):
                    x = threading.Thread(target=createSocket, args=(i, num_clientes))
                    x.start()
                    time.sleep(1)
                fin=True
                break
        finally:
            filenameLog = log(filenameF, filesizeF, success, tiempos)
            filenameLog = os.path.basename(filenameLog)
            var = os.path.join("./LogsCliente", filenameLog)
            if (fin):
                break
