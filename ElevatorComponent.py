from multiprocessing import Process, Pipe
from CommunicationManager import *

from abc import abstractmethod
from enum import Enum


class STATE(Enum):
    NONE = "No State"


class ElevatorComponent(Process):

    def __init__(self):
        super().__init__()
        self.state = STATE.NONE
        self.state_comm = None
        pass

    def run(self):
        self.main()

    def change_state(self, next_state):
        self.state = next_state

    def state_communication(self):
        while True:
            bSendState = self.state_comm.recv()
            if bSendState is True:
                self.state_comm.send(self.state)


    @abstractmethod
    def state_processor(self): raise NotImplementedError

    @abstractmethod
    def main(self): raise NotImplementedError

    """
    Need Abstract Methods used for Logging
    """

