from ElevatorComponent import ElevatorComponent
from Messages import *


class STATE(Enum):
    """
    States used exclusively by Door Status Processor
    """
    DONE = "done"
    BUSY = "busy"


class DoorStatusProcessor(ElevatorComponent):

    def __init__(self):
        super().__init__()
        # input
        self.iStCar = None    # Received from Elevator Car
        self.iStFloor = None  # Received from Floor(s)
        self.input = None     # Received from Elevator Controller
        # output
        self.out = None  # Recipient is Elevator Controller
        # component vars
        self.doors = dict()   # Map<int, StatusDoor>
        self.curFloor = None  # int
        self.state = STATE.BUSY
        pass

    def state_processor(self):
        while True:
            if self.state == STATE.BUSY:
                # in ? en
                    # Above Met: MoveTo STATE.DONE
                # oStatus ! MsgDoor
                    # Above Met: MoveTo STATE.DONE
                pass
            elif self.state == STATE.DONE:
                # iStFloor ? doorFloor
                # iStCar ? dooCar
                # [floorDoorStatus == carDoorStatus]
                    # Above Met: MoveTo STATE.BUSY
                pass
        pass

    def main(self):
        self.state_processor()
        pass

    def run(self):
        self.main()


if __name__ == '__main__':
    dsp = DoorStatusProcessor()
    dsp.main()
