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

        
    def setoReqMsg(self, msg):
        self.oReqMsg = msg
        # Generate oReqMsg log
        self.write_log(self.get_sim_time(), self.get_real_time(),"Car Button","Elevator Car","R", self.oReqMsg.contents)

    def setoStCarMsg(self, msg):
        self.oStCarMsg = msg
        # Generate oStCarMsg log
        self.write_log(self.get_sim_time(), self.get_real_time(),"Car Ctrl","Elevator Car","R", self.oStCarMsg.contents)

    def setoStDoorMsg(self, msg):
        self.oStDoorMsg = msg
        # Generate oStDoorMsg log
        self.write_log(self.get_sim_time(), self.get_real_time(),"Car Ctrl","Elevator Car","R", self.oStDoorMsg.contents)


    def state_processor(self):
        pass

    def main(self):
        while True:
            # Send output
            if(self.oReqMsg):
                # Send oReq
                self.oReq.send(self.oReqMsg)

                # Generate oReq log
                self.write_log(self.get_sim_time(), self.get_real_time(),"Elevator Car","Request Proc","S", self.oReqMsg.contents)

                
            if(self.oStCarMsg):
                # Send oStCar
                self.oStCar.send(self.oStCarMsg)
                # Generate oStCar log
                self.write_log(self.get_sim_time(), self.get_real_time(),"Elevator Car","Elevator Ctrl","S", self.oStCarMsg.contents)
                
            if(self.oStDoorMsg):
                # Send oStDoor
                self.oStDoor.send(self.oStDoorMsg)

                # Generate oStDoor log
                self.write_log(self.get_sim_time(), self.get_real_time(),"Elevator Car","Door Status Proc","S", self.oStDoorMsg.contents)
               
            # Get iCmd
            try:
                job = self.iCmd.recv()
                # Generate oStCarMsg log
                self.write_log(self.get_sim_time(), self.get_real_time(),"Elevator Ctrl","Elevator Car","R", job.contents)

                self.ctrl.setIN(job)
            except EOFError:
                pass



if __name__ == '__main__':
    ctrl = None
    car = ElevatorCar(ctrl)
    car.main()