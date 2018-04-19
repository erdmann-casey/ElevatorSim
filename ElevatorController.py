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
        self.iReq_msg = Msg(None)
        self.iStCar_msg = Msg(None)
        self.iStDoor_msg = Msg(None)
        # output
        self.oCmdCar = None    # Recipient is Elevator Car
        self.oCmdFloor = {}  # Recipient is Floor(s)
        self.out = None        # Recipient is Door Status Process
        self.done = None       # Recipient is Request Processor
        # vars
        self.curFloor = None      # int TODO: Set within main loop
        self.destFloor = None     # int
        self.isGoUp = None        # boolean
        self.isGoDown = None      # boolean
        self.isOperating = None   # boolean TODO: Set within main loop
        self.statusDoor = None    # string
        self.statusCar = None     # string
        self.reset = False        # boolean, otherwise known as "mode" or "reset mode"
        self.state = STATE.IDLE

    def receive_iReq(self):
        if self.iReq.poll():
            self.iReq_msg = self.iReq.recv()
            self.destFloor = self.iReq_msg.contents.get("REQ")
            # TODO: Fill In Proper Times
            self.write_log(self.get_sim_time(), self.get_real_time(), "RequestProc", "ElevCtrl", "R", self.iReq_msg.contents)
            return True
        else:
            return False

    def receive_iStCar(self):
        if self.iStCar.poll():
            self.iStCar_msg = self.iStCar.recv()
            self.statusCar = self.iStCar_msg.contents.get("content")
            # TODO: Fill In Proper Times
            self.write_log(self.get_sim_time(), self.get_real_time(), "ElevCar", "ElevCtrl", "R", self.iStCar_msg.contents)
            return True
        else:
            return False

    def receive_iStDoor(self):
        if self.iStDoor.poll():
            self.iStDoor_msg = self.iStDoor.recv()
            self.statusDoor = self.iStDoor_msg.contents.get("content")
            # TODO: Fill In Proper Times
            self.write_log(self.get_sim_time(), self.get_real_time(), "DoorStatusProc", "ElevCtrl", "R", self.iStDoor_msg.contents)
            return True
        else:
            return False

    def send_oCmdCar(self, msg):
        self.oCmdCar.send(msg)
        # TODO: Fill In Proper Times
        self.write_log(self.get_sim_time(), self.get_real_time(), "ElevCtrl", "ElevCar", "S", msg.contents)

    def send_oCmdFloor(self, msg):
        self.oCmdFloor[msg.contents.get("id")].send(msg)
        # TODO: Fill In Proper Times
        self.write_log(self.get_sim_time(), self.get_real_time(), "ElevCtrl", "FloorX", "S", msg.contents)

    def send_out(self, msg):
        self.out.send(msg)
        # TODO: Fill In Proper Times
        self.write_log(self.get_sim_time(), self.get_real_time(), "ElevCtrl", "DoorStatusProc", "S", msg.contents)

    def send_done(self, msg):
        self.done.send(msg)
        # TODO: Fill In Proper Times
        self.write_log(self.get_sim_time(), self.get_real_time(), "ElevCtrl", "RequestProc", "S", msg.contents)

    def state_processor(self):
        while True:
            if self.state is STATE.IDLE:
                if self.receive_iReq():
                    if not self.isOperating and self.reset is True:
                        self.change_state(STATE.MOVE)
                    elif not self.isOperating and self.reset is False:
                        self.change_state(STATE.STOP)

            if self.state is STATE.MOVE:
                self.send_oCmdCar(MsgCar(CommandCar.CAR_MOVE, self.curFloor, self.destFloor, True))
                self.send_oCmdFloor(MsgDoor(CommandDoor.DOOR_FLOOR_X_OPEN, self.destFloor, True))
                self.send_out(MsgElev(self.destFloor))
                self.change_state(STATE.WAIT_FOR_CAR_READY)

            if self.state is STATE.WAIT_FOR_CAR_READY:
                if self.iStDoor.poll() and self.iStCar.poll():
                    self.receive_iStDoor()
                    self.receive_iStCar()
                    if self.iStDoor_msg.contents.get("content") is StatusDoor.DOOR_CAR_CLOSED and self.iStCar_msg.contents.get("content") is StatusCar.CAR_READY_TO_MOVE and self.isGoUp:
                        self.change_state(STATE.MOVE_UP)
                    elif self.iStDoor_msg.contents.get("content") is StatusDoor.DOOR_CAR_CLOSED and self.iStCar_msg.contents.get("content") is StatusCar.CAR_READY_TO_MOVE and self.isGoDown:
                        self.change_state(STATE.MOVE_DOWN)

            if self.state is STATE.MOVE_UP:
                self.isGoUp = True
                self.send_oCmdCar(MsgCar(CommandCar.CAR_UP, self.curFloor, self.destFloor, True))
                self.change_state(STATE.MOVING_UP)

            if self.state is STATE.MOVE_DOWN:
                self.isGoDown = True
                self.send_oCmdCar(MsgCar(CommandCar.CAR_DOWN, self.curFloor, self.destFloor, True))
                self.change_state(STATE.MOVING_DOWN)

            if self.state is STATE.MOVING_UP:
                if self.iStDoor.poll() and self.iStCar.poll():
                    self.receive_iStDoor()
                    self.receive_iStCar()
                    if self.iStDoor_msg.contents.get("content") is StatusDoor.DOOR_BOTH_CLOSED and self.iStCar_msg.contents.get("content") is StatusCar.CAR_STOPPED and not self.isGoUp and not self.isGoDown:
                        self.change_state(STATE.STOP)

            if self.state is STATE.MOVING_DOWN:
                if self.iStDoor.poll() and self.iStCar.poll():
                    self.receive_iStDoor()
                    self.receive_iStCar()
                    if self.iStDoor_msg.contents.get("content") is StatusDoor.DOOR_BOTH_CLOSED and self.iStCar_msg.contents.get("content") is StatusCar.CAR_STOPPED and not self.isGoUp and not self.isGoDown:
                        self.change_state(STATE.STOP)

            if self.state is STATE.STOP:
                self.isGoUp, self.isGoDown = False
                self.send_oCmdCar(MsgCar(CommandCar.CAR_STOP, self.curFloor, self.destFloor, True))
                self.send_oCmdFloor(MsgDoor(CommandDoor.DOOR_FLOOR_X_OPEN, self.destFloor, True))
                self.change_state(STATE.WAIT_FOR_CAR_OPEN)

            if self.state is STATE.WAIT_FOR_CAR_OPEN:
                if self.iStDoor.poll() and self.iStCar.poll():
                    self.receive_iStDoor()
                    self.receive_iStCar()
                    if self.iStDoor_msg.contents.get("content") is StatusDoor.DOOR_BOTH_OPENED and self.iStCar_msg.contents.get("content") is StatusCar.CAR_OPENING:
                        self.change_state(STATE.WAIT_FOR_CAR_CLOSE)

            if self.state is STATE.WAIT_FOR_CAR_CLOSE:
                if self.iStDoor.poll() and self.iStCar.poll():
                    self.receive_iStDoor()
                    self.receive_iStCar()
                    if self.iStDoor_msg.contents.get("content") is StatusDoor.DOOR_BOTH_CLOSED and self.iStCar_msg.contents.get("content") is StatusCar.CAR_STOPPED:
                        self.change_state(STATE.DONE)

            if self.state is STATE.DONE:
                self.send_done(MsgElev("done"))
                self.change_state(STATE.IDLE)

    def main(self):
        self.state_processor()

    def run(self):
        self.main()


if __name__ == '__main__':
    ec = ElevatorController()
    ec.main()
