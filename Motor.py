from ElevatorComponent import ElevatorComponent
from Messages import *

class STATE(Enum):
    """
    States used exclusively by Motor
    """
    PASSIVE = "passive"
    BUSY = "busy"


class Motor(ElevatorComponent):
    
    def __init__(self, CarCtrl):
        super().__init__()
        # input
        self.IN = None    # Received from Car Controller

        # output
        self.OUT = None # Recipient is Car Controller

        # Coupled Input/Output: Sends and receives from Car Controller so an instance of the controller is needed
        self.ctrl = CarCtrl

        # component vars
        self.state = STATE.PASSIVE # initialize in PASSIVE state
    

        pass

    def state_processor(self):
        while True:
            if self.state == STATE.PASSIVE:
                # in ? job && job != null 
                    # Above Met: MoveTo STATE.BUSY
                pass
            elif self.state == STATE.BUSY:
                # Send message MsgMotor -> OUT
                # MoveTo STATE.PASSIVE
                pass
            

        pass

    def main(self):
        self.state_processor()
        pass
    
if __name__ == '__main__':
    ctrl = None
    motor = Motor(ctrl)
    motor.main()