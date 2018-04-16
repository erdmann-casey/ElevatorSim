from enum import Enum


class Msg(object):
    def __init__(self, content):
        self.contents = {"content": content}


class Command(object):
    pass


class Status(object):
    pass


class CommandCar(Command):
    CAR_UP = "CarUP"
    CAR_DOWN = "CarDOWN"
    CAR_MOVE = "CarMOVE"
    CAR_STOP = "CarSTOP"


class StatusCar(Status):
    CAR_READY_TO_MOVE = "CarREADYTOMOVE"
    CAR_MOVING = "CarMOVING"
    CAR_OPENING = "CarOPENING"
    CAR_STOPPED = "CarSTOPPED"


class MsgCar(Msg):
    pass


class CommandDoor(Command):
    DOOR_FLOOR_X_OPEN = "DoorFloorXOPEN"
    DOOR_FLOOR_X_CLOSE = "DoorFloorXCLOSE"
    DOOR_CAR_OPEN = "DoorCarOPEN"
    DOOR_CAR_CLOSE = "DoorCarCLOSE"


class StatusDoor(Status):
    DOOR_FLOOR_OPENED = "DoorFloorXOPENED"
    DOOR_FLOOR_CLOSED = "DoorFloorXCLOSED"
    DOOR_CAR_OPENED = "DoorCarOPENED"
    DOOR_CAR_CLOSED = "DoorCarCLOSED"


class MsgDoor(Msg):
    def __init__(self, content, floor_id):
        self.contents = {"content": content, "id": floor_id}


class CommandMotor(Command):
    MOTOR_FORWARD = "MotorFORWARD"
    MOTOR_BACKWARD = "MotorBACKWARD"
    MOTOR_STOP = "MotorSTOP"


class StatusMotor(Status):
    MOTOR_MOVING = "MotorMOVING"
    MOTOR_REACHED = "MotorREACHED"


class MsgMotor(Msg):
    pass


class CommandReq(Command):

    pass


class MsgReq(Msg):
    pass


class CommandElev(Command):
    pass


class MsgElev(Msg):
    pass


class CommandFloor(Command):
    FLOOR_X_DOWN = "FloorXDOWN"
    FLOOR_X_UP = "FloorXUP"
    FLOOR_REQ = "FloorRequest"


class MsgFloor(Msg):

    def __init__(self, content, floor_id):
        self.contents = {"CommandDoor": content, "id": floor_id}
