import sys

from multiprocessing import Pipe
from ElevatorCar import ElevatorCar
from ElevatorComponent import ElevatorComponent
from ElevatorController import ElevatorController
from RequestProcessor import RequestProcessor
from DoorStatusProcessor import DoorStatusProcessor
from Floor import Floor


class ElevatorSystem(object):

    def __init__(self, num_floors):
        super(ElevatorSystem, self).__init__()
        # initialize components
        """self.elevCar = ElevatorCar()"""
        self.elevController = ElevatorController()
        self.requestProc = RequestProcessor()
        self.doorStatusProc = DoorStatusProcessor()
        self.floors = [Floor(num) for num in range(num_floors)]

        # setup pipes, output->input
        """
        self.elevCar.oReq, self.requestProc.input = Pipe()
        self.elevCar.oStCar, self.elevController.iStCar = Pipe()
        self.elevCar.oStDoor, self.doorStatusProc.iStCar = Pipe()
        """
        self.elevController.done, self.requestProc.input = Pipe()
        """self.elevController.oCmdCar, self.elevCar.iCmd = Pipe()"""
        # Setup Floor pipes separately, skipping self.elevController.oCmdFloor...
        self.elevController.out, self.doorStatusProc.input = Pipe()
        self.requestProc.out, self.elevController.iReq, Pipe()
        self.doorStatusProc.out, self.elevController.iReq = Pipe()
        for num in range(num_floors):
            # Floor Pipes...
            self.floors[num].iCmd, self.elevController.oCmdFloor = Pipe()
            self.floors[num].oReq, self.requestProc.input = Pipe()
            self.floors[num].oStatus, self.doorStatusProc.iStFloor = Pipe()
            """
            This results in only the last floor to retain functional pipes to the other components
            Solution? io arrays to match floors? setup single pipe when needed (how will floors send requests)?
            Pipes are PAIRS of connection objects...
            
            Utilizing Sockets, the Server for each component could receive messages from an arbitrary number of
            senders, just with the need to identify who the sender was to properly process that message. Pipes require
            a hardline, one-to-one connection. How to solve this problem so that an arbitrary number of floors can all
            be piped into singleton components?
            """

    def start_elevator_system(self):
        #self.elevCar.start()
        #self.elevController.start()
        self.requestProc.start()
        #self.doorStatusProc.start()
        for floor in self.floors:
            floor.start()

    def print_component_states(self):
        print("Current States:")
        # print Elevator Car States
        print("Elevator Controller: {}".format(self.elevController.state.value))
        print("Request Processor: {}".format(self.requestProc.state.value))
        print("Door Status Processor: {}".format(self.doorStatusProc.state.value))

    def elevator_menu(self):
        while True:
            for floor in self.floors:
                print("{}) Go To Floor {}".format(floor.door.id, floor.door.id))
            print("C) Cancel")

            user_input = input("Please Select a Floor: ")

            if user_input == 'c' or user_input == 'C':
                break
            else:
                floor_no = int(user_input)
                if 0 < floor_no <= len(self.floors):
                    print("Queueing Floor {} For Next Stop".format(floor_no))
                    break
                else:
                    print("Floor {} does not exist".format(floor_no))

    def floor_menu(self):
        while True:
            for floor in self.floors:
                print("{}) Request Elevator from Floor {}".format(floor.door.id, floor.door.id))
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

    def action_menu(self):
        while True:
            if self.elevController.is_alive() and self.doorStatusProc.is_alive() and self.requestProc.is_alive():
                print("\n-----All Processes Live!-----\n")

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
        # if self.elevCar.is_alive():
            # self.elevCar.terminate()
            # self.elevCar.join()
        if self.elevController.is_alive():
            self.elevController.terminate()
            self.elevController.join()
        if self.requestProc.is_alive():
            self.requestProc.terminate()
            self.requestProc.join()
        if self.doorStatusProc.is_alive():
            self.doorStatusProc.terminate()
            self.doorStatusProc.join()
        for floor in self.floors:
            if floor.is_alive():
                floor.terminate()
                floor.join()


if __name__ == '__main__':
    es = ElevatorSystem(5)
    es.main()

