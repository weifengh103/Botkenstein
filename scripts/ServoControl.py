import time
from adafruit_servokit import ServoKit

class ServoControl:

    # joint angle offset to match 0 degree in ROS. 
    homeAngleOffset = [83,107,46,83,160,85]
    angleAdjScale = 4.0/3.0
    angleAdjScaleSmall = 4.0/3.0
    def __init__(self):
           
        self.kit=ServoKit(channels=16)


    def MoveJ1(self,inputAngle):
        inputAngle = inputAngle * self.angleAdjScale + self.homeAngleOffset[0]
        
        self.kit.servo[0].angle = inputAngle
        return

    def MoveJ2(self,inputAngle):
        inputAngle = inputAngle * self.angleAdjScale + self.homeAngleOffset[1]
        offset = 90 - inputAngle
        angleServo22 = 99+offset
        self.kit.servo[1].angle = inputAngle
        self.kit.servo[2].angle = angleServo22
        return

    def MoveJ3(self,inputAngle):
        inputAngle = -inputAngle
        inputAngle = inputAngle * self.angleAdjScale + self.homeAngleOffset[2]
        self.kit.servo[3].angle = inputAngle
        return

    def MoveJ4(self,inputAngle):
        inputAngle = -inputAngle
        inputAngle = inputAngle * self.angleAdjScale + self.homeAngleOffset[3]
        self.kit.servo[4].angle = inputAngle
        return

    def MoveJ5(self,inputAngle):
        inputAngle = -inputAngle
        inputAngle = inputAngle *self.angleAdjScale+ self.homeAngleOffset[4]
        self.kit.servo[5].angle = inputAngle
        return

    def MoveJ6(self,inputAngle):
        inputAngle = -inputAngle
        inputAngle = inputAngle*self.angleAdjScale + self.homeAngleOffset[5]
        self.kit.servo[6].angle = inputAngle
        return

    def HomeRobot(self):
        # self.MoveJ1(83)
        # self.MoveJ2(107)
        # self.MoveJ3(46)
        # self.MoveJ4(83)
        # self.MoveJ5(160)
        # self.MoveJ6(90)

        self.MoveJ1(0)
        self.MoveJ2(0)
        self.MoveJ3(0)
        self.MoveJ4(0)
        self.MoveJ5(0)
        self.MoveJ6(0)
        



