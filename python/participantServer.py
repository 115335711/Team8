from socket import *

portNum = 9900

class Server(object):

    def __init__(self, name):
        """Set up the server on the predetermined IP address and port number, wait for an incoming connection and display any chat messages received."""
        self._addr = gethostbyname(gethostname())
        self._port = portNum
        self._sock = socket(AF_INET, SOCK_STREAM) #Creates a socket that uses TCP
        self._sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #Make the socket reusable
        self._sock.bind((self._addr, self._port)) #Open a connection on the predetermined IP address and portnumber
        print("Server opened @ %s: %s" % (self._addr, self._port))
        self._sock.listen(1) #Bind the server to have exactly one connection open
        try:
            data = ""
            while True:
                self._connection, self._clientAddr = self._sock.accept() #Accept the first incoming connection and save the client's IP address and port number
                data = self._connection.recv(1024).decode()
                if data:
                    message = eval(str(data))
                    if message[1] == "chat":
                        #Change to display message in the textbox
                        print("<%s>: %s" % (message[0], message[2]))
                    elif message[1] == "ctrl":
                        if message[2] == "stop":
                            self.close()
                            return
                    else:
                        pass
                else:
                    pass
        except ConnectionResetError:
            print("Error")
            self.close()
        finally:
            self.close()
            return

    def close(self):
        """Closes the established connection."""
        self._connection.close()
        self._sock.close()
        return
        
