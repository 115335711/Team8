from socket import *
from threading import *
from deckSetUp import *

def startServerThread(accept):
    (connection, (clientAddr, clientPort)) = accept
    try:
        print("Connection from %s on port %s" % (clientAddr, clientPort))
        data = ""
        while True:
            data = connection.recv(1024).decode()
            if data: 
                message = eval(str(data))
                if message[1] == "ctrl":
                    if message[2] == "stop":
                        pass #close thread
                    else:
                        #
                        #give 2 card to the client
                        #
                        info = eval(str(message[2]))
                        clients[message[0]] = info[0] #name
                        statistics[message[0]] = [info[1], info[2], info[3], info[4]] #[lowerPoints, higherPoints], fundsAvailable, fundsBetted, fundsInsured
                elif message[1] == "chat":
                    print("<%s>: %s" % (clients[message[0]], message[2]))
                    transmitter.set(clients[message[0]], message[2])
                    transmitter.broadcast()
                elif message[1] == "cmmd":
                    if indx < maxClients and message[0] == clientOnIp:
                        print(message[2])
                        #
                        #add options regarding what to do with the different messages
                        #
    except:
        pass

def setUpGame(clientsNum, deckNum, shflNum):
    global portNum, deck, clntNum, maxClients, clientOnIp, indx
    maxClients = clientsNum
    deck = Generator(deckNum, shflNum)
    print(gethostbyname(gethostname()))
    addr = gethostbyname(gethostname())
    port = portNum
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((addr, port))
    while True:
        sock.listen(1)
        if clntNum < maxClients - 1:
            clntNum += 1
            Thread(target=startServerThread, args=(sock.accept(),)).start()
        if clntNum == maxClients - 1 and clientOnIp == "":
            clientOnIp = sorted(clients)[indx]

class Transmitter(object):

    def __init__(self):
        self._id = ""
        self._ip = gethostbyname(gethostname())
        self._mssg = ""

    def set(self, name, mssg):
        self._id = name
        self._mssg = mssg

    def broadcast(self):
        for client in clients:
            if client != self._ip:
                try:
                    self._sock = socket(AF_INET, SOCK_STREAM)
                    self._sock.connect((client, portNum))
                    self.transmit("chat", self._mssg)
                except:
                    pass
                finally:
                    self._sock.close()
        return

    def transmit(self, mssgType, mssg):
        message = str((self._id, mssgType, mssg))
        try:
            self._sock.sendall(message.encode())
        except ConnectionResetError:
            print("The connection has been closed by the server. Please try again later.")
            self._sock.close()

#Setting up
transmitter = Transmitter()
portNum = 9901
deck = ""

#Limiting the number of players
clntNum = -1
maxClients = 0

#Keeping track of the players' info and who's turn it is
clients = {}
statistics = {}
indx = 0
clientOnIp = ""
