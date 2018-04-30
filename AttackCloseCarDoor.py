from ElevatorComponent import ElevatorComponent
from Messages import *
from threading import Thread

class AttackCloseCarDoor(ElevatorComponent):
    
    def __init__(self, CarDoor):
        super().__init__()
        # input
        self.IN = None    # Received from Car Controller

        # output
        self.OUT = None # Recipient is Car Controller and Elevator Car

        # Coupled Input/Output: Sends and receives from Car Controller and sends to Elevator Car, so an instance of the both is needed
        self.door = CarDoor

    def setIN(self, IN):
        self.IN = IN
        if(self.IN):
            if(self.IN.contents["value"] == CommandDoor.DOOR_CAR_OPEN):
                # Generate IN Log 
                self.write_log(self.get_sim_time(), self.get_real_time(),"Car Ctrl","Attacker","R","in",self.IN)
                # Hack 'em
                self.oDoor = MsgDoor("oDoor", CommandDoor.DOOR_CAR_CLOSE, self.IN.contents["id"], False)
                self.door.setIN(self.oDoor)
                self.write_log(self.get_sim_time(), self.get_real_time(),"Attacker","Car Door","S","in",self.oDoor)

            elif(self.IN.contents["value"] == CommandDoor.DOOR_CAR_CLOSE):
                self.write_log(self.get_sim_time(), self.get_real_time(),"Car Ctrl","Attacker","R","in",self.IN)
                self.door.setIN(self.oDoor)
                self.write_log(self.get_sim_time(), self.get_real_time(),"Attacker","Car Door","S","in",self.IN)
                

    def state_processor(self):
        thread_CarDoor = Thread(target = self.door.state_processor, args = ())
        thread_CarDoor.start()
        pass

    def main(self):
        self.state_processor()
        pass
        
    
if __name__ == '__main__':
    door = None
    attack = AttackCloseCarDoor(door)
    attack.main()