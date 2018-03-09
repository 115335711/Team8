#!/usr/bin/env python3

from sys import *
from socket import *
from threading import *
import time
import shelve
from deckSetUp import *


def setUpGame(clientsNum=4, deckNum=1, shflNum=10):
    """Starts a new game allowing 'clientNum' number of players to join and using 'deckNum' number of decks that has been shuffled 'shflNum' number of times."""
    global addr, port, deck, clntNum, actuNum, maxClients, clientOnIp, indx, dealerHand, dealerPnts
    maxClients = clientsNum
    deck = Generator(deckNum, shflNum)
    sock = socket(AF_INET, SOCK_STREAM) #Creates a socket that uses TCP
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #Make the socket reusable
    sock.bind((addr, port)) #Open a connection on the predetermined IP address and portnumber
    while True:
        sock.listen(1)
        #Wait for 'maxClient' number of players them start the game
        if clntNum < maxClients - 1:
            clntNum += 1
            Thread(target=startServerThread, args=(sock.accept(),)).start()
            time.sleep(1)
        if clntNum == maxClients - 1 and clientOnIp == "":
            #There are enough players so the game can start
            deckLock.acquire() #Acquire lock
            dealerHand += [deck.rem()]
            dealerPnts += [dealerHand[0]._val]
            dealerHand += [deck.rem()]
            dealerPnts += [dealerHand[1]._val]
            deckLock.release() #Release lock
            clientOnIp = sorted(clients)[indx]
            mssg = "***DEALER: %s***" % str(dealerHand[0])
            print(mssg)
            mssgLock.acquire() #Acquire lock
            transmitter.set("", mssg)
            transmitter.broadcast("cmmd")
            mssgLock.release() #Release lock
            informAboutTurn()
            for client in clients:
                for i in range(2):
                    getCard(client, port)
        if actuNum == 0:
            #When everyone has disconnected, stop the service"""
            return
        
