from multiprocessing import Queue

from ElevatorComponent import ElevatorComponent
from Messages import *


class STATE(Enum):
    """
    States used exclusively by Request Processor
    """
    PASSIVE = "passive"
    SEND_JOB = "sendJob"
    BUSY = "busy"


class RequestProcessor(ElevatorComponent):

    def __init__(self):
        super().__init__()
        # input
        self.input = dict()  # Key 0 is Elevator Car, Key 1 is Floor 1, Key 2 is Floor 2, etc.
        self.next = None
        # Received Messages
        self.in_msg = {}  # Key 0 is MsgReq from ElevCar, Key 1 is from Floor 1, Key 2 Floor 2, etc.
        self.next_msg = None
        # output
        self.out = None
        # component vars
        self.q = Queue()             # Queue<entity>
        self.job = None              # entity
        self.processing_time = None  # double
        self.state = STATE.PASSIVE   # state is inherited from ElevatorComponent


    def poll_input(self):
        index = 0
        for conn in self.input:
            if conn.poll():
                return True
            else:
                index += 1
                continue
        return False

    def receive_input(self):
        index = 0
        for conn in self.input:
            if conn.poll():
                self.in_msg[index] = conn.recv()  # msg is a Floor Request
                self.q.put(self.in_msg[index])
                self.job = self.in_msg[index]
                # TODO: Fill In Proper Times
                self.write_log(self.get_sim_time(), self.get_real_time(), "[Sender]", "RequestProc", "R", self.in_msg[index].contents)
                return True
            else:
                index += 1
                continue
        return False

    def receive_next(self):
        if self.next.poll():
            self.next_msg = self.next.recv()
            # TODO: Fill In Proper Times
            self.write_log(self.get_sim_time(), self.get_real_time(), "ElevCtrl", "RequestProc", "R", self.next_msg.contents)
            return True
        else:
            return False

    def send_out(self, msg):
        self.out.send(msg)
        # TODO: Fill In Proper Times
        self.write_log(self.get_sim_time(), self.get_real_time(), "RequestProc", "ElevCtrl", "S", msg.contents)

    def state_processor(self):
        while True:
            if self.state is STATE.PASSIVE:
                if self.poll_input():
                    self.receive_input()

                if self.q.empty() and self.job is None:
                    self.change_state(STATE.PASSIVE)

                elif not self.q.empty() and self.job is not None:
                    self.change_state(STATE.SEND_JOB)

            elif self.state is STATE.SEND_JOB:
                if not self.q.empty():
                    self.job = self.q.get()
                    self.send_out(self.job)
                    self.job = None
                    self.change_state(STATE.BUSY)

            elif self.state is STATE.BUSY:
                # TODO: Fix this code block
                # BUSY -> SENDJOB transition will loop endlessly
                if self.poll_input():
                    self.receive_input()
                    if self.job is not None and not self.q.empty() and self.next_msg.contents.get("ELEV") is True:
                        self.change_state(STATE.SEND_JOB)

                if self.next.poll():
                    self.receive_next()
                    if self.next_msg.contents.get("ELEV") is False or self.q.empty():
                        self.change_state(STATE.BUSY)

                    elif self.next_msg.contents.get("ELEV") is True and not self.q.empty():
                        self.change_state(STATE.SEND_JOB)

                    elif self.next_msg.contents.get("ELEV") is not None and not self.q.empty():
                        self.change_state(STATE.SEND_JOB)

    def main(self):
        self.state_processor()


if __name__ == '__main__':
    rp = RequestProcessor()
    rp.main()
