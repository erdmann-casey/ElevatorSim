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
    
        

    def state_processor(self):
        while True:
            if self.state == STATE.PASSIVE:
                # in ? job && job != null 
                    # Above Met: MoveTo STATE.BUSY
                self.IN = self.ctrl.oMotor
                # Generate IN log
                if(self.IN):
                    self.write_log(self.get_sim_time(), self.get_real_time(),"Elevator Ctrl","Motor","R",self.IN.contents)

                    if(self.IN.contents['content'] == StatusMotor.MOTOR_MOVING):
                        self.state = STATE.BUSY
                        # Generate Status log
                        self.write_log(self.get_sim_time(), self.get_real_time(),"Motor","","C",self.IN.contents)

                
            elif self.state == STATE.BUSY:
                # Send message MsgMotor -> OUT
                self.OUT = MsgMotor(StatusMotor.MOTOR_MOVING)

                self.ctrl.setiMotor(self.OUT)

                # Generate OUT log
                self.write_log(self.get_sim_time(), self.get_real_time(),"Motor","Elevator Ctrl","S",self.OUT.contents)

                # MoveTo STATE.PASSIVE
                self.state = STATE.PASSIVE
                
            

        

    def main(self):
        self.state_processor()
        
    
if __name__ == '__main__':
    ctrl = None
    motor = Motor(ctrl)
    motor.main()