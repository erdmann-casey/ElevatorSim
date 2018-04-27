import time
from ElevatorComponent import ElevatorComponent
from Messages import MsgFloor, CommandFloor, MsgDoor, CommandDoor, StatusDoor, MsgReq
from enum import Enum


class STATE(Enum):
    """
    States used exclusively by Floor
    """
    OPENED = "opened"
    CLOSED = "closed"


class FloorDoor(ElevatorComponent):

    processing_time = 5.0  # double, set arbitrarily
    motion_time = 3.0      # double, set arbitrarily

    def __init__(self, floor_id, iCmd, oStatus):
        super().__init__()
        # component variables
        self.id = floor_id           # int
        self.job = None              # entity
        self.input = iCmd
        self.out = oStatus
        self.state = STATE.CLOSED

    def open_door(self):
        # print("FLOOR {} OPENING DOOR...").format(self.id)
        time.sleep(self.motion_time)
        self.state = STATE.OPENED
        msg = MsgDoor("oStatus", StatusDoor().DOOR_FLOOR_OPENED, self.id, False)
        self.write_log(self.get_sim_time(), self.get_real_time(),"Floor_" + str(self.id), "", "C", "", msg)
        self.out.send(msg)
        self.write_log(self.get_sim_time(), self.get_real_time(), "Floor_" + str(self.id), "DoorStatusProc", "S", "oStatus", msg)

    def close_door(self):
        # print("FLOOR {} CLOSING DOOR...").format(self.id)
        time.sleep(self.motion_time)
        self.state = STATE.CLOSED
        msg = MsgDoor("oStatus", StatusDoor().DOOR_FLOOR_CLOSED, self.id, False)
        self.write_log(self.get_sim_time(), self.get_real_time(),"Floor_" + str(self.id), "", "C", "", msg)
        self.out.send(msg)
        self.write_log(self.get_sim_time(), self.get_real_time(), "Floor_" + str(self.id), "DoorStatusProc", "S", "oStatus", msg)

    def receive_in(self):
        if self.input.poll():
            msg = self.input.recv()
            self.write_log(self.get_sim_time(), self.get_real_time(), "ElevCtrl", "Floor_" + str(self.id), "R", "iCmd", msg)
            self.job = msg.contents.get("value")
            return True
        else:
            return False

    def state_processor(self):
        while True:
            if self.receive_in():
                # print("FLOOR {} JOB is {}".format(self.id, self.job))

                if self.job == CommandDoor.DOOR_FLOOR_X_OPEN:
                    # print("FLOOR_{} opening door...".format(self.id))
                    self.job = None
                    self.open_door()
                    """
                    if self.state == STATE.OPENED:
                        continue
                    else:
                        self.open_door()
                    """

                elif self.job == CommandDoor.DOOR_FLOOR_X_CLOSE:
                    # print("FLOOR_{} closing door...".format(self.id))
                    self.job = None
                    self.close_door()
                    """
                    if self.state == STATE.CLOSED:
                        continue
                    else:
                        self.close_door()
                    """
            elif self.state == STATE.OPENED:
                time.sleep(self.processing_time)
                self.close_door()
                continue

    def main(self):
        self.state_processor()


class Floor(ElevatorComponent):

    def __init__(self, floor_id, in_cmd, out_req, out_status):
        super().__init__()
        # input
        self.iCmd = in_cmd
        # outputs
        self.oReq = out_req
        self.oStatus = out_status
        # msg
        self.iCmd_msg = None
        # component vars
        self.door = FloorDoor(floor_id, self.iCmd, self.oStatus)

    def state_processor(self):
        while True:
            continue

    def main(self):
        self.state_processor()

    def send_request(self):
        # msg = MsgFloor(CommandFloor.FLOOR_REQ, self.door.id)
        msg = MsgReq("oReq", self.door.id)
        self.oReq.send(msg)
        self.write_log(self.get_sim_time(), self.get_real_time(), "Floor_" + str(self.door.id), "RequestProc", "S", "oReq", msg)


if __name__ == '__main__':
    f = Floor(0)
    f.main()

