from multiprocessing import Queue

from ElevatorComponent import ElevatorComponent
from Messages import *
from threading import Thread


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
        self.in_msg = None
        self.next = None
        self.next_msg = None
        # output
        self.out = None
        # component vars
        self.q = Queue()             # Queue<entity>
        self.job = None              # entity
        self.processing_time = None  # double
        self.state = STATE.PASSIVE   # state is inherited from ElevatorComponent

    def state_processor(self):
        while True:
            if self.state is STATE.PASSIVE:
                self.receive_input()
                if self.q.empty() and self.job is None:
                    self.change_state(STATE.PASSIVE)
                elif not self.q.empty() and self.job is not None:
                    self.change_state(STATE.SEND_JOB)

            elif self.state is STATE.SEND_JOB:
                if not self.q.empty():
                    self.job = self.q.get()
                    self.out.send(self.job)
                    self.job = None
                    self.change_state(STATE.BUSY)

            elif self.state is STATE.BUSY:
                if self.next_msg.contents.get("ELEV") is False or self.q.empty():
                    self.change_state(STATE.BUSY)

                elif self.next_msg.contents.get("ELEV") is True and not self.q.empty():
                    self.change_state(STATE.SEND_JOB)

                elif self.receive_next() and self.next_msg.contents.get("ELEV") is not None and not self.q.empty():
                    # Perform necessary actions
                    # next ? sendNext
                    self.change_state(STATE.SEND_JOB)

                elif self.job is not None and not self.q.empty() and self.next_msg.contents.get("ELEV") is True:
                    # Perform necessary actions
                    # in ? job in q
                    self.change_state(STATE.SEND_JOB)

    def receive_input(self):
        if self.input.poll():
            self.in_msg = self.input.recv()  # msg is a Floor Request
            self.q.put(self.in_msg)
            self.job = self.in_msg
            return True
        else:
            return False

    def receive_next(self):
        if self.next.poll():
            self.next_msg = self.next.recv()
            return True
        else:
            return False

    def main(self):
        self.state_processor()


if __name__ == '__main__':
    rp = RequestProcessor()
    rp.main()
