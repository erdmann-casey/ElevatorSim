from ElevatorComponent import ElevatorComponent
from Messages import *
from time import time

class ElevatorCar(ElevatorComponent):

    def __init__(self, CarCtrl, system_time):
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

        self.system_time = system_time

        self.elev_car_time = time()

        

    def state_processor(self):
        pass

    def main(self):
        while True:
            # Send output
            if(self.oReqMsg):
                # Send oReq
                self.oReq.send(self.oReqMsg)

                # Generate oReq log
                sim_time = str(time() - self.system_time)
                oReq_run_time = str(time() - self.elev_car_time)
                
                log = sim_time + "," + oReq_run_time + ",Elevator Car,Request Proc,S," + str(self.oReqMsg.contents)

                print(log)

                
            if(self.oStCarMsg):
                # Generate oStCarMsg log
                sim_time = str(time() - self.system_time)
                oStCar_run_time = str(time() - self.elev_car_time)
                
                log = sim_time + "," + oStCar_run_time + ",Car Ctrl,Elevator Car,R," + str(self.oReqMsg.contents)

                print(log)
                # Send oStCar
                self.oStCar.send(self.oStCarMsg)
                # Generate oStCar log
                sim_time = str(time() - self.system_time)
                oStCar_run_time = str(time() - self.elev_car_time)
                
                log = sim_time + "," + oStCar_run_time + ",Elevator Car,Elevator Controller,S," + str(self.oReqMsg.contents)

                print(log)
                
            if(self.oStDoorMsg):
                # Generate oStDoorMsg log
                sim_time = str(time() - self.system_time)
                oStDoor_run_time = str(time() - self.elev_car_time)
                
                log = sim_time + "," + oStDoor_run_time + ",Car Ctrl,Elevator Car,R," + str(self.oStDoorMsg.contents)

                print(log)
                # Send oStDoor
                self.oStDoor.send(self.oStDoorMsg)
                # Generate oStDoor log
                sim_time = str(time() - self.system_time)
                oStDoor_run_time = str(time() - self.elev_car_time)
                
                log = sim_time + "," + oStDoor_run_time + ",Elevator Car,Door Status Proc,S," + str(self.oStDoorMsg.contents)

                print(log)
                
            # Get iCmd
            try:
                job = self.iCmd.recv()
                # Generate oStCarMsg log
                sim_time = str(time() - self.system_time)
                iCmd_run_time = str(time() - self.elev_car_time)
                
                log = sim_time + "," + iCmd_run_time + ",Elevator Controller,Elevator Car,R," + str(job.contents)

                print(log)
                self.ctrl.setIN(job)
            except EOFError:
                pass



if __name__ == '__main__':
    ctrl = None
    car = ElevatorCar(ctrl, time())
    car.main()