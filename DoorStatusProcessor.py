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
        self.state = STATE.DONE
        self.floorDoorStatus = None
        self.carDoorStatus = None

    def receive_iStCar(self):
        self.iStCar_msg = self.iStCar.recv()
        self.doors[0] = self.iStCar_msg.contents.get("value")  # Index 0 reserved for Car Door
        self.write_log(self.get_sim_time(), self.get_real_time(), "ElevCar", "DoorStatusProc", "R", "iStCar", self.iStCar_msg)

    def poll_iStFloor(self, floor_no):
        if floor_no == 1:
            return self.iStFloor1.poll()
        elif floor_no == 2:
            return self.iStFloor2.poll()
        elif floor_no == 3:
            return self.iStFloor3.poll()
        elif floor_no == 4:
            return self.iStFloor4.poll()
        elif floor_no == 5:
            return self.iStFloor5.poll()
        else:
            return False

    def receive_iStFloor(self, floor_no):
        if floor_no == 1:
            self.iStFloor_msg[1] = self.iStFloor1.recv()
            self.doors[1] = self.iStFloor_msg[1].contents.get("value")
            self.write_log(self.get_sim_time(), self.get_real_time(), "Floor_1", "DoorStatusProc", "R", "iStFloor", self.iStFloor_msg[1])

        elif floor_no == 2:
            self.iStFloor_msg[2] = self.iStFloor2.recv()
            self.doors[2] = self.iStFloor_msg[2].contents.get("value")
            self.write_log(self.get_sim_time(), self.get_real_time(), "Floor_2", "DoorStatusProc", "R", "iStFloor",  self.iStFloor_msg[2])

        elif floor_no == 3:
            self.iStFloor_msg[3] = self.iStFloor3.recv()
            self.doors[3] = self.iStFloor_msg[3].contents.get("value")
            self.write_log(self.get_sim_time(), self.get_real_time(), "Floor_3", "DoorStatusProc", "R", "iStFloor",  self.iStFloor_msg[3])

        elif floor_no == 4:
            self.iStFloor_msg[4] = self.iStFloor4.recv()
            self.doors[4] = self.iStFloor_msg[4].contents.get("value")
            self.write_log(self.get_sim_time(), self.get_real_time(), "Floor_4", "DoorStatusProc", "R", "iStFloor",  self.iStFloor_msg[4])

        elif floor_no == 5:
            self.iStFloor_msg[5] = self.iStFloor5.recv()
            self.doors[5] = self.iStFloor_msg[5].contents.get("value")
            self.write_log(self.get_sim_time(), self.get_real_time(), "Floor_5", "DoorStatusProc", "R", "iStFloor",  self.iStFloor_msg[5])

    def receive_iStFloor_all(self):
        if self.iStFloor1.poll():
            self.receive_iStFloor(1)
        if self.iStFloor2.poll():
            self.receive_iStFloor(2)
        if self.iStFloor3.poll():
            self.receive_iStFloor(3)
        if self.iStFloor4.poll():
            self.receive_iStFloor(4)
        if self.iStFloor5.poll():
            self.receive_iStFloor(5)

    def receive_input(self):
        self.input_msg = self.input.recv()
        self.curFloor = self.input_msg.contents.get("value").get("ELEV")
        self.write_log(self.get_sim_time(), self.get_real_time(), "ElevCtrl", "DoorStatusProc", "R", "in", self.input_msg)

    def send_out(self, msg):
        self.out.send(msg)
        self.write_log(self.get_sim_time(), self.get_real_time(), "DoorStatusProc", "ElevCtrl", "S", "out", msg)

    def state_processor(self):
        while True:
            if self.state == STATE.BUSY:
                if self.iStCar.poll():
                    self.receive_iStCar()
                self.receive_iStFloor_all()

                if self.doors.get(self.curFloor) == StatusDoor.DOOR_FLOOR_CLOSED and self.doors.get(0) == StatusDoor.DOOR_CAR_CLOSED:
                    print("----Door States synchronized!!----")
                    self.send_out(MsgDoor("out", StatusDoor.DOOR_BOTH_CLOSED, self.curFloor, False))
                    self.curFloor = None
                    self.change_state(STATE.DONE)
                    continue

                elif self.doors.get(self.curFloor) == StatusDoor.DOOR_FLOOR_OPENED and self.doors.get(0) == StatusDoor.DOOR_CAR_OPENED:
                    print("----Door States synchronized!!----")
                    self.send_out(MsgDoor("out", StatusDoor.DOOR_BOTH_OPENED, self.curFloor, False))
                    self.curFloor = None
                    self.change_state(STATE.DONE)
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
