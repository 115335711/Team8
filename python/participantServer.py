#!/usr/bin/env python3

from socket import *

class Server(object):

    def __init__(self, mode, port):
        """Sets up a server on a predetermined IP address and port number, waits for an incoming connection and displays any messages received."""
        self._addr = gethostbyname(gethostname())
        self._port = port
        self._sock = socket(AF_INET, SOCK_STREAM) #Creates a socket that uses TCP
        self._sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #Make the socket reusable
        self._sock.bind((self._addr, self._port)) #Open a connection on the predetermined IP address and portnumber
        print("Server opened @ %s: %s" % (self._addr, self._port))
        self._sock.listen(1)
        try:
            data = ""
            while True:
                self._connection, self._clientAddr = self._sock.accept() #Accept the first incoming connection and save the client's IP address and port number
                data = self._connection.recv(1024).decode()
                if data:
                    message = eval(str(data))
                    if message[1] == "ctrl":
                        if message[2] == "stop":
                            self.close()
                    elif mode == "chat" and message[1] == "chat":
                        print("<%s>: %s" % (message[0], message[2]), end="")
                    elif mode == "cmmd" and message[1] == "cmmd":
                        print(message[2])
        except:
            self.close()
        finally:
            self.close()

    def close(self):
        """Closes the established connection."""
        self._connection.close()
        self._sock.close()
        return
