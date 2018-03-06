#!/usr/bin/env python3

from sys import *
from socket import *
from threading import *
import time
from deckSetUp import *

def startServerThread(accept):
    """Creates a server thread  connected to a player, receives and forwards messages from him/her and sends messages to him/her."""
    global indx
    (connection, (clientAddr, clientPort)) = accept
    try:
        print("Connection from %s on port %s" % (clientAddr, clientPort))
        data = ""
        while True:
            data = connection.recv(1024).decode()
            if data: 
                message = eval(str(data))
                if message[1] == "ctrl":
                    if message[2] == "start":
                        #The player wants to start playing
                        for i in range(2):
                            getCard(message[0], clientAddr, port)
                    elif message[2] == "stop":
                        #The player wants to stop playing
                        pass #close thread, remove player info and tell the client's server to stop too
                    else:
                        #The player just joined and wants to pass on his/her info
                        info = eval(str(message[2]))
                        clntLock.acquire() #Get lock
                        clients[message[0]] = info[0] #name
                        statistics[message[0]] = [info[1], 0, info[2], info[3], info[4]] #[points], tunrNum, fundsAvailable, fundsBetted, fundsInsured
                        clntLock.release() #Release lock
                elif message[1] == "chat":
                    #The player wants to send a message to everyone
                    #print("<%s>: %s" % (clients[message[0]], message[2]))
                    mssgLock.acquire() #Get lock
                    transmitter.set(clients[message[0]], message[2])
                    transmitter.broadcast()
                    mssgLock.release() #Release lock
                elif message[1] == "cmmd":
                    #The player wants to play
                    if indx < maxClients and message[0] == clientOnIp:
                        if message[2] == "hit":
                            getCard(message[0], clientAddr, port)
                        elif message[2] == "stick":
                            indx += 1
                        elif message[2] == "double_down" and statistics[clientOnIp][1] == 0:
                            getCard(message[0], clientAddr, port)
                            indx += 1
                        #
                        #add insurance
                        #
                        elif message[2] == "surrender" and statistics[clientOnIp][1] == 0:
                            clntLock.acquire() #Get lock
                            bet50 = statistics[clientOnIp][3]/2
                            print(bet50)
                            funds = statistics[clientOnIp][2]
                            funds -= bet50
                            statistics[clientOnIp][2] = funds
                            clntLock.release() #Release lock
                            indx += 1
                        clntLock.acquire() #Get lock
                        temp = statistics[clientOnIp][1]
                        temp += 1
                        statistics[clientOnIp][1] = temp
                        clntLock.release() #Release lock
    except:
        pass

def getCard(client, recvAddr, recvPort):
    deckLock.acquire() #Get lock
    card = deck.rem()
    deckLock.release() #Release lock
    clntLock.acquire() #Get lock
    calcPoint(client, card)
    clntLock.release() #Release lock
    mssg = str(card)
    if client != addr:
        mssgLock.acquire() #Get lock
        transmitter.set("", mssg)
        transmitter.transmit("cmmd", recvAddr, recvPort)
        mssgLock.release() #Release lock
    else:
        print(mssg)

def calcPoint(playerIp, card):
    if statistics[playerIp][0] == []:
        statistics[playerIp][0].append(int(card._val))
    else:
        for point in range(len(statistics[playerIp][0])):
            temp = statistics[playerIp][0][point]
            temp += int(card._val)
            statistics[playerIp][0][point] = temp
    if card._num == "Ace":
        temp = statistics[playerIp][0][-1]
        temp += 10
        statistics[playerIp][0].append(temp)
    remvPoint(playerIp)
    return

def remvPoint(playerIp):
    global indx
    index = len(statistics[playerIp][0]) - 1
    while index != -1:
        if statistics[playerIp][0][index] > 21:
            statistics[playerIp][0].pop(index)
        index -= 1
    if statistics[playerIp][0] == []:
        indx += 1
    print(statistics[playerIp][0])
    return
        

def setUpGame(clientsNum=4, deckNum=1, shflNum=10):
    """Starts a new game allowing 'clientNum' number of players to join and using 'deckNum' number of decks that has been shuffled 'shflNum' number of times."""
    global addr, port,  deck, clntNum, maxClients, clientOnIp, indx
    maxClients = clientsNum
    deck = Generator(deckNum, shflNum)
    #for testing
    print(addr)
    sock = socket(AF_INET, SOCK_STREAM) #Creates a socket that uses TCP
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #Make the socket reusable
    sock.bind((addr, port)) #Open a connection on the predetermined IP address and portnumber
    while True:
        sock.listen(1)
        if clntNum < maxClients - 1:
            clntNum += 1
            Thread(target=startServerThread, args=(sock.accept(),)).start()
        if clntNum == maxClients - 1 and clientOnIp == "":
            #dealer draws2 cards and displays the first
            time.sleep(1)
            clientOnIp = sorted(clients)[indx]
        if clientOnIp != "":
            try:
                clientOnIp = sorted(clients)[indx]
            except IndexError:
                pass
                #dealer's turn goes here
                #tell each client its stats

class Transmitter(object):

    def __init__(self):
        """Creates a Transmitter object which the host uses to forward messages and to communicate with the players."""
        self._id = ""
        self._ip = gethostbyname(gethostname())
        self._mssg = ""

    def set(self, name, mssg):
        """Sets the name under which to send the message and the message itself."""
        self._id = name
        self._mssg = mssg

    def broadcast(self):
        """Sends a message to every player."""
        for client in clients:
            try:
                self.transmit("chat", client, chat)
            except:
                pass
            finally:
                self._sock.close()
        return

    def transmit(self, mssgType, client, portNum):
        """Establishes a connection, creates a standardised message and sends it over the connection."""
        self._sock = socket(AF_INET, SOCK_STREAM)
        self._sock.connect((client, portNum))
        message = str((self._id, mssgType, self._mssg))
        try:
            self._sock.sendall(message.encode())
        except ConnectionResetError:
            print("The connection has been closed by the server. Please try again later.")
            self._sock.close()

#Setting up
addr = gethostbyname(gethostname())
port = 5000
chat = 4000
transmitter = Transmitter()
deck = ""

#Limiting the number of players
clntNum = -1
maxClients = 0

#Locking functionality
deckLock = Lock()
clntLock = Lock()
mssgLock = Lock()

#Keeping track of the players' info and who's turn it is
clients = {}
statistics = {}
indx = 0
clientOnIp = ""

setUpGame(int(argv[1]), int(argv[2]), int(argv[3]))
