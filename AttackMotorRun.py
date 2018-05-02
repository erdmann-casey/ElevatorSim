from ElevatorComponent import ElevatorComponent
from Messages import *

class AttackMotorRun(ElevatorComponent):
    
    def __init__(self):
        super().__init__()
        # input
        self.iCmd = None    # Received from Car Controller

        # output
        self.oCmdCar = None # Recipient is Car Controller and Elevator Car

    def send_oCmdCar(self, msg):
        self.oCmdCar.send(msg)
        self.write_log(self.get_sim_time(), self.get_real_time(), "Attacker", "ElevCar", "S", "oCmdCar", msg)


    def state_processor(self):
         while True:
            # Get iCmd
            try:
                job = self.iCmd.recv()
                # Generate oStCarMsg log
                self.write_log(self.get_sim_time(), self.get_real_time(),"Elevator Ctrl","Attacker","R","iCmd",job)
                if(isinstance(job, MsgCar) and job.contents['isCommand']):
                    if(job.contents['value'] != CommandCar.CAR_STOP):
                        self.send_oCmdCar(MsgCar("oCmdCar", job.contents['value'], job.contents['pos'], 100, True))
                else:
                    self.send_oCmdCar(job)
            except EOFError:
                pass
        

    def main(self):
        self.state_processor()
        pass
        
    
if __name__ == '__main__':
    attack = AttackMotorRun()
    attack.main()