from multiprocessing import Process
from abc import abstractmethod
from enum import Enum
from time import time
from Messages import *


class STATE(Enum):
    NONE = "No State"


class ElevatorComponent(Process):

    def __init__(self):
        super().__init__()
        self.state = STATE.NONE
        self.state_comm = None
        self.start_time = time()
        pass

    def run(self):
        self.main()

    def change_state(self, next_state):
        self.state = next_state

    def state_communication(self):
        while True:
            bSendState = self.state_comm.recv()
            if bSendState is True:
                self.state_comm.send(self.state)

    def write_log(self, sim_time, real_time, sender, receiver, action, port, msg):

        log_str = "{}, {}, {}, {}, {}, ".format(sim_time, real_time, sender, receiver, action)

        if type(msg) is MsgCar:
            if action == "C":
                log_str += '{"statusCar":"'+msg.contents.get("value")+'"}'
            else:
                log_str += '{"port":"' + port + '", "value":"'+msg.contents.get("value")+'[pos:'+str(msg.contents.get("pos"))+'][dest:'+str(msg.contents.get("dest"))+']"}'

        elif type(msg) is MsgDoor:
            if action == "C":
                log_str += '{"statusDoor":"'+msg.contents.get("value")+'"}'
                log_str = log_str.replace("X", str(msg.contents.get("id")))
            else:
                log_str += '{"port":"'+port+'", "value": "'+msg.contents.get("value")+'"}'

        elif type(msg) is MsgElev:
            if action == "C":
                log_str += '{"statusElev":"'+msg.contents.get("value")+'"}'
            else:
                log_str += '{"port":"'+port+'", "value":"[ELEV:'+str(msg.contents.get("value").get("ELEV"))+']"}'

        elif type(msg) is MsgFloor:
            if action == "C":
                log_str += '{"statusFloor":"'+msg.contents.get("value")+'"}'
                log_str = log_str.replace("X", str(msg.contents.get("id")))
            else:
                log_str += '{"port":"' + port + '", "value": "' + msg.contents.get("value") + '"}'

        elif type(msg) is MsgMotor:
            if action == "C":
                log_str += '{"statusMotor":"'+msg.contents.get("value")+'"}'
            else:
                log_str += '{"port":"' + port + '", "value": "' + msg.contents.get("value") + '"}'

        elif type(msg) is MsgReq:
            if action == "C":
                log_str += '{"statusReq":"'+msg.contents.get("value")+'"}'
            else:
                log_str += '{"port":"'+port+'", "value":"[REQ:'+str(msg.contents.get("value").get("REQ"))+']"}'

        log_str += "\n"
        """
        for key in msg_contents:
            if type(msg_contents.get(key)) is dict:
                log_str += "\"{}\": \"[{}:{}]\"".format("value", msg_contents.get(key).keys(), msg_contents.get(key).values())
            log_str += ""
        log_str += "{}\n".format(msg_contents)
        """
        file = open("logs.txt", "a+")
        file.write(log_str)
        file.close()

    def get_sim_time(self):
        return time() - self.start_time

    def get_real_time(self):
        return time()

    @abstractmethod
    def state_processor(self): raise NotImplementedError

    @abstractmethod
    def main(self): raise NotImplementedError