def startServerThread(accept):
    """Creates a server thread  connected to a player, receives and forwards messages from him/her and sends messages to him/her."""
    global indx, actuNum, dealerPnts
    (connection, (clientAddr, clientPort)) = accept
    try:
        print("Connection from %s on port %s" % (clientAddr, clientPort))
        data = ""
        while True:
            data = connection.recv(1024).decode()
            if data:
                message = eval(str(data))
                if message[1] == "ctrl":
                    if message[2] == "start": #deprecated
                        #The player wants to start playing
                        pass
                    elif message[2] == "stop":
                        #The player wants to stop playing
                        funds = statistics[message[0]][2]
                        print(funds)
                        bet = statistics[message[0]][3]
                        if statistics[message[0]][5] in ["lost", "surrendered"]:
                            funds -= bet
                            mssg = [1, 0, 1, funds, 0, bet]
                        elif statistics[message[0]][5] == "won":
                            funds += (bet * 2)
                            mssg = [1, 1, 0, funds, bet, 0]
                        else:
                            funds += bet
                            mssg = [1, 0, 0, funds, 0, 0]
                        print(mssg)
                        name = clients[message[0]]
                        if message[0] == addr:
                            #Pickle the player's info
                            db = shelve.open("userDB")
                            player = db[name]
                            for i in range(len(player)):
                                if i != 3:
                                    player[i] += mssg[i]
                                else:
                                    player[i] = mssg[i]
                            db[name] = player
                            db.close()
                        else:
                            mssgLock.acquire() #Acquire lock
                            transmitter.set(name, mssg)
                            print(mssg)
                            transmitter.transmit("ctrl", message[0], port)
                            mssgLock.release() #Release lock
                            time.sleep(1)
                            mssgLock.acquire() #Acquire lock
                            transmitter.set(name, "stop")
                            transmitter.transmit("ctrl", message[0], port)
                            mssgLock.release() #Release lock
                        del clients[clientAddr]
                        del statistics[clientAddr]
                        clntLock.release() #Release lock
                        actuNum -= 1
                        return 
                    else:
                        #The player just joined and wants to pass on his/her info
                        info = eval(str(message[2]))
                        clntLock.acquire() #Acquire lock
                        clients[message[0]] = info[0] #name
                        statistics[message[0]] = [[], 0, info[1], info[2], False, "lost"] #[points], turnNum, fundsAvailable, fundsBetted, fundsInsured
                        clntLock.release() #Release lock
                elif message[1] == "chat":
                    #The player wants to send a message to everyone
                    mssgLock.acquire() #Acquire lock
                    transmitter.set(clients[message[0]], message[2])
                    transmitter.broadcast("chat")
                    mssgLock.release() #Release lock
                elif message[1] == "cmmd":
                    #The player wants to play
                    if indx < maxClients and message[0] == clientOnIp:
                        if message[2] == "hit":
                            getCard(message[0], port)
                        elif message[2] == "stick":
                            indx += 1
                            mssg ="***%s - STICK***" % (clients[message[0]])
                            print(mssg)
                            mssgLock.acquire() #Acquire lock
                            transmitter.set("", mssg)
                            transmitter.broadcast("cmmd")
                            mssgLock.release() #Release lock
                            informAboutTurn()
                        elif message[2] == "double_down" and statistics[clientOnIp][1] == 0:
                            getCard(message[0], port)
                            clntLock.acquire() #Acquire lock
                            betInc = statistics[clientOnIp][3]*2
                            statistics[clientOnIp][3] = betInc
                            clntLock.release() #Release lock
                            indx += 1
                            mssg ="***%s - DOUBLE DOWN***" % (clients[message[0]])
                            print(mssg)
                            mssgLock.acquire() #Acquire lock
                            transmitter.set("", mssg)
                            transmitter.broadcast("cmmd")
                            mssgLock.release() #Release lock
                            informAboutTurn()
                        elif message[2] == "take_out_insurance" and statistics[clientOnIp][1] == 0 and int(dealerPnts[0]) == 1: 
                            clntLock.acquire() #Acquire lock
                            statistics[clientOnIp][4] = True
                            clntLock.release() #Release lock
                            mssg ="***%s - TAKE OUT INSURANCE***" % (clients[message[0]])
                            print(mssg)
                            mssgLock.acquire() #Acquire lock
                            transmitter.set("", mssg)
                            transmitter.broadcast("cmmd")
                            mssgLock.release() #Release lock
                        elif message[2] == "surrender" and statistics[clientOnIp][1] == 0:
                            clntLock.acquire() #Acquire lock
                            statistics[clientOnIp][5] = "surrendered"
                            bet50 = statistics[clientOnIp][3]/2
                            funds = statistics[clientOnIp][2]
                            funds += bet50
                            statistics[clientOnIp][2] = funds
                            clntLock.release() #Release lock
                            indx += 1
                            mssg ="***%s - SURRENDER***" % (clients[message[0]])
                            print(mssg)
                            mssgLock.acquire() #Acquire lock
                            transmitter.set("", mssg)
                            transmitter.broadcast("cmmd")
                            mssgLock.release() #Release lock
                            informAboutTurn()
    except:
        pass

def getCard(client, recvPort):
    """Gives the player a card."""
    deckLock.acquire() #Acquire lock
    card = deck.rem()
    deckLock.release() #Release lock
    clntLock.acquire() #Acquire lock
    calcPoint(client, card)
    clntLock.release() #Release lock
    strCard = str(card)
    name = clients[client]
    mssg = "***%s - HIT: %s***" % (name, strCard)
    print(mssg)
    mssgLock.acquire() #Acquire lock
    transmitter.set("", mssg)
    transmitter.broadcast("cmmd")
    mssgLock.release() #Release lock
    return

def calcPoint(playerIp, card):
    """Calculates how many points the player should receive."""
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
    """Removes all points over 21 from the player."""
    global indx
    index = len(statistics[playerIp][0]) - 1
    while index != -1:
        if statistics[playerIp][0][index] > 21:
            statistics[playerIp][0].pop(index)
        index -= 1
    if statistics[playerIp][0] == []:
        indx += 1
        informAboutTurn()
    return

def informAboutTurn():
    """Sends a message to every player so they know who's turn it is."""
    global clientOnIp, indx
    try:
        clientOnIp = sorted(clients)[indx]
    except IndexError:
        clientOnIp = "dealer"
    if clientOnIp != "dealer":
        mssg = "***%s's TURN***" %(clients[clientOnIp])
    else:
        mssg = "***DEALER's TURN***"
    mssgLock.acquire() #Acquire lock
    transmitter.set("", mssg)
    transmitter.broadcast("cmmd")
    mssgLock.release() #Release lock
    print(mssg)
    if clientOnIp == "dealer":
        dealerTurn()
    return

