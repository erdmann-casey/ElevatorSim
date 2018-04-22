from multiprocessing import Process
from abc import abstractmethod
from enum import Enum
from time import time


class STATE(Enum):
    NONE = "No State"


class ElevatorComponent(Process):

    def __init__(self):
        super().__init__()
        self.state = STATE.NONE
        self.state_comm = None
        self.start_time = time()
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

    def write_log(self, sim_time, real_time, sender, receiver, action, msg_contents):
        log_str = "{}, {}, {}, {}, {}, {}\n".format(sim_time, real_time, sender, receiver, action, msg_contents)
        file = open("logs.txt", "a+")
        file.write(log_str)
        file.close()

    def get_sim_time(self):
        return time() - self.start_time

    def get_real_time(self):
        return time()

    @abstractmethod
    def state_processor(self): raise NotImplementedError

    @abstractmethod
    def main(self): raise NotImplementedError
