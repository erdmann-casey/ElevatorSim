import sys

from multiprocessing import Pipe
from ElevatorCar import ElevatorCar
from CarCtrl import CarCtrl
from CarDoor import CarDoor
from CarBtn import CarBtn
from Motor import Motor
from ElevatorController import ElevatorController
from RequestProcessor import RequestProcessor
from DoorStatusProcessor import DoorStatusProcessor
from Floor import Floor
from time import time

class ElevatorSystem(object):

    def __init__(self, num_floors):
        super(ElevatorSystem, self).__init__()

        self.system_time = time()

        # initialize components
        self.elevController = ElevatorController()
        self.requestProc = RequestProcessor()
        self.doorStatusProc = DoorStatusProcessor()
        
        # Special Instation for Elevator Car to handle dependencies for inner communication
        self.elevCar = ElevatorCar(None, self.system_time)
        self.elevCarCtrl = CarCtrl(None, None, None, self.system_time)
        self.elevCarDoor = CarDoor(self.elevCarCtrl, self.elevCar, self.system_time)
        self.elevCarBtn = CarBtn(self.elevCar, self.system_time)
        self.elevCarMotor = Motor(self.elevCarCtrl, self.system_time)

        self.elevCar.ctrl = self.elevCarCtrl
        self.elevCarCtrl.car = self.elevCar
        self.elevCarCtrl.door = self.elevCarDoor
        self.elevCarCtrl.motor = self.elevCarMotor


        # setup pipes, output->input
        self.elevController.done, self.requestProc.input = Pipe()
        """self.elevController.oCmdCar, self.elevCar.iCmd = Pipe()"""
        # Setup Floor pipes separately, skipping self.elevController.oCmdFloor...
        self.elevController.out, self.doorStatusProc.input = Pipe()
        self.requestProc.out, self.elevController.iReq = Pipe()
        self.doorStatusProc.out, self.elevController.iStDoor = Pipe()
        
        self.elevCar.iCmd, self.elevController.oCmdCar = Pipe()
        self.elevCar.oReq, self.requestProc.input_car = Pipe()  # input[0] reserved for ElevCar, [1] = F1, [2] = F2, etc.
        self.elevCar.oStCar, self.elevController.iStCar = Pipe()
        self.elevCar.oStDoor, self.doorStatusProc.iStCar = Pipe()

        # setup pipes to get component states
        self.requestProc.state_comm, self.rp_pipe = Pipe()

        # Floor Pipes
        f1_iCmd, self.elevController.oCmdFloor1 = Pipe()
        f1_oReq, self.requestProc.input_floor1 = Pipe()
        f1_oStatus, self.doorStatusProc.iStFloor1 = Pipe()
        #
        f2_iCmd, self.elevController.oCmdFloor2 = Pipe()
        f2_oReq, self.requestProc.input_floor2 = Pipe()
        f2_oStatus, self.doorStatusProc.iStFloor2 = Pipe()
        #
        f3_iCmd, self.elevController.oCmdFloor3 = Pipe()
        f3_oReq, self.requestProc.input_floor3 = Pipe()
        f3_oStatus, self.doorStatusProc.iStFloor3 = Pipe()
        #
        f4_iCmd, self.elevController.oCmdFloor4 = Pipe()
        f4_oReq, self.requestProc.input_floor4 = Pipe()
        f4_oStatus, self.doorStatusProc.iStFloor4 = Pipe()
        #
        f5_iCmd, self.elevController.oCmdFloor5 = Pipe()
        f5_oReq, self.requestProc.input_floor5 = Pipe()
        f5_oStatus, self.doorStatusProc.iStFloor5 = Pipe()

        # Instantiate Floors
        # self.floors = [Floor(num) for num in range(num_floors)]
        self.floors = { 1: Floor(1, f1_iCmd, f1_oReq, f1_oStatus), 2: Floor(2, f2_iCmd, f2_oReq, f2_oStatus), 3: Floor(3, f3_iCmd, f3_oReq, f3_oStatus), 4: Floor(4, f4_iCmd, f4_oReq, f4_oStatus), 5: Floor(5, f5_iCmd, f5_oReq, f5_oStatus) }
        """
        for num in range(num_floors):
            # Floor Pipes...
            self.floors.get(num).iCmd, self.elevController.oCmdFloor[num] = Pipe()
            self.floors.get(num).oReq, self.requestProc.input[num] = Pipe()
            self.floors.get(num).oStatus, self.doorStatusProc.iStFloor[num] = Pipe()
        """

    def start_elevator_system(self):
        self.elevCar.start()
        self.elevCarCtrl.start()
        self.elevCarDoor.start()
        self.elevCarBtn.start()
        self.elevCarMotor.start()
        self.elevController.start()
        self.requestProc.start()
        self.doorStatusProc.start()
        # Floors
        for num in range(5):
            if num is 0:
                continue
            else:
                self.floors.get(num).start()
                self.floors.get(num).door.start()

    def print_component_states(self):
        """
        So. Obviously. These are references to the objects, not the processes.
        So. You know. This doesn't work. Obviously.
        """
        self.rp_pipe.send(True)
        print("Current States:")
        # print Elevator Car States
        print("Elevator Controller: {}".format(self.elevController.state))
        # print("Request Processor: {}".format(self.rp_pipe.recv()))
        print("Request Processor: {}".format(self.requestProc.state))
        print("Door Status Processor: {}".format(self.doorStatusProc.state))

    def elevator_menu(self):
        while True:
            for floor_id in self.floors:
                print("{}) Go To Floor {}".format(floor_id, floor_id))
            print("C) Cancel")

            user_input = input("Please Select a Floor: ")

            if user_input == 'c' or user_input == 'C':
                break
            else:
                floor_no = int(user_input)
                if 0 < floor_no <= len(self.floors):
                    # TODO: ElevCar.PressButton(floor_no)
                    print("Queueing Floor {} For Next Stop".format(floor_no))
                    break
                else:
                    print("Floor {} does not exist".format(floor_no))

    def floor_menu(self):
        while True:
            for floor_id in self.floors:
                print("{}) Request Elevator from Floor {}".format(floor_id, floor_id))
            print("C) Cancel")

            user_input = input("Please Select a Floor: ")

            if user_input == 'c' or user_input == 'C':
                break
            else:
                floor_no = int(user_input)
                if 0 < floor_no <= len(self.floors):
                    print("Calling Elevator from floor {}".format(floor_no))
                    self.floors[floor_no].send_request()
                    break
                else:
                    print("Floor {} does not exist".format(floor_no))

    def check_all_processes_live(self):
        if not self.elevCar.is_alive():
            print("ElevCar Process Not Running!!")
        if not self.elevCarBtn.is_alive():
            print("ElevCarBtn Process Not Running!!")
        if not self.elevCarCtrl.is_alive():
            print("ElevCarCtrl Process Not Running!!")
        if not self.elevCarDoor.is_alive():
            print("ElevCarDoor Process Not Running!!")
        if not self.elevCarMotor.is_alive():
            print("ElevCarMotor Process Not Running!!")
        if not self.doorStatusProc.is_alive():
            print("DoorStatusProc Process Not Running!!")
        if not self.elevController.is_alive():
            print("ElevCtrl Process Not Running!!")
        if not self.requestProc.is_alive():
            print("RequestProc Process Not Running!!")

    def action_menu(self):
        while True:
            self.check_all_processes_live()

            print(
                "\n"
                "1) Start Elevator System\n"
                "2) Print Component States\n"
                "3) Intercept Communications\n"
                "4) Press Elevator Button\n"
                "5) Press Floor Button\n"
                "Q) Quit\n"
            )

            user_input = input("Selection: ")
            print("Your input: " + user_input + "\n")

            if user_input == '1':
                self.start_elevator_system()

            elif user_input == '2':
                self.print_component_states()

            elif user_input == '3':
                pass

            elif user_input == '4':
                self.elevator_menu()

            elif user_input == '5':
                self.floor_menu()

            elif user_input == 'q' or user_input == 'Q':
                print("Exiting...\n")
                break

            else:
                print("Invalid Input\n")

    def main(self):
        self.action_menu()
        if self.elevCar.is_alive():
            self.elevCar.terminate()
            self.elevCar.join()

        if self.elevCarBtn.is_alive():
            self.elevCarBtn.terminate()
            self.elevCarBtn.join()

        if self.elevCarCtrl.is_alive():
            self.elevCarCtrl.terminate()
            self.elevCarCtrl.join()

        if self.elevCarDoor.is_alive():
            self.elevCarDoor.terminate()
            self.elevCarDoor.join()

        if self.elevCarMotor.is_alive():
            self.elevCarMotor.terminate()
            self.elevCarMotor.join()

        if self.elevController.is_alive():
            self.elevController.terminate()
            self.elevController.join()

        if self.requestProc.is_alive():
            self.requestProc.terminate()
            self.requestProc.join()

        if self.doorStatusProc.is_alive():
            self.doorStatusProc.terminate()
            self.doorStatusProc.join()

        for floor_no in self.floors:
            if self.floors.get(floor_no).is_alive():
                self.floors.get(floor_no).terminate()
                self.floors.get(floor_no).join()


if __name__ == '__main__':
    es = ElevatorSystem(5)
    es.main()

