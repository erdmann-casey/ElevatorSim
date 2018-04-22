from ElevatorComponent import ElevatorComponent
from Messages import *


class CarBtn(ElevatorComponent):
    
    def __init__(self, ElevatorCar):
        super().__init__()

        # output
        self.OUT = None # Recipient is Car Controller

        # Coupled Input/Output: Sends and receives from Car Controller so an instance of the controller is needed
        self.car = ElevatorCar
        

    def press(self, id):
        # Send Message MsgReq -> OUT
        self.OUT = MsgReq(id)
    
        self.car.oReqMsg = self.OUT

        # Generate button pressed log
        self.write_log(self.get_sim_time(), self.get_real_time(),"Car Btn","Elevator Car","S",self.OUT.contents)
    
    def state_processor(self):
        pass
        
    def main(self):
        pass
    
if __name__ == '__main__':
    car = None
    button = CarBtn(car)
    button.main()