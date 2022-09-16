#!/usr/bin/python3.8
# from re import X
from re import X
import rospy
import tf
import os
import math

from threading import Thread
from std_msgs.msg import String


class TFListener:
    
    def __init__(self):
        self.X = 1
        self.Y = 0
        self.Z = 0

        self.RX = 0
        self.RY = 0
        self.RZ = 0

        self.J1 = 0
        self.J2 = 0
        self.J3 = 0
        self.J4 = 0
        self.J5 = 0
        self.J6 = 0


    def PoseListener(self):
        # loop forever until roscore or this node is down
        tflistener = tf.TransformListener()
      
       
   

        while not rospy.is_shutdown():
            try:
                # listen to transform
                (trans,rot) = tflistener.lookupTransform('/link6', '/base_link', rospy.Time(0))
              
                # print the transform
                os.system('clear')
                # rospy.loginfo('---------')
                # rospy.loginfo('Translation: ' + str(trans))
                # rospy.loginfo('Rotation: ' + str(rot))

                self.X =round(trans[0]*100,3)
                self.Y =round(trans[1]*100,3)
                self.Z =round(trans[2]*100,3)


                quaternion = (rot[0],rot[1],rot[2],rot[3])
                euler = tf.transformations.euler_from_quaternion(quaternion)
                self.RX = round(math.degrees(euler[0]),3)
                self.RY = round(math.degrees(euler[1]),3)
                self.RZ = round(math.degrees(euler[2]),3)
                print('X: ',self.X,'Y: ',self.Y,'Z: ',self.Z)
                print('RX: ',self.RX,'RY: ',self.RY,'RZ: ',self.RZ)

            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                continue
            # sleep to control the node frequency
                    # set the node to run 1 time per second (1 hz)
            rate = rospy.Rate(50)
            rate.sleep()


   

    def Initialize(self):

        # initialize node
        rospy.init_node('WH_listener')
        rospy.loginfo('started listener node !')
        # create tf listener



        windowListenThread = Thread(target=self.PoseListener)
        windowListenThread.start()
        return

    