from ElevatorComponent import ElevatorComponent
from Messages import *


class STATE(Enum):
    """
    States used exclusively by Elevator Controller
    """
    IDLE = "idle"
    MOVE = "move"
    STOP = "stop"
    WAIT_FOR_CAR_READY = "waitForCarReady"
    MOVE_UP = "moveUP"
    MOVE_DOWN = "moveDOWN"
    MOVING_UP = "movingUP"
    MOVING_DOWN = "movingDOWN"
    WAIT_FOR_CAR_OPEN = "waitForCarOpen"
    WAIT_FOR_CAR_CLOSE = "waitForCarClose"
    DONE = "done"


class ElevatorController(ElevatorComponent):

    def __init__(self):
        super().__init__()
        # input
        self.iReq = None     # Received from Request Processor
        self.iStCar = None   # Received from Elevator Car
        self.iStDoor = None  # Received from Door Status Processor
        # Received Messages
        self.iReq_msg = None
        self.iStCar_msg = None
        self.iStDoor_msg = None
        # output
        self.oCmdCar = None    # Recipient is Elevator Car
        self.oCmdFloor1 = None  # Recipient is Floor(s)
        self.oCmdFloor2 = None  # Recipient is Floor(s)
        self.oCmdFloor3 = None  # Recipient is Floor(s)
        self.oCmdFloor4 = None  # Recipient is Floor(s)
        self.oCmdFloor5 = None  # Recipient is Floor(s)
        self.out = None        # Recipient is Door Status Process
        self.done = None       # Recipient is Request Processor
        # vars
        self.curFloor = 0         # int
        self.destFloor = 0        # int
        self.isGoUp = None        # boolean
        self.isGoDown = None      # boolean
        self.isOperating = None   # boolean TODO: Set within main loop
        self.statusDoor = None    # string
        self.statusCar = None     # string
        self.reset = True         # boolean, otherwise known as "mode" or "reset mode"
        self.state = STATE.IDLE

    def receive_iReq(self):
        if self.iReq.poll():
            self.iReq_msg = self.iReq.recv()
            self.destFloor = self.iReq_msg.contents.get("value").get("REQ")
            self.write_log(self.get_sim_time(), self.get_real_time(), "RequestProc", "ElevCtrl", "R", "iReq", self.iReq_msg)
            if self.destFloor > self.curFloor:
                self.isGoUp = True
            elif self.destFloor < self.curFloor:
                self.isGoDown = True
            return True
        else:
            return False

    def receive_iStCar(self):
        if self.iStCar.poll():
            self.iStCar_msg = self.iStCar.recv()
            self.statusCar = self.iStCar_msg.contents.get("value")
            self.write_log(self.get_sim_time(), self.get_real_time(), "ElevCar", "ElevCtrl", "R", "iStCar", self.iStCar_msg)
            return True
        else:
            return False

    def receive_iStDoor(self):
        if self.iStDoor.poll():
            self.iStDoor_msg = self.iStDoor.recv()
            self.statusDoor = self.iStDoor_msg.contents.get("value")
            self.write_log(self.get_sim_time(), self.get_real_time(), "DoorStatusProc", "ElevCtrl", "R", "iStDoor", self.iStDoor_msg)
            return True
        else:
            return False

    def send_oCmdCar(self, msg):
        self.oCmdCar.send(msg)
        self.write_log(self.get_sim_time(), self.get_real_time(), "ElevCtrl", "ElevCar", "S", "oCmdCar", msg)

    def send_oCmdFloor(self, id, msg):
        if id is 1:
            self.oCmdFloor1.send(msg)
            self.write_log(self.get_sim_time(), self.get_real_time(), "ElevCtrl", "Floor_1", "S", "oCmdFloor", msg)

        elif id is 2:
            self.oCmdFloor2.send(msg)
            self.write_log(self.get_sim_time(), self.get_real_time(), "ElevCtrl", "Floor_2", "S", "oCmdFloor", msg)

        elif id is 3:
            self.oCmdFloor3.send(msg)
            self.write_log(self.get_sim_time(), self.get_real_time(), "ElevCtrl", "Floor_3", "S", "oCmdFloor", msg)

        elif id is 4:
            self.oCmdFloor4.send(msg)
            self.write_log(self.get_sim_time(), self.get_real_time(), "ElevCtrl", "Floor_4", "S", "oCmdFloor", msg)

        elif id is 5:
            self.oCmdFloor5.send(msg)
            self.write_log(self.get_sim_time(), self.get_real_time(), "ElevCtrl", "Floor_5", "S", "oCmdFloor", msg)

    def send_out(self, msg):
        self.out.send(msg)
        self.write_log(self.get_sim_time(), self.get_real_time(), "ElevCtrl", "DoorStatusProc", "S", "oCmdFloor", msg)

    def send_done(self, msg):
        self.done.send(msg)
        self.write_log(self.get_sim_time(), self.get_real_time(), "ElevCtrl", "RequestProc", "S", "oCmdFloor", msg)

    def state_processor(self):
        while True:
            if self.state == STATE.IDLE:
                if self.receive_iReq():
                    if self.curFloor == self.destFloor:
                        continue
                    if not self.isOperating and self.reset is True:
                        self.change_state(STATE.MOVE)
                        continue
                    elif not self.isOperating and self.reset is False:
                        self.change_state(STATE.STOP)
                        continue

            if self.state == STATE.MOVE:
                self.reset = False
                self.send_oCmdCar(MsgCar("oCmdCar", CommandCar.CAR_MOVE, self.curFloor, self.destFloor, True))
                self.send_oCmdFloor(self.destFloor, MsgDoor("oCmdFloor", CommandDoor.DOOR_FLOOR_X_CLOSE, self.destFloor, True))
                self.send_out(MsgElev("out", self.destFloor))
                self.change_state(STATE.WAIT_FOR_CAR_READY)
                continue

            if self.state == STATE.WAIT_FOR_CAR_READY:
                if self.iStDoor.poll():
                    self.receive_iStDoor()
                if self.iStCar.poll():
                    self.receive_iStCar()

                if self.iStDoor_msg is not None and self.iStCar_msg is not None:
                    if self.iStDoor_msg.contents.get("value") == StatusDoor.DOOR_BOTH_CLOSED and self.iStCar_msg.contents.get("value") == StatusCar.CAR_READY_TO_MOVE and self.isGoUp:
                        self.change_state(STATE.MOVE_UP)
                        continue
                    elif self.iStDoor_msg.contents.get("value") == StatusDoor.DOOR_BOTH_CLOSED and self.iStCar_msg.contents.get("value") == StatusCar.CAR_READY_TO_MOVE and self.isGoDown:
                        self.change_state(STATE.MOVE_DOWN)
                        continue

            if self.state == STATE.MOVE_UP:
                self.isGoUp = True
                self.send_oCmdCar(MsgCar("oCmdCar", CommandCar.CAR_UP, self.curFloor, self.destFloor, True))
                self.change_state(STATE.MOVING_UP)
                continue

            if self.state == STATE.MOVE_DOWN:
                self.isGoDown = True
                self.send_oCmdCar(MsgCar("oCmdCar", CommandCar.CAR_DOWN, self.curFloor, self.destFloor, True))
                self.change_state(STATE.MOVING_DOWN)
                continue

            if self.state == STATE.MOVING_UP:
                if self.iStDoor.poll():
                    self.receive_iStDoor()
                if self.iStCar.poll():
                    self.receive_iStCar()
                if self.iStDoor_msg.contents.get("value") == StatusDoor.DOOR_BOTH_CLOSED and self.iStCar_msg.contents.get("value") == StatusCar.CAR_STOPPED:  # and not self.isGoUp and not self.isGoDown:
                    self.change_state(STATE.STOP)
                    continue

            if self.state == STATE.MOVING_DOWN:
                if self.iStDoor.poll():
                    self.receive_iStDoor()
                if self.iStCar.poll():
                    self.receive_iStCar()
                if self.iStDoor_msg.contents.get("value") == StatusDoor.DOOR_BOTH_CLOSED and self.iStCar_msg.contents.get("value") == StatusCar.CAR_STOPPED:  # and not self.isGoUp and not self.isGoDown:
                    self.change_state(STATE.STOP)
                    continue

            if self.state == STATE.STOP:
                self.isGoUp = False
                self.isGoDown = False
                self.curFloor = self.destFloor
                # self.send_oCmdCar(MsgCar(CommandCar.CAR_STOP, self.curFloor, self.destFloor, True))
                self.send_oCmdCar(MsgDoor("oCmdCar", CommandDoor.DOOR_CAR_OPEN, self.curFloor, True))
                self.send_oCmdFloor(self.destFloor, MsgDoor("oCmdFloor", CommandDoor.DOOR_FLOOR_X_OPEN, self.destFloor, True))
                self.change_state(STATE.WAIT_FOR_CAR_OPEN)
                continue

            if self.state == STATE.WAIT_FOR_CAR_OPEN:
                if self.iStDoor.poll():
                    self.receive_iStDoor()
                if self.iStCar.poll():
                    self.receive_iStCar()
                    if self.iStCar_msg.contents.get("value") == StatusCar.CAR_OPENING:  # and self.iStDoor_msg.contents.get("value") == StatusDoor.DOOR_BOTH_OPENED:
                        self.change_state(STATE.WAIT_FOR_CAR_CLOSE)
                        continue

            if self.state == STATE.WAIT_FOR_CAR_CLOSE:
                if self.iStDoor.poll():
                    self.receive_iStDoor()
                if self.iStCar.poll():
                    self.receive_iStCar()
                    if self.iStDoor_msg.contents.get("value") == StatusDoor.DOOR_BOTH_CLOSED and (self.iStCar_msg.contents.get("value") == StatusCar.CAR_STOPPED or self.iStCar_msg.contents.get("value") == StatusCar.CAR_READY_TO_MOVE):
                        self.change_state(STATE.DONE)
                        continue

            if self.state == STATE.DONE:
                self.send_done(MsgElev("done", True))  # "done" or True
                self.reset = True
                self.change_state(STATE.IDLE)
                continue

    def main(self):
        self.state_processor()

    def run(self):
        self.main()


if __name__ == '__main__':
    ec = ElevatorController()
    ec.main()
