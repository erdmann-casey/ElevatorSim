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
                if(self.IN.contents['content'] == StatusMotor.MOTOR_MOVING):
                    self.state = STATE.BUSY
                    # Generate oReq log
                    sim_time = str(time() - self.system_time)
                    motor_run_time = str(time() - self.motor_time)
                    
                    log = sim_time + "," + motor_run_time + ",Motor,C" + str(self.IN.contents)

                    print(log)
                pass
            elif self.state == STATE.BUSY:
                # Send message MsgMotor -> OUT
                self.OUT = MsgMotor(StatusMotor.MOTOR_MOVING)

                self.ctrl.setiMotor(self.OUT)

                # Generate oReq log
                sim_time = str(time() - self.system_time)
                motor_run_time = str(time() - self.motor_time)
                    
                log = sim_time + "," + motor_run_time + ",Motor, Elevator Ctrl,S" + str(self.OUT.contents)

                print(log)
                # MoveTo STATE.PASSIVE
                self.state = STATE.PASSIVE
                pass
            

        pass

    def main(self):
        self.state_processor()
        pass
    
if __name__ == '__main__':
    ctrl = None
    motor = Motor(ctrl)
    motor.main()