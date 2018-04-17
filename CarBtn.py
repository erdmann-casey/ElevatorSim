from ElevatorComponent import ElevatorComponent
from Messages import *
from time import time

class CarBtn(ElevatorComponent):
    
    def __init__(self, ElevatorCar, system_time):
        super().__init__()

        # output
        self.OUT = None # Recipient is Car Controller

        # Coupled Input/Output: Sends and receives from Car Controller so an instance of the controller is needed
        self.car = ElevatorCar

        self.system_time = system_time

        self.button_time = time()
        
        pass

    def press(self, id):
        # Send Message MsgReq -> OUT
        self.OUT = MsgReq(id)
    
        self.car.oReqMsg = self.OUT

        # Generate button pressed log
        sim_time = str(time() - self.system_time)
        btn_run_time = str(time() - self.button_time)
        
        log = sim_time + "," + btn_run_time + ",Car Btn,Elevator Car,S," + str(self.OUT.contents)

        print(log)


        pass
    
    def state_processor(self):
        pass
        
    def main(self):
        pass
    
if __name__ == '__main__':
    car = None
    button = CarBtn(car, time())
    button.main()