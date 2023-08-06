"a client conection used for comunication subscript"

from socket import socket
from pickle import dumps, loads
from jpe_types.paralel import Thread

class client:
    """a container for sockets and ip addresses at current
    """
    def __init__(self, con: socket, ip: int, name: str):
        """crates container

        @param con: the socket to connect to
        @type con: socket.socket

        @param ip: the ip addres the sock is connected to
        @type ip: int

        @param name: the name of the client
        @type name: a string
        """

        self.active = True
        "weather or not the client is active"

        self.sock = con
        "the socket its connected to"

        self.ip = ip
        "the ip the sock is connected to"

        self.name=name
        "the name of the client (str)"
    
    def send(self, data, flags=0):
        """send data

        Send data to the socket. The socket must be connected to a remote socket. The optional flags argument has the same meaning as for recv() above. Returns the number of bytes sent. Applications are responsible for checking that all data has been sent; if only some of the data was transmitted, the application needs to attempt delivery of the remaining data. For further information on this topic, consult the Socket Programming HOWTO.
        """
        self.sock.send(dumps(data))

    def __str__(self):
        return self.name

    def recv(self, bufsize, flags=0):
        """receve data

        Receive data from the socket. The return value is a bytes object representing the data received. The maximum amount of data to be received at once is specified by bufsize. See the Unix manual page recv(2) for the meaning of the optional argument flags; it defaults to zero.

        Note

            - For best match with hardware and network realities, the value of bufsize should be a relatively small power of 2, for example, 4096.

    
        from: https://docs.python.org/3/library/socket.html#socket-objects
        """
        res = loads(self.sock.recv(bufsize))
        return res

    def startListening(self, fun, bufferSize: int, flags=0):
        """starts listening for updats
        
        start a jpe_types thread to run self.getUpdate
        
        @param fun: the function to be run
        @type fun: function

        @param bufferSize: the size for socket.recv
        @type bufferSize: int

        @param flags: flags for socket.recv
        @type flags: see socket doc"""

        self.listening_Thread = Thread(target=self.getUpdate,
                                       args=(fun, bufferSize),
                                       kwargs={"flags": flags},
                                       daemon=True,
                                       name=f"client_{self.name}_Listener")
        "the thread used to listen for updates"
        self.listening_Thread.start()
                                       
    def getUpdate(self, fun, bufferSize:int, flags=0):
        """get updates

        run in a Thread and will run fun each time it gets an update

        @param fun: the function to be run
        @type fun: function

        @param bufferSize: the size for socket.recv
        @type bufferSize: int

        @param flags: flags for socket.recv
        @type flags: see socket doc
        """
        while self.active:
            try:
                res = self.recv(bufferSize, flags=flags)
            except Exception as e:
                print(f"client {self} get update error {e}")

            fun(*res, self)
    
    def _close(self):
        self.active = False
        self.sock.close()
    
