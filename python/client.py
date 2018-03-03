from socket import *

class Client(object):

    def __init__(self, name, hostAddr, hostPort):
        """Sets up the client and establishes a connection with the host."""
        self._addr = gethostbyname(gethostname())
        self._hostAddr = hostAddr
        self._hostPort = hostPort
        self._pnts = [0, 0]
        self._fundsAvailable = 500
        self._fundsBetted = 10
        self._fundsInsured = 0
        self._sock = socket(AF_INET, SOCK_STREAM) #Creates a socket that uses TCP
        try:
            self._connection = self._sock.connect((self._hostAddr, self._hostPort)) #Creates a connection with the host's IP address and port number
            info = (name, self._pnts, self._fundsAvailable, self._fundsBetted, self._fundsInsured)
            self.transmit("ctrl", info)
        except:
            self.close()
        finally:
            return

    def hit(self):
        self.transmit("cmmd", "hit")
        return

    def stick(self):
        self.transmit("cmmd", "stick")
        return

    def doubleDown(self):
        self.transmit("cmmd", "double_down")
        return
    
    def takeOutInsurence(self):
        self.transmit("cmmd", "take_out_insurence")
        return

    def surrender(self):
        self.transmit("cmmd", "surrender")
        return
    
    def transmit(self, mssgType, mssg):
        """Creates a standardised message and sends it over the established connection."""
        mssgStr = str(mssg)
        message = str((self._addr, mssgType, mssgStr))
        self._sock.sendall(message.encode())

    def close(self):
        """Closes the established connection."""
        self._sock.close()
