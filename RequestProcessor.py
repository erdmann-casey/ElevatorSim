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
        self.input_car = None  # Key 0 is Elevator Car, Key 1 is Floor 1, Key 2 is Floor 2, etc.
        self.input_floor1 = None
        self.input_floor2 = None
        self.input_floor3 = None
        self.input_floor4 = None
        self.input_floor5 = None
        self.next = None
        # Received Messages
        self.in_msg = {}  # Key 0 is MsgReq from ElevCar, Key 1 is from Floor 1, Key 2 Floor 2, etc.
        self.next_msg = None
        # output
        self.out = None
        # component vars
        self.q = Queue()             # Queue<entity>
        self.job = None              # entity
        self.processing_time = 2.00  # double, set here arbitrarily
        self.state = STATE.PASSIVE   # state is inherited from ElevatorComponent

    def poll_input(self, id):
        if id == 0:
            return self.input_car.poll()
        if id == 1:
            return self.input_floor1.poll()
        if id == 2:
            return self.input_floor2.poll()
        if id == 3:
            return self.input_floor3.poll()
        if id == 4:
            return self.input_floor4.poll()
        if id == 5:
            return self.input_floor5.poll()

    def receive_input(self, id):
        if id == 0:
            self.in_msg[id] = self.input_car.recv()
            self.q.put(self.in_msg[id])
            self.write_log(self.get_sim_time(), self.get_real_time(), "ElevCar", "RequestProc", "R", self.in_msg[id].contents)
        if id == 1:
            self.in_msg[id] = self.input_floor1.recv()
            self.q.put(self.in_msg[id])
            self.write_log(self.get_sim_time(), self.get_real_time(), "Floor_1", "RequestProc", "R", self.in_msg[id].contents)
        if id == 2:
            self.in_msg[id] = self.input_floor2.recv()
            self.q.put(self.in_msg[id])
            self.write_log(self.get_sim_time(), self.get_real_time(), "Floor_2", "RequestProc", "R", self.in_msg[id].contents)
        if id == 3:
            self.in_msg[id] = self.input_floor3.recv()
            self.q.put(self.in_msg[id])
            self.write_log(self.get_sim_time(), self.get_real_time(), "Floor_3", "RequestProc", "R", self.in_msg[id].contents)
        if id == 4:
            self.in_msg[id] = self.input_floor4.recv()
            self.q.put(self.in_msg[id])
            self.write_log(self.get_sim_time(), self.get_real_time(), "Floor_4", "RequestProc", "R", self.in_msg[id].contents)
        if id == 5:
            self.in_msg[id] = self.input_floor5.recv()
            self.q.put(self.in_msg[id])
            self.write_log(self.get_sim_time(), self.get_real_time(), "Floor_5", "RequestProc", "R", self.in_msg[id].contents)

    def receive_input_all(self):
        for num in range(6):
            if self.poll_input(num):
                self.receive_input(num)
            else:
                continue

    def receive_next(self):
        if self.next.poll():
            self.next_msg = self.next.recv()
            self.write_log(self.get_sim_time(), self.get_real_time(), "ElevCtrl", "RequestProc", "R", self.next_msg.contents)
            return True
        else:
            return False

    def send_out(self, msg):
        self.out.send(msg)
        self.write_log(self.get_sim_time(), self.get_real_time(), "RequestProc", "ElevCtrl", "S", msg.contents)

    def state_processor(self):
        while True:
            if self.state == STATE.PASSIVE:
                self.receive_input_all()

                if self.q.empty():
                    self.change_state(STATE.PASSIVE)
                    continue

                elif not self.q.empty():
                    self.change_state(STATE.SEND_JOB)
                    continue

            elif self.state == STATE.SEND_JOB:
                if not self.q.empty():
                    self.job = self.q.get()
                    self.send_out(self.job)
                    self.job = None
                    self.change_state(STATE.BUSY)
                    continue

            elif self.state == STATE.BUSY:
                self.receive_input_all()

                if self.q.empty():
                    self.change_state(STATE.BUSY)
                    continue

                elif self.next.poll():
                    self.receive_next()
                    if self.next_msg.contents.get("ELEV") is True:
                        self.change_state(STATE.SEND_JOB)
                        continue

    def main(self):
        self.state_processor()


if __name__ == '__main__':
    rp = RequestProcessor()
    rp.main()
