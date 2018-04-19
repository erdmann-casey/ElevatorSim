import time
from ElevatorComponent import ElevatorComponent
from Messages import MsgFloor, CommandFloor, MsgDoor, CommandDoor, StatusDoor
from multiprocessing import connection


class FloorDoor(ElevatorComponent):

    processing_time = 1.0  # double
    motion_time = 2.0      # double

    def __init__(self, floor_id, oStatus):
        super().__init__()
        # component variables
        self.id = floor_id           # int
        self.job = None              # entity
        self.out = oStatus
        pass

    def open_door(self):
        time.sleep(self.processing_time)
        time.sleep(self.motion_time)
        self.out.send(MsgDoor(StatusDoor().DOOR_FLOOR_OPENED, self.id, False))

    def close_door(self):
        time.sleep(self.processing_time)
        time.sleep(self.motion_time)
        self.out.send(MsgDoor(StatusDoor().DOOR_FLOOR_CLOSED, self.id, False))

    def state_processor(self):
        while True:
            if self.job is None:
                pass
            elif self.job is CommandDoor.DOOR_FLOOR_X_OPEN:
                self.open_door()
            elif self.job is CommandDoor.DOOR_FLOOR_X_CLOSE:
                self.close_door()

    def main(self):
        self.state_processor()


class Floor(ElevatorComponent):

    def __init__(self, floor_id):
        super().__init__()
        # input
        self.iCmd = None
        # outputS
        self.oReq = None
        self.oStatus = None
        # component vars
        self.door = FloorDoor(floor_id, self.oStatus)
        pass

    def state_processor(self):
        while True:
            try:
                job = self.iCmd.recv()
                self.door.job = job
            except EOFError:
                # Pipe Connection Terminated, TODO: Fix this
                pass
        pass

    def main(self):
        self.state_processor()

    def send_request(self):
        msg = MsgFloor(CommandFloor.FLOOR_REQ, self.door.id)
        self.oReq.send(msg)


if __name__ == '__main__':
    f = Floor(0)
    f.main()

