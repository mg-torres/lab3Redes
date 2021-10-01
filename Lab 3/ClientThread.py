import socket, threading

class ClientThread(threading.Thread):

    ip='localhost'
    port=100025
    sock = socket.create_connection((ip, port))

    def __init__(self,ip,port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        print("[+] New thread started for "+ip+":"+str(port))


    def run(self, clientsock):
        print ("Connection from : "+self.ip+":"+str(self.port))

        clientsock.send("\nWelcome to the server\n\n")

        data = "dummydata"

        while len(data):
            data = clientsock.recv(2048)
            print("Client sent : "+data)
            clientsock.send("You sent me : "+data)

        print("Client disconnected...")