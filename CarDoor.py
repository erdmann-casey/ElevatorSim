from ElevatorComponent import ElevatorComponent
from Messages import *

class STATE(Enum):
    """
    States used exclusively by Car Door
    """
    OPENED = "opened"
    OPENING = "opening"
    CLOSED = "closed"
    CLOSING = "closing"


class CarDoor(ElevatorComponent):
    
    def __init__(self, CarCtrl, ElevatorCar):
        super().__init__()
        # input
        self.IN = None    # Received from Car Controller

        # output
        self.OUT = None # Recipient is Car Controller and Elevator Car

        # Coupled Input/Output: Sends and receives from Car Controller and sends to Elevator Car, so an instance of the both is needed
        self.ctrl = CarCtrl
        self.car = ElevatorCar

        # component vars
        self.state = STATE.CLOSED # initialize in CLOSED state
    

        pass

    def state_processor(self):
        while True:
            if self.state == STATE.CLOSED:
                # in ? job && cmdDoor == OPEN
                    # Above Met: MoveTo STATE.OPENING
                # in ? job && cmdDoor == CLOSE
                    # Above Met: MoveTo STATE.CLOSING
                pass
            elif self.state == STATE.OPENING:
                # Send message MsgDoor -> OUT
                # MoveTo STATE.OPENED
                pass
            elif self.state == STATE.OPENED:
                # Do some timeout logic, MoveTo STATE.CLOSING
                pass
            elif self.state == STATE.CLOSING:
                # Send message MsgDoor -> OUT
                # MoveTo STATE.CLOSED
                pass
                

        pass

    def main(self):
        self.state_processor()
        pass
    
if __name__ == '__main__':
    ctrl = None
    car = None
    door = CarDoor(ctrl, car)
    door.main()