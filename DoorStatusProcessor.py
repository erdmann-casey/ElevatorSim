from ElevatorComponent import ElevatorComponent
from Messages import *


class STATE(Enum):
    """
    States used exclusively by Door Status Processor
    """
    DONE = "done"
    BUSY = "busy"


class DoorStatusProcessor(ElevatorComponent):

    def __init__(self):
        super().__init__()
        # input
        self.iStCar = None    # Received from Elevator Car
        self.iStFloor1 = None  # Received from Floor(s)
        self.iStFloor2 = None  # Received from Floor(s)
        self.iStFloor3 = None  # Received from Floor(s)
        self.iStFloor4 = None  # Received from Floor(s)
        self.iStFloor5 = None  # Received from Floor(s)
        self.input = None     # Received from Elevator Controller
        # msg
        self.iStCar_msg = None
        self.iStFloor_msg = {}
        self.input_msg = None
        # output
        self.out = None  # Recipient is Elevator Controller
        # component vars
        self.doors = {}   # Map<int, StatusDoor>
        self.curFloor = None  # int
        self.state = STATE.BUSY
        self.floorDoorStatus = None
        self.carDoorStatus = None

    def receive_iStCar(self):
        self.iStCar_msg = self.iStCar.recv()
        self.doors[0] = self.iStCar_msg.contents.get("content")  # Index 0 reserved for Car Door
        self.write_log(self.get_sim_time(), self.get_real_time(), "ElevCar", "DoorStatusProc", "R", self.iStCar_msg.contents)

    def poll_iStFloor(self, floor_no):
        if floor_no is 1:
            return self.iStFloor1.poll()
        elif floor_no is 2:
            return self.iStFloor2.poll()
        elif floor_no is 3:
            return self.iStFloor3.poll()
        elif floor_no is 4:
            return self.iStFloor4.poll()
        elif floor_no is 5:
            return self.iStFloor5.poll()
        else:
            return False

    def receive_iStFloor(self, floor_no):
        if floor_no is 1:
            self.iStFloor_msg[1] = self.iStFloor1.recv()
            self.doors[1] = self.iStFloor_msg[1].contents.get("content")

        elif floor_no is 2:
            self.iStFloor_msg[2] = self.iStFloor2.recv()
            self.doors[2] = self.iStFloor_msg[2].contents.get("content")

        elif floor_no is 3:
            self.iStFloor_msg[3] = self.iStFloor3.recv()
            self.doors[3] = self.iStFloor_msg[3].contents.get("content")

        elif floor_no is 4:
            self.iStFloor_msg[4] = self.iStFloor4.recv()
            self.doors[4] = self.iStFloor_msg[4].contents.get("content")

        elif floor_no is 5:
            self.iStFloor_msg[5] = self.iStFloor5.recv()
            self.doors[5] = self.iStFloor_msg[5].contents.get("content")

    def receive_iStFloor_all(self):
        if self.iStFloor1.poll():
            self.iStFloor_msg[1] = self.iStFloor1.recv()
            self.doors[1] = self.iStFloor_msg[1].contents.get("content")
            self.write_log(self.get_sim_time(), self.get_real_time(), "Floor_1", "DoorStatusProc", "R", self.iStFloor_msg[1].contents)
        if self.iStFloor2.poll():
            self.iStFloor_msg[2] = self.iStFloor2.recv()
            self.doors[2] = self.iStFloor_msg[2].contents.get("content")
            self.write_log(self.get_sim_time(), self.get_real_time(), "Floor_2", "DoorStatusProc", "R", self.iStFloor_msg[2].contents)
        if self.iStFloor3.poll():
            self.iStFloor_msg[3] = self.iStFloor3.recv()
            self.doors[3] = self.iStFloor_msg[3].contents.get("content")
            self.write_log(self.get_sim_time(), self.get_real_time(), "Floor_3", "DoorStatusProc", "R", self.iStFloor_msg[3].contents)
        if self.iStFloor4.poll():
            self.iStFloor_msg[4] = self.iStFloor4.recv()
            self.doors[4] = self.iStFloor_msg[4].contents.get("content")
            self.write_log(self.get_sim_time(), self.get_real_time(), "Floor_4", "DoorStatusProc", "R", self.iStFloor_msg[4].contents)
        if self.iStFloor5.poll():
            self.iStFloor_msg[5] = self.iStFloor5.recv()
            self.doors[5] = self.iStFloor_msg[5].contents.get("content")
            self.write_log(self.get_sim_time(), self.get_real_time(), "Floor_5", "DoorStatusProc", "R", self.iStFloor_msg[5].contents)

    def receive_input(self):
        self.input_msg = self.input.recv()
        self.curFloor = self.input_msg.contents.get("ELEV")
        self.write_log(self.get_sim_time(), self.get_real_time(), "ElevCtrl", "DoorStatusProc", "R", self.input_msg.contents)

    def send_out(self, msg):
        self.out.send(msg)
        self.write_log(self.get_sim_time(), self.get_real_time(), "DoorStatusProc", "ElevCtrl", "S", msg.contents)

    def state_processor(self):
        while True:
            if self.state == STATE.BUSY:
                if self.poll_iStFloor(self.curFloor) and self.iStCar.poll():
                    self.receive_iStCar()
                    self.receive_iStFloor(self.curFloor)

                    if self.doors[self.curFloor] is StatusDoor.DOOR_FLOOR_CLOSED and self.doors[0] is StatusDoor.DOOR_CAR_CLOSED:
                        self.send_out(MsgDoor(StatusDoor.DOOR_BOTH_CLOSED, self.curFloor, False))
                        self.curFloor = None
                        self.change_state(STATE.DONE)
                        continue

                    elif self.doors[self.curFloor] is StatusDoor.DOOR_FLOOR_OPENED and self.doors[0] is StatusDoor.DOOR_CAR_OPENED:
                        self.send_out(MsgDoor(StatusDoor.DOOR_BOTH_OPENED, self.curFloor, False))
                        self.curFloor = None
                        self.change_state(STATE.DONE)
                        continue
                    else:
                        continue
                else:
                    continue

            elif self.state == STATE.DONE:
                if self.curFloor is None:
                    self.receive_input()
                    self.change_state(STATE.BUSY)
                    continue

    def main(self):
        self.state_processor()


if __name__ == '__main__':
    dsp = DoorStatusProcessor()
    dsp.main()
