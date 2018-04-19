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
        self.iStFloor = {}  # Received from Floor(s)
        self.input = None     # Received from Elevator Controller
        # msg
        self.iStCar_msg = None
        self.iStFloor_msg = {}
        self.input_msg = None
        # output
        self.out = None  # Recipient is Elevator Controller
        # component vars
        self.doors = dict()   # Map<int, StatusDoor>
        self.curFloor = None  # int
        self.state = STATE.BUSY
        self.floorDoorStatus = None
        self.carDoorStatus = None

    def receive_iStCar(self):
        if self.iStCar.poll():
            self.iStCar_msg = self.iStCar.recv()
            self.doors[0] = self.iStCar_msg.contents.get("content")  # Index 0 reserved for Car Door
            # TODO: Fill In Proper Times
            self.write_log(self.get_sim_time(), self.get_real_time(), "ElevCar", "DoorStatusProc", "R", self.iStCar_msg.contents)
            return True
        else:
            return False

    def poll_iStFloor(self):
        for conn in self.iStFloor:
            index = 1
            if conn.poll():
                return True
            else:
                index += 1
                continue
        return False

    def receive_iStFloor(self):
        for conn in self.iStFloor:
            index = 1
            if conn.poll():
                self.iStFloor_msg[index] = conn.recv()
                self.doors[self.iStFloor_msg[index].contents.get("id")] = self.iStFloor_msg[index].contents.get("content")
                # TODO: Fill In Proper Times
                self.write_log(self.get_sim_time(), self.get_real_time(), "Floor_" + str(index), "DoorStatusProc", "R", self.iStFloor_msg[index].contents)
                return True
            else:
                index += 1
                continue
        return False

    def receive_input(self):
        if self.input.poll():
            self.input_msg = self.input.recv()
            # TODO: Fill In Proper Times
            self.write_log(self.get_sim_time(), self.get_real_time(), "ElevCtrl", "DoorStatusProc", "R", self.input_msg.contents)
            return True
        else:
            return False

    def send_out(self, msg):
        self.out.send(msg)
        # TODO: Fill In Proper Times
        self.write_log(self.get_sim_time(), self.get_real_time(), "DoorStatusProc", "ElevCtrl", "S", msg.contents)

    def state_processor(self):
        while True:
            if self.state == STATE.BUSY:
                if self.input.poll():
                    # TODO: Finish this code block
                    # Check if Correct MsgDoor
                    # Above Met: MoveTo STATE.BUSY
                    pass
                else:
                    if self.floorDoorStatus is StatusDoor.DOOR_FLOOR_CLOSED and self.carDoorStatus is StatusDoor.DOOR_CAR_CLOSED:
                        self.send_out(MsgDoor(StatusDoor.DOOR_BOTH_CLOSED, self.curFloor, False))
                        self.change_state(STATE.DONE)

                    elif self.floorDoorStatus is StatusDoor.DOOR_FLOOR_OPENED and self.carDoorStatus is StatusDoor.DOOR_CAR_OPENED:
                        self.send_out(MsgDoor(StatusDoor.DOOR_BOTH_OPENED, self.curFloor, False))
                        self.change_state(STATE.DONE)

                    # TODO: Finish this code block
                    # oStatus ! MsgDoor (Under what criteria do we send this message? Every iteration?)
                    # Above Met: MoveTo STATE.DONE
                    pass

            elif self.state == STATE.DONE:
                if self.poll_iStFloor() and self.iStCar.poll():
                    self.receive_iStCar()
                    self.receive_iStFloor()
                    if self.floorDoorStatus is not None and self.floorDoorStatus is self.carDoorStatus:
                        self.change_state(STATE.BUSY)

    def main(self):
        self.state_processor()


if __name__ == '__main__':
    dsp = DoorStatusProcessor()
    dsp.main()
