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
        self.floorDoorStatus = None
        self.carDoorStatus = None

    def state_processor(self):
        while True:
            if self.state == STATE.BUSY:
                # in ? en (What is "in ? en"?)
                    # Above Met: MoveTo STATE.BUSY
                # oStatus ! MsgDoor (Under what criteria do we send this message? Every iteration?)
                    # Above Met: MoveTo STATE.DONE
                pass
            elif self.state == STATE.DONE:
                self.receive_iStCar()
                self.receive_iStFloor()
                if self.floorDoorStatus is not None and self.floorDoorStatus is self.carDoorStatus:
                    self.change_state(STATE.BUSY)
        pass

    def receive_iStCar(self):
        if self.iStCar.poll():
            car_door_msg = self.iStCar.recv()
            self.doors[0] = car_door_msg.contents.get("content")  # Index 0 reserved for Car Door
            return True
        else:
            return False

    def receive_iStFloor(self):
        if self.iStFloor.poll():
            floor_door_msg = self.iStFloor.recv()
            self.doors[floor_door_msg.contents.get("id")] = floor_door_msg.contents.get("content")
            return True
        else:
            return False

    def receive_input(self):
        if self.input.poll():
            return True
        else:
            return False

    def main(self):
        self.state_processor()
        pass


if __name__ == '__main__':
    dsp = DoorStatusProcessor()
    dsp.main()
