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

        # Coupled Input/Output: Multiple outs to an instance of the CarDoor, the Motor, and the Elevator Car itself
        self.door = CarDoor
        self.motor = Motor
        self.car = ElevatorCar

        # component vars
        self.state = STATE.IDLE # initialize in IDLE state


        self.curFloor = 0
        self.destFloor = 0

        self.doorStatus = StatusDoor.DOOR_CAR_CLOSED

        self.operating = False

        self.motorStatus = StatusMotor.MOTOR_REACHED



        pass

    def setiMotor(self, iMotor):
        self.iMotor = iMotor
        sim_time = str(time() - self.system_time)
        ctrl_run_time = str(time() - self.ctrl_time)
                    
        log = sim_time + "," + ctrl_run_time + ",Motor, Elevator Ctrl,R" + str(self.iMotor.contents)

        print(log)

    def state_processor(self):
        while True:

            if(isinstance(self.IN, MsgCar)):
                self.curFloor = self.IN.contents['pos']
                self.destFloor = self.IN.contents['dest']
            
            if(self.iDoor):
                self.doorStatus = self.iDoor.contents['content']
            
            if(self.iMotor):
                self.motorStatus = self.iMotor.contents['content']


            if self.state == STATE.IDLE:
                # in ? msgDoor && cmdDoor == OPEN 
                    # Above Met: MoveTo STATE.OPENING_DOOR
                if(self.IN.contents['isCommand'] and self.IN.contents['content'] == CommandDoor.DOOR_CAR_OPEN):
                    self.state = STATE.OPENING_DOOR
                
                # in ? en && cmdCar == MOVE
                    # Above Met: MoveTo STATE.PREP_TO_CLOSE
                elif(self.IN.contents['isCommand'] and self.IN.contents['content'] == CommandCar.CAR_MOVE):
                    self.state = STATE.PREP_TO_CLOSE

                # Elevator Car is idle, set operating to False
                self.operating = False

                pass
            
            elif self.state == STATE.OPENING_DOOR:
                # Send message MsgDoor -> oDoor
                self.oDoor = MsgDoor(StatusDoor.DOOR_CAR_OPENED, self.curFloor, False)
                # Send message MsgCar -> oSt
                self.oSt = MsgCar(StatusCar.CAR_OPENING, self.curFloor, self.destFloor, False)
                # MoveTo STATE.CONFIRM_OPEN
                self.state = STATE.CONFIRM_OPEN
                # Elevator Car is no longer in IDLE, set operating to True
                self.operating = True
                pass
            elif self.state == STATE.CONFIRM_OPEN:
                # iDoor ? msg && statusDoor == OPENED
                    # Above Met: MoveTo STATE.CLOSING
                if(self.iDoor.contents['content'] == StatusDoor.DOOR_CAR_OPENED):
                    self.state = STATE.CLOSING
                pass
            elif self.state == STATE.CLOSING:
                # MoveTo STATE.PREP_TO_CLOSE
                self.state == STATE.PREP_TO_CLOSE
            elif self.state == STATE.PREP_TO_CLOSE:
                # Send message MsgDoor -> oDoor
                self.oDoor = MsgDoor(StatusDoor.DOOR_CAR_CLOSED, self.curFloor, False)
                # Send message MsgCar -> oSt
                self.oSt = MsgCar(StatusCar.CAR_STOPPED, self.curFloor, self.destFloor, False)
                # MoveTo STATE.CONFIRM_CLOSE
                self.state = STATE.CONFIRM_CLOSE
                # Elevator Car is no longer in IDLE, set operating to True
                self.operating = True
                pass
            elif self.state == STATE.CONFIRM_CLOSE:
                # iDoor ? msg && statusDoor == CLOSE && inProcess
                    # Above Met: MoveTo STATE.PREP_TO_MOVE
                if(self.iDoor.contents['content'] == StatusDoor.DOOR_CAR_CLOSED):
                    self.state = STATE.PREP_TO_MOVE

                pass
            elif self.state == STATE.PREP_TO_MOVE:
                 # Send message MsgCar -> oSt
                 self.oSt = MsgCar(StatusCar.CAR_READY_TO_MOVE, self.curFloor, self.destFloor, False)
                 # MoveTo STATE.WAIT_TO_MOVE
                 self.state = STATE.WAIT_TO_MOVE
                 pass
            elif self.state == STATE.WAIT_TO_MOVE:
                # in ? msg && cmdCar == Up
                    # Above Met: MoveTo STATE.MOVE_FWD
                if(self.IN.contents['content'] == CommandCar.CAR_UP):
                    self.state = STATE.MOVE_FWD
                # in ? msg && cmdCar == Down
                    # Above Met: MoveTo STATE.MOVE_BCK
                elif(self.IN.contents['content'] == CommandCar.CAR_DOWN):
                    self.state = STATE.MOVE_BCK               
                pass
            elif self.state == STATE.MOVE_FWD:
                # MsgMotor -> oMotor
                self.oMotor = MsgMotor(CommandMotor.MOTOR_FORWARD)
                sim_time = str(time() - self.system_time)
                ctrl_run_time = str(time() - self.ctrl_time)
                    
                log = sim_time + "," + ctrl_run_time + ",Elevator Ctrl, Motor,S" + str(self.oMotor.contents)

                print(log)
                # MsgCar -> oSt
                self.oSt = MsgCar(StatusCar.CAR_MOVING, self.curFloor, self.destFloor, False)
                # MoveTo STATE.MOVING
                self.state = STATE.MOVING
                pass
            elif self.state == STATE.MOVE_BCK:
                # MsgMotor -> oMotor
                self.oMotor = MsgMotor(CommandMotor.MOTOR_BACKWARD)
                sim_time = str(time() - self.system_time)
                ctrl_run_time = str(time() - self.ctrl_time)
                    
                log = sim_time + "," + ctrl_run_time + ",Elevator Ctrl, Motor,S" + str(self.oMotor.contents)

                print(log)               
                # MsgCar -> oSt
                self.oSt = MsgCar(StatusCar.CAR_MOVING, self.curFloor, self.destFloor, False)
                # MoveTo STATE.MOVING
                self.state = STATE.MOVING
                pass
            elif self.state == STATE.MOVING:
                # in ? MsgCar && cmdCar == DOWN && statusDoor == CLOSED && operating == true && motor_running == false
                    # Above Met: MoveTo STATE.WAIT_TO_MOVE
                if(self.IN.contents['content'] == CommandCar.CAR_DOWN and self.doorStatus == StatusDoor.DOOR_CAR_CLOSED and self.operating and self.motorStatus == StatusMotor.MOTOR_REACHED):
                    self.state = STATE.WAIT_TO_MOVE
                # in ? MsgCar && cmdCar == UP && statusDoor == CLOSED && operating == true && motor_running == false
                    # Above Met: MoveTo STATE.WAIT_TO_MOVE
                elif(self.IN.contents['content'] == CommandCar.CAR_UP and self.doorStatus == StatusDoor.DOOR_CAR_CLOSED and self.operating and self.motorStatus == StatusMotor.MOTOR_REACHED):
                    self.state = STATE.WAIT_TO_MOVE
                # iMotor ? MsgMotor pos==dest
                    # Above Met: MoveTo STATE.REACHED
                elif(self.iMotor and self.curFloor == self.destFloor):
                    self.state = STATE.REACHED
                pass
            elif self.state == STATE.REACHED:
                # MsgCar -> oSt
                self.oSt = MsgCar(StatusCar.CAR_STOPPED, self.curFloor, self.destFloor, False)
                # MoveTo STATE.WAIT_TO_OPEN
                self.state = STATE.WAIT_TO_OPEN
                pass
            elif self.state == STATE.WAIT_TO_OPEN:
                # in ? msg && cmdDoor == OPEN
                    # Above Met: MoveTo STATE.OPENING_DOOR
                if(self.IN.contents['content'] == CommandDoor.DOOR_CAR_OPEN):
                    self.state = STATE.OPENING_DOOR
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