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
        self.iReq_msg = None
        self.iStCar = None   # Received from Elevator Car
        self.iStCar_msg = None
        self.iStDoor = None  # Received from Door Status Processor
        self.iStDoor_msg = None
        # output
        self.oCmdCar = None    # Recipient is Elevator Car
        self.oCmdFloor = None  # Recipient is Floor(s)
        self.out = None        # Recipient is Door Status Process
        self.done = None       # Recipient is Request Processor
        # vars
        self.curFloor = None    # int
        self.destFloor = None   # int
        self.isGoUp = None      # boolean
        self.isGoDown = None    # boolean
        self.isOperating = None   # boolean
        self.statusDoor = None  # string
        self.statusCar = None   # string
        self.reset = False      # boolean, otherwise known as "mode" or "reset mode"
        self.state = STATE.IDLE

    def receive_iReq(self):
        if self.iReq.poll():
            self.iReq_msg = self.iReq.recv()
            return True
        else:
            return False

    def receive_iStCar(self):
        if self.iStCar.poll():
            self.iStCar_msg = self.iStCar.recv()
            return True
        else:
            return False

    def receive_iStDoor(self):
        if self.iStDoor.poll():
            self.iStDoor_msg = self.iStDoor.recv()
            return True
        else:
            return False

    def state_processor(self):
        while True:
            if self.state is STATE.IDLE:
                if self.receive_iReq():
                    if not self.isOperating and self.reset is True:
                        self.change_state(STATE.MOVE)
                    elif not self.isOperating and self.reset is False:
                        self.change_state(STATE.STOP)

            if self.state is STATE.MOVE:
                # oCmdCar   !  msgCar
                # oCmdFloor !  msgFloor
                # out       !  msgElev
                    # Above Met: MoveTo STATE.WAIT_FOR_CAR_READY
                pass

            if self.state is STATE.WAIT_FOR_CAR_READY:
                if self.iStDoor.poll() and self.iStCar.poll():
                    self.receive_iStDoor()
                    self.receive_iStCar()
                    if self.iStDoor_msg.contents.get("content") is StatusDoor.DOOR_CAR_CLOSED and self.iStCar_msg.contents.get("content") is StatusCar.CAR_READY_TO_MOVE and self.isGoUp:
                        self.change_state(STATE.MOVE_UP)
                    elif self.iStDoor_msg.contents.get("content") is StatusDoor.DOOR_CAR_CLOSED and self.iStCar_msg.contents.get("content") is StatusCar.CAR_READY_TO_MOVE and self.isGoDown:
                        self.change_state(STATE.MOVE_DOWN)

            if self.state is STATE.MOVE_UP:
                # oCmdCar !  msgCar
                    # Above Met: MoveTo STATE.MOVING_UP
                pass

            if self.state is STATE.MOVE_DOWN:
                # oCmdCar !  msgCar
                    # Above Met: MoveTo STATE.MOVING_DOWN
                pass

            if self.state is STATE.MOVING_UP:
                if self.iStDoor.poll() and self.iStCar.poll():
                    self.iStDoor_msg = self.receive_iStDoor()
                    self.iStCar_msg = self.receive_iStCar()
                    if self.iStDoor_msg.contents.get("content") is StatusDoor.DOOR_BOTH_CLOSED and self.iStCar_msg.contents.get("content") is StatusCar.CAR_STOPPED and not self.isGoUp and not self.isGoDown:
                        self.change_state(STATE.STOP)

            if self.state is STATE.MOVING_DOWN:
                if self.iStDoor.poll() and self.iStCar.poll():
                    self.iStDoor_msg = self.receive_iStDoor()
                    self.iStCar_msg = self.receive_iStCar()
                    if self.iStDoor_msg.contents.get("content") is StatusDoor.DOOR_BOTH_CLOSED and self.iStCar_msg.contents.get("content") is StatusCar.CAR_STOPPED and not self.isGoUp and not self.isGoDown:
                        self.change_state(STATE.STOP)

            if self.state is STATE.STOP:
                # oCmdCar   !  msgDoor
                # oCmdFloor !  msgDoor
                    # Above Met: MoveTo STATE.WAIT_FOR_CAR_OPEN
                pass

            if self.state is STATE.WAIT_FOR_CAR_OPEN:
                if self.iStDoor.poll() and self.iStCar.poll():
                    self.iStDoor_msg = self.receive_iStDoor()
                    self.iStCar_msg = self.receive_iStCar()
                    if self.iStDoor_msg.contents.get("content") is StatusDoor.DOOR_BOTH_OPEN and self.iStCar_msg.content.get("content") is StatusCar.CAR_OPENING:
                        self.change_state(STATE.WAIT_FOR_CAR_CLOSE)

            if self.state is STATE.WAIT_FOR_CAR_CLOSE:
                if self.iStDoor.poll() and self.iStCar.poll():
                    self.iStDoor_msg = self.receive_iStDoor()
                    self.iStCar_msg = self.receive_iStCar()
                    if self.iStDoor_msg.contents.get("content") is StatusDoor.DOOR_BOTH_CLOSED and self.iStCar_msg.content.get("content") is StatusCar.CAR_STOPPED:
                        self.change_state(STATE.DONE)
                # iStDoor ? msgDoor
                # iStCar  ? msgDoor
                # [door == closed && Car == stopped]
                    # Above Met: MoveTo STATE.DONE
                pass

            if self.state is STATE.DONE:
                # oDone !  msgElev
                    # Above Met: MoveTo STATE.IDLE
                pass

    def main(self):
        self.state_processor()

    def run(self):
        self.main()


if __name__ == '__main__':
    ec = ElevatorController()
    ec.main()
