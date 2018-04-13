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

                msg = self.input.recv()  # msg is a Floor Request
                print(msg.contents)
                self.q.put(msg)
                self.job = msg

                if self.q.empty() and self.job is None:
                    # Perform necessary actions
                    self.change_state(STATE.PASSIVE)
                elif not self.q.empty() and self.job is not None:
                    # Perform necessary actions
                    self.change_state(STATE.SEND_JOB)
            elif self.state is STATE.SEND_JOB:
                # out ! job
                if not self.q.empty():
                    # Perform necessary actions
                    # send a message via self.out
                    self.change_state(STATE.BUSY)
            elif self.state is STATE.BUSY:
                """
                if self.done is False or self.q.empty():
                    # Perform necessary actions
                    self.change_state(STATE.BUSY)
                elif self.done is True and not self.q.empty():
                    # Perform necessary actions
                    self.change_state(STATE.SEND_JOB)
                elif self.sendNext is not None and not self.q.empty():
                    # Perform necessary actions
                    # next ? sendNext
                    self.change_state(STATE.SEND_JOB)
                elif self.job is not None and not self.q.empty() and self.done is True:
                    # Perform necessary actions
                    # in ? job in q
                    self.change_state(STATE.SEND_JOB)
                """

    def main(self):
        self.state_processor()


if __name__ == '__main__':
    rp = RequestProcessor()
    rp.main()
