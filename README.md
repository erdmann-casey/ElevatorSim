# ElevatorSim
A functional model of an elevator written in python used to conduct research about Cyber Attacks/Effects on CPS

## How to Run the Simulator

To run the simulation simply execute the following:
`python3 ElevatorSystem.py`

***Advisory***: This simulation relies heavily on multiprocessing and multithreading, and is a very raw implementation of this type of system. As such multiple processes/threads run in infinite loops and can cause lower resource systems to crash/hang in the event of specific actions (such as an attack simulation that causes an component to run forever). The simulation is not currently optimized, and although it is stable and usable, you alone are responsible for running the simulator at your own risk.

On initial execution you will see a menu with several options:

```
1) Start Elevator System
2) Print Component States
3) Intercept Communications
4) Press Elevator Button
5) Press Floor Button
6) Enable An Attack! (Do this first if you want to test attacks)
Q) Quit

Selection:
```

Each of these options will perform a different action depending on how you want to utilize the simulation. Some features are currently either not fully implmented or not implemented at all and will be marked as such below.

- **1) Start Elevator System** - Starts all compoenents of the elevator system effectively turning the entire elevator "on". This is essentially starts the simulation. Once the system is on, the menu options 4 and 5 can be interacted with to cause the elevator to move to different floors.
- **2) Print Component States** *(not fully implemented)*: Selecting this option will print the current state of all running components. At this time, only the following component states will print: Elevator Controller, Request Processor, Door Status Processor, Elevator Car, Car Controller, Motor, Car Door. It is also important to note that some state transitions are instant, so debugging states via this menu item is not reccommended. This option is more for simple state observation after performing specific actions to see if the resulting effects made a more permanent or drastic impact on a component state.
- **3) Intercept Communications** *(not implemented)*: This feature is not currently implemented. The intent for this feature is that by selecting this feature you would be able to dynamically create an attacker component as the simulation is running, and intercept messages between components to do some MitM attack testing. This is a more advanced feature that was more of an idea to pursue later. The menu item exists still for later implementation, but for now this feature does not work.
- **4) Press Elevator Button**: This feature allows you to emulate being inside of the Elevator Car and selecting a button to go to a specific floor. After selecting a floor, and request message will be sent and the car will move to that floor under normal cirumstances.
- **5) Press Floor Button**: This feature allows you to emulate being outside of the Elevator Car and on certain Floor so that you can select the floor that the car will need to go to in order to pick up a passenger. Traditionally, these are up/down buttons outside of an elevator, however in this model you are able to select a specific floor as a destination since mechanisms for emulating being on an existent floor at the start are not implemented. Also the benefit in doing it this way is when testing attacks based on the floor requests, you are able to test specific floors for various attack ideas more easily.
- **6) Enable an Attack!**: This feature allows you to enable a preset attack included with the base project. To add an attack here simply implement a new attacker component and add the coditional code, any setup, and a menu item to the ElevatorSystem.py script. To use any of the current attacks, you **MUST** run this options **BEFORE** starting the elevator system (option 1)
- **Q) Quit**: Exits the simulation.

## Attack Documentation
At this time there are 3 attacks that can be simulated via this model by default. More attacks can be implemented by following the format of the ElevatorComponent class while referencing existing attacks as examples. Attacks can vary in extreme ways when it comes to implementation, however, using the existing model for MitM pipe communications is a recommended starting point if the attack is simple. If an attack exists inside the ElevatorCar it is recommended to reference the AttackCloseCarDoor.py. This is due to the fact that at this time the Elevator Car uses instances of threaded objects maintained by the Car Controller itself to pass messages rather than pipes used by external components.

- Force Door Close (AttackDoorClose.py) - Forces the Car Door to remain closed at all times resulting in anything inside being trapped in the Elevator Car.
- Force Destination (AttackButtonReq.py) - Forces the Elevator Car to always travel to a floor specified by the attacker regardless of the Car Button's recieved input.
- "Infinite" Motor/Motor Burnout (AttackMotorRun.py) - Forces the elevator car to a non existent floor specified by the attacker, and simultaneously blocks any messages telling the motor to stop running. The result is that the Car Controller will claim to reach the non existent floor, but the motor will never stop causing the car to "crash". Coincidentally this **WILL** cause the simulation to hang, execute with caution.


<img src="mitre-logo.png" width=250/>
<br/>
<img src="csu-logo.png" width=250/>

The above logos used are property of Columbus State University and The MITRE Corporation respectively. These entities provided the opportunity to research the topic of Cyber Effects on Cyber Physical Systems that yielded this open source elevator simulation project. All credit for creating and providing the logical design specification included in this repository goes to the authors/researchers at The MITRE Corporation.
