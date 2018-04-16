from ElevatorComponent import ElevatorComponent
from Messages import *

class STATE(Enum):
    """
    States used exclusively by Car Controller
    """
    IDLE = "idle"
    OPENING_DOOR = "openingDoor"
    CONFIRM_OPEN = "confirmOpen"
    CLOSING = "closing"
    PREP_TO_CLOSE = "prepToClose"
    CONFIRM_CLOSE = "confirmClose"
    PREP_TO_MOVE = "prepToMove"
    WAIT_TO_MOVE = "waitToMove"
    MOVE_BCK = "moveBCK"
    MOVE_FWD = "moveFWD"
    MOVING = "moving"
    REACHED = "reached"
    WAIT_TO_OPEN = "waitToOpen"





class CarCtrl(ElevatorComponent):
    
    def __init__(self, CarDoor, Motor, ElevatorCar):
        super().__init__()
        # input
        self.iDoor = None    # Received from Car Door
        self.iMotor = None    # Received from Motor
        self.IN = None    # Received from Elevator Car

        # output
        self.oDoor = None # Recipient is Car Door
        self.oMotor = None # Recipient is Motor
        self.oSt = None # Recipient is Elevator Car

        # Coupled Input: iCmd goes to "in" on the CarCtrl so we need an instance of the CarCtrl
        self.door = CarDoor
        self.motor = Motor
        self.car = ElevatorCar

        # component vars
        self.state = STATE.IDLE # initialize in IDLE state

        pass

    def state_processor(self):
        while True:
            if self.state == STATE.IDLE:
                # in ? msgDoor && cmdDoor == OPEN 
                    # Above Met: MoveTo STATE.OPENING_DOOR
                # in ? en && cmdCar == MOVE
                    # Above Met: MoveTo STATE.PREP_TO_CLOSE
                pass
            elif self.state == STATE.OPENING_DOOR:
                # Send message MsgDoor -> oDoor
                # Send message MsgCar -> oSt
                # MoveTo STATE.CONFIRM_OPEN
                pass
            elif self.state == STATE.CONFIRM_OPEN:
                # iDoor ? msg && statusDoor == OPENED
                    # Above Met: MoveTo STATE.CLOSING
                pass
            elif self.state == STATE.CLOSING:
                # MoveTo STATE.PREP_TO_CLOSE
                self.state == STATE.PREP_TO_CLOSE
            elif self.state == STATE.PREP_TO_CLOSE:
                # Send message MsgDoor -> oDoor
                # Send message MsgCar -> oSt
                # MoveTo STATE.CONFIRM_CLOSE
                pass
            elif self.state == STATE.CONFIRM_CLOSE:
                # iDoor ? msg && statusDoor == CLOSE && inProcess
                    # Above Met: MoveTo STATE.PREP_TO_MOVE
                pass
            elif self.state == STATE.PREP_TO_MOVE:
                 # Send message MsgCar -> oSt
                 # MoveTo STATE.WAIT_TO_MOVE
                 pass
            elif self.state == STATE.WAIT_TO_MOVE:
                # in ? msg && cmdCar == Up
                    # Above Met: MoveTo STATE.MOVE_FWD
                # in ? msg && cmdCar == Down
                    # Above Met: MoveTo STATE.MOVE_BCK
                pass
            elif self.state == STATE.MOVE_FWD:
                # MsgMotor -> oMotor
                # MsgCar -> oSt
                # MoveTo STATE.MOVING
                pass
            elif self.state == STATE.MOVE_BCK:
                # MsgMotor -> oMotor
                # MsgCar -> oSt
                # MoveTo STATE.MOVING
                pass
            elif self.state == STATE.MOVING:
                # in ? MsgCar && cmdCar == DOWN && statusDoor == CLOSED && operating == true && motor_running == false
                    # Above Met: MoveTo STATE.WAIT_TO_MOVE
                # in ? MsgCar && cmdCar == UP && statusDoor == CLOSED && operating == true && motor_running == false
                    # Above Met: MoveTo STATE.WAIT_TO_MOVE
                # iMotor ? MsgMotor pos==dest
                    # Above Met: MoveTo STATE.REACHED
                pass
            elif self.state == STATE.REACHED:
                # MsgCar -> oSt
                # MoveTo STATE.WAIT_TO_OPEN
                pass
            elif self.state == STATE.WAIT_TO_OPEN:
                # in ? msg && cmdDoor == OPEN
                    # Above Met: MoveTo STATE.OPENING_DOOR
                pass

        pass

    def main(self):
        self.state_processor()
        pass
    
if __name__ == '__main__':
    door = None
    motor = None
    car = None
    ctrl = CarCtrl(door, motor, car)
    ctrl.main()