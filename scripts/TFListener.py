#!/usr/bin/python3.8
# from re import X
from re import X
import rospy
import tf
import os
import math
from threading import Thread

class TFListener:
    
    X = 0
    Y = 0
    Z = 0

    RX = 0
    RY = 0
    RZ = 0

    J1 = 0
    J2 = 0
    J3 = 0
    J4 = 0
    J5 = 0
    J6 = 0


    def PoseListener(self):
        # loop forever until roscore or this node is down
        listener = tf.TransformListener()
        while not rospy.is_shutdown():
            try:
                # listen to transform
                (trans,rot) = listener.lookupTransform('/link6', '/base_link', rospy.Time(0))
              
                # print the transform
                # os.system('clear')
                # rospy.loginfo('---------')
                # rospy.loginfo('Translation: ' + str(trans))
                # rospy.loginfo('Rotation: ' + str(rot))

                X =round(trans[0]*100,3)
                Y =round(trans[1]*100,3)
                Z =round(trans[2]*100,3)


                quaternion = (rot[0],rot[1],rot[2],rot[3])
                euler = tf.transformations.euler_from_quaternion(quaternion)
                RX = round(math.degrees(euler[0]),3)
                RY = round(math.degrees(euler[1]),3)
                RZ = round(math.degrees(euler[2]),3)
                # print('X: ',X,'Y: ',Y,'Z: ',Z)
                # print('RX: ',RX,'RY: ',RY,'RZ: ',RZ)

            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                continue
            # sleep to control the node frequency
                    # set the node to run 1 time per second (1 hz)
            rate = rospy.Rate(1.0)
            rate.sleep()

    def Initialize(self):

        # initialize node
        rospy.init_node('WH_listener')

        rospy.loginfo('started listener node !')
        # create tf listener


        windowListenThread = Thread(target=self.PoseListener)
        windowListenThread.start()
        return

    