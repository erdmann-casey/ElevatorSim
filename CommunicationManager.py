import socket
import pickle
import queue

from threading import *


class Server(Thread):
    HOST = socket.gethostname()  # localhost
    PORT = 4545                  # arbitrary port
    SOCK = None
    received_msgs = queue.Queue()

    def __init__(self, host, port):
        Thread.__init__(self)
        self.HOST = host
        self.PORT = port
        self.start()
        pass

    def run(self):
        self.SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ADDR = (self.HOST, self.PORT)
        self.SOCK.bind(ADDR)
        self.SOCK.listen(8)  # arbitrary number of connections

        while True:
            (client_sock, client_addr) = self.SOCK.accept()
            client_data = self.SOCK.recv(2018)  # arbitrary size
            client_sock.close()

            self.received_msgs.put(pickle.loads(client_data))
        pass


class ThreadedClass(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()

    def run(self):
        pass


class CommunicationManager(object):

    listen_server = None

    def __init__(self):
        # Create Listen Server Thread
        # Handle Client operations
        pass

    """
    Send a single message to a single recipient
    
    msg       :: the Msg object to send
    recipient :: the address ((host, port)) of the recipient
    """
    @staticmethod
    def send(msg, recipient):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(recipient)
        msg_serialized = pickle.dumps(msg)
        s.send(msg_serialized)
        s.close()
        pass

