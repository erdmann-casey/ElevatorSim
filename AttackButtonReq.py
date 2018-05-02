from ElevatorComponent import ElevatorComponent
from Messages import *

class AttackButtonReq(ElevatorComponent):
    
    def __init__(self):
        super().__init__()
        # input
        self.IN = None    # Received from Car Controller

        # output
        self.oReq = None # Recipient is Car Controller and Elevator Car

    def send_oReq(self, msg):
        self.oReq.send(msg)
        self.write_log(self.get_sim_time(), self.get_real_time(),"Attacker","Request Proc","S","oReq",msg)


    def state_processor(self):
         while True:
            # Get iCmd
            try:
                job = self.IN.recv()
                # Generate oStCarMsg log
                self.write_log(self.get_sim_time(), self.get_real_time(),"Elevator Car","Attacker","R","oReq",job)
                
                self.send_oReq(MsgReq('oReq', 4))

            except EOFError:
                pass
        

    def main(self):
        self.state_processor()
        pass
        
    
if __name__ == '__main__':
    attack = AttackButtonReq()
    attack.main()