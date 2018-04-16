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

        # Coupled Input/Output: iCmd goes to "in" on the CarCtrl so we need an instance of the CarCtrl
        self.ctrl = CarCtrl

        pass

    def state_processor(self):
        pass

    def main(self):
        while True:
            # Send output
            if(self.oReq):
                # Send oReq
                pass
            if(self.oStCar):
                # Send oStCar
                pass
            if(self.oStDoor):
                # Send oStDoor
                pass
            # Get iCmd
            try:
                job = self.iCmd.recv()
                self.ctrl.IN = job
            except EOFError:
                pass



if __name__ == '__main__':
    ctrl = None
    ec = ElevatorCar(ctrl)
    ec.main()