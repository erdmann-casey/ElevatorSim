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
        self.input = None
        self.next = None
        # Received Messages
        self.in_msg = None
        self.next_msg = None
        # output
        self.out = None
        # component vars
        self.q = Queue()             # Queue<entity>
        self.job = None              # entity
        self.processing_time = None  # double
        self.state = STATE.PASSIVE   # state is inherited from ElevatorComponent

    def receive_input(self):
        if self.input.poll():
            self.in_msg = self.input.recv()  # msg is a Floor Request
            self.q.put(self.in_msg)
            self.job = self.in_msg
            # TODO: Fill In Proper Times
            self.write_log(0, 0, "[Sender]", "RequestProc", "R", self.in_msg.contents)
            return True
        else:
            return False

    def receive_next(self):
        if self.next.poll():
            self.next_msg = self.next.recv()
            # TODO: Fill In Proper Times
            self.write_log(0, 0, "ElevCtrl", "RequestProc", "R", self.next_msg.contents)
            return True
        else:
            return False

    def send_out(self, msg):
        self.out.send(msg)
        # TODO: Fill In Proper Times
        self.write_log(0, 0, "RequestProc", "ElevCtrl", "S", self.msg.contents)

    def state_processor(self):
        while True:
            if self.state is STATE.PASSIVE:
                if self.input.poll():
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
                if self.input.poll():
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
