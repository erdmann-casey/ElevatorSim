from ElevatorComponent import ElevatorComponent
from Messages import *


class CarBtn(ElevatorComponent):
    
    def __init__(self, ElevatorCar):
        super().__init__()

        # output
        self.OUT = None # Recipient is Car Controller

        # Coupled Input/Output: Sends and receives from Car Controller so an instance of the controller is needed
        self.car = ElevatorCar

        pass

    def press(self, id):
        # Send Message MsgReq -> OUT
        msg = MsgReq(id)

        self.car.oReqMsg = msg

        pass
    
    def state_processor(self):
        pass
        
    def main(self):
        pass
    
if __name__ == '__main__':
    car = None
    button = CarBtn(car)
    button.main()