
import socket
import os
import hashlib

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




fin = False
success = False

valormd5=0

def md5(connection, fname,hashrecibido):

    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    with open(fname, 'rb') as f:
        while True:
            data = f.read(BUFFER_SIZE)
            if not data:
                break
            md5.update(data)
            sha1.update(data)
    print(format(md5.hexdigest()))
    print(hashrecibido)

    if (format(md5.hexdigest()) == hashrecibido):
        mssg = b'Los valores son iguales'
        print(mssg)
        sock.sendall(mssg)
    else:
        mssg = b'Los valores son diferentes'
        print(mssg)
        sock.sendall(mssg)


#def
sock = socket.create_connection(('localhost', 10000))
print('Family  :', families[sock.family])
print('Type    :', types[sock.type])
print('Protocol:', protocols[sock.proto])
print()
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
    filename = ""
    filesize = 0
    if('SEPARATOR' in received):
        filename, filesize = received.split(SEPARATOR)
        filename= '/ArchivoRecibidos/'+filename
        # remove absolute path if there is
        filename = os.path.basename(filename)
        var=os.path.join("./ArchivoRecibidos", filename)
        print(var)
        # convert to integer
        print(filename)
        filesize = int(filesize)
    try:
        #progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(var, "w") as f:
            while True:
                # read 1024 bytes from the socket (receive)
                bytes_read = sock.recv(BUFFER_SIZE)
                if ('Finaliza transmision' in bytes_read.decode('ISO-8859-1')):
                    break
                # write to the file the bytes we just received
                f.write(bytes_read.decode('ISO-8859-1'))
                # update the progress bar
                #progress.update(len(bytes_read))
                print('received {!r}'.format(filename))
    finally:
        f.close()
        received = sock.recv(BUFFER_SIZE).decode('ISO-8859-1')
        print(received)
        md5(sock,var, received)
        #if (success):
        #    message2 = b'Transmision exitosa'
        #    sock.sendall(message2)
        #else:
        #    message2 = b'Transmision no exitosa'
        #    sock.sendall(message2)
        fin = True
        print('closing socket')
        sock.close()
        if (fin):
            break
