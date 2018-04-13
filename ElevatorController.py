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
        self.operating = None   # boolean
        self.statusDoor = None  # string
        self.statusCar = None   # string
        self.state = STATE.IDLE

    def state_processor(self):
        while True:
            if self.state is STATE.IDLE:
                # iReq ? cmdReq
                # [!isOperating && mode == true]
                    # Above Met: MoveTo STATE.MOVE
                # iReq ? cmdReq
                # [!isOperating && mode == false]
                    # Above Met: MoveTo STATE.STOP
                pass
            if self.state is STATE.MOVE:
                # oCmdCar   !  msgCar
                # oCmdFloor !  msgFloor
                # out       !  msgElev
                    # Above Met: MoveTo STATE.WAIT_FOR_CAR_READY
                pass
            if self.state is STATE.WAIT_FOR_CAR_READY:
                # iStDoor ?  msgDoor
                # iStCar  ?  msgCar
                # [door == closed && Car == readyToMove && isGoUp]
                    # Above Met: MoveTo STATE.MOVE_UP
                # iStDoor ?  msgDoor
                # iStCar  ?  msgCar
                # [door == closed && Car == readyToMove && isGoDown]
                    # Above Met: MoveTo STATE.MOVE_DOWN
                pass
            if self.state is STATE.MOVE_UP:
                # oCmdCar !  msgCar
                    # Above Met: MoveTo STATE.MOVING_UP
                pass
            if self.state is STATE.MOVE_DOWN:
                # oCmdCar !  msgCar
                    # Above Met: MoveTo STATE.MOVING_DOWN
                pass
            if self.state is STATE.MOVING_UP:
                # iStDoor ?  msgDoor
                # iStCar  ?  msgCar
                # [door == closed && Car == stopped && !isGoUp && !isGoDown]
                    # Above Met: MoveTo STATE.STOP
                pass
            if self.state is STATE.MOVING_DOWN:
                # iStDoor ?  msgDoor
                # iStCar  ?  msgCar
                # [door == closed && Car == stopped && !isGoUp && !isGoDown]
                    # Above Met: MoveTo STATE.STOP
                pass
            if self.state is STATE.STOP:
                # oCmdCar   !  msgDoor
                # oCmdFloor !  msgDoor
                    # Above Met: MoveTo STATE.WAIT_FOR_CAR_OPEN
                pass
            if self.state is STATE.WAIT_FOR_CAR_OPEN:
                # iStDoor ? msgDoor
                # iStCar  ? msgDoor
                # [door == opened && Car == opening]
                    # Above Met: MoveTo STATE.WAIT_FOR_CAR_CLOSE
                pass
            if self.state is STATE.WAIT_FOR_CAR_CLOSE:
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