def dealerTurn():
    #It's the dealer's turn
    global deck, clientOnIp, dealerHand, dealerPnts
    mssg = "***DEALER: %s***" % str(dealerHand[1])
    print(mssg)
    mssgLock.acquire() #Acquire lock
    transmitter.set("", mssg)
    transmitter.broadcast("cmmd")
    mssgLock.release() #Release lock
    while sum([int(card) for card in dealerPnts]) < 17:
        #The dealer must get a hard 17
        deckLock.acquire() #Acquire lock
        dealerHand += [deck.rem()]
        dealerPnts += [dealerHand[len(dealerHand) - 1]._val]
        deckLock.release() #Release lock
        mssg = "***DEALER: %s***" % str(dealerHand[len(dealerHand) - 1])
        print(mssg)
        mssgLock.acquire() #Acquire lock
        transmitter.set("", mssg)
        transmitter.broadcast("cmmd")
        mssgLock.release() #Release lock
        print("hi")
    for client in statistics:
        if statistics[client][5] != "surrendered":
            if sum([int(card) for card in dealerPnts]) == 21 and len(dealerPnts) == 2:
                #dealer has blackjack
                if max(statistics[client][0]) == 21:
                    #player reached 21
                    statistics[client][5] = "draw"
                else:
                    #player didn't reach 21
                    statistics[client][5] = "lost"
            elif sum([int(card) for card in dealerPnts]) > 21:
                #dealer went bust
                if len(statistics[client][0]) == 0:
                    #blayer went bust
                    statistics[client][5] = "draw"
                else:
                    #player didn't go bust
                    statistics[client][5] = "won"
            else:
                #dealer isn't bust but doesn't have  blackjack
                if len(statistics[client][0]) == 0:
                    #player went bust
                    statistics[client][5] = "lost"
                elif max(statistics[client][0]) < sum([int(card) for card in dealerPnts]):
                    #player has less points than the dealer
                    statistics[client][5] = "lost"
                elif max(statistics[client][0]) == sum([int(card) for card in dealerPnts]):
                    #player has the same amount of points as the dealer
                    statistics[client][5] = "draw"
                else:
                    #player has more points than the dealer
                    statistics[client][5] = "won"
        mssg = "***%s - %s***" % (clients[client], statistics[client][5])
        print(mssg)
        mssgLock.acquire() #Acquire lock
        transmitter.set("", mssg)
        transmitter.broadcast("cmmd")
        mssgLock.release() #Release lock
    return

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

    def broadcast(self, command, no=""):
        """Sends a message to every player."""
        for client in clients:
            if client != no:
                try:
                    if command == "chat":
                        self.transmit(command, client, chat)
                    elif command == "cmmd":
                        self.transmit(command, client, port)
                except:
                    pass
        return

    def transmit(self, mssgType, client, portNum):
        """Establishes a connection, creates a standardised message and sends it over the connection."""
        self._sock = socket(AF_INET, SOCK_STREAM)
        self._sock.connect((client, portNum))
        message = str((self._id, mssgType, self._mssg))
        self._sock.sendall(message.encode())
        self._sock.close()

#Setting up
addr = gethostbyname(gethostname())
port = 5000
chat = 4000
transmitter = Transmitter()
deck = ""

#Taking care of the dealer
dealerHand = []
dealerPnts = []

#Limiting the number of players
clntNum = -1
actuNum = 0
maxClients = 0

#Locking functionality
deckLock = Lock()
clntLock = Lock()
mssgLock = Lock()

#Keeping track of the players' info and who's turn it is
clients = {} #{ip:name}
statistics = {} #{ip:[[points], turnNum, fundsAvailable, fundsBetted, fundsInsured, ending]
indx = 0
clientOnIp = ""

if len(argv) == 4:
    setUpGame(int(argv[1]), int(argv[2]), int(argv[3]))
elif len(argv) == 3:
    setUpGame(int(argv[1]), int(argv[2]))
elif len(argv) == 2:
    setUpGame(int(argv[1]))
elif len(argv) == 1:
    setUpGame()
else:
    pass
