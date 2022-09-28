# Project Title

Botkenstein

## Description

BotKenstein is a DIY Robot-AGV (Autonomous Guided Vehicle) project for learning how to build a robot-AGV system from scratch, and apply it for vision based path planing and forlowing, object tracking and handling, charge station docking, and other interesting functions in the future. 

The control software is implemented in Python and run on a Nvidia Jetson Xavier NX developer kit with Ubuntu 20.04 . ROS Noetice is used for robot motion control and its robot joints informoation is sent to the robot's servo motors for real time control. The robot is mounted on a Roomba robot that has two DC driven wheels with encoders. The intelligence in the Roomba is striped out and it is control by the control software.  A Realsense D415 camera is used for all of the vision related tasks. All the vsion functions will be implemented in OpenCV. Also, Tanserflow will be applied for advance deeplearning functions. 


## Project Road Map
* Assemble the DIY robot kit and test the servo motors with arduino. (Achieved)
* Setup ROS Noetic and MoveIt in Jetson Xavier. (Achieved)
* Create URDL file for the robot kit and simulate robot motion in ROS. (Achieved)
* Implement a robot control API with Joint, Tool and World move functions. (Achieved)
* Develop a GUI with PySimpleGUI for robot motion control testing. (Achieved)
* Add servo control to the software.(Achieved)
* Control the real robot with ROS in real time. (Achieved)
* Mount a camera and a suction cup to the robot, and wire the hardware to the onboard outputs. (Achieved)
* Setup OpenCV, Tenserflow and Realsense SDK in the software.
* Implement a vision guided robot pick and place funcion.
* Wire the Roomba DC motors to the Jetson board.
* Implement the motor PID control.
* Mount the robot to the Roomba and setup the system hardware. 
* Develop a deep learning based vision tracking funtion for AGV path following and robot picking. 
* Implement acharge station docking. 
* Add voice control to the system.
* Add more interesting ideas to the list. 
