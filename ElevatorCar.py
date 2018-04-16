from ElevatorComponent import ElevatorComponent
from Messages import *

class ElevatorCar(ElevatorComponent):

    def __init__(self, CarCtrl):
        super().__init__()
        # input
        self.iCmd = None    # Received from Elevator Controller

        # output
        self.oReq = None # Recipient is Request Processor
        self.oStCar = None # Recipient is Elevator Controller
        self.oStDoor = None # Recipient is Door Status Processor

        # Instance variables to store the actual message objects that will be sent via Pipes
        self.oReqMsg = None
        self.oStCarMsg = None
        self.oStDoorMsg = None

        # Coupled Input/Output: iCmd goes to "in" on the CarCtrl so we need an instance of the CarCtrl
        self.ctrl = CarCtrl

        pass

    def state_processor(self):
        pass

    def main(self):
        while True:
            # Send output
            if(self.oReqMsg):
                # Send oReq
                self.oReq.send(self.oReqMsg)
                pass
            if(self.oStCarMsg):
                # Send oStCar
                self.oStCar.send(self.oStCarMsg)
                pass
            if(self.oStDoorMsg):
                # Send oStDoor
                self.oStDoor.send(self.oStDoorMsg)
                pass
            # Get iCmd
            try:
                job = self.iCmd.recv()
                self.ctrl.IN = job
            except EOFError:
                pass



if __name__ == '__main__':
    ctrl = None
    car = ElevatorCar(ctrl)
    car.main()