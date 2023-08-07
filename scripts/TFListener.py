#!/usr/bin/python3.8
# from re import X

import rospy
import tf
import os
import math

import sys
import copy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import tf2_geometry_msgs
import tf2_ros

import serial
import struct

from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose

from threading import Thread
from sensor_msgs.msg import JointState

class TFListener:
    
    def __init__(self):

        # self.ser = serial.Serial(
        # port='/dev/ttyUSB0',
        # baudrate=9600,
        # parity=serial.PARITY_NONE,
        # stopbits=serial.STOPBITS_ONE,
        # bytesize=serial.EIGHTBITS
        # )

        self.X = 0
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
        
        rospy.init_node('WH_listener', anonymous=True)

        self.tflistener = tf.TransformListener()



        moveit_commander.roscpp_initialize(sys.argv)
 
     
        robot = moveit_commander.RobotCommander()
        scene = moveit_commander.PlanningSceneInterface()
        group_name = "Arm"
        move_group = moveit_commander.MoveGroupCommander(group_name)

        display_trajectory_publisher = rospy.Publisher(
            "/move_group/display_planned_path",
            moveit_msgs.msg.DisplayTrajectory,
            queue_size=20,
        )

        planning_frame = move_group.get_planning_frame()
        print("============ Planning frame: %s" % planning_frame)

        # We can also print the name of the end-effector link for this group:
        eef_link = move_group.get_end_effector_link()
        print("============ End effector link: %s" % eef_link)

        # We can get a list of all the groups in the robot:
        group_names = robot.get_group_names()
        print("============ Available Planning Groups:", robot.get_group_names())

        # Sometimes for debugging it is useful to print the entire state of the
        # robot:
        print("============ Printing robot state")
        print(robot.get_current_state())
        print("")
        ## END_SUB_TUTORIAL

        # Misc variables
        self.box_name = ""
        self.robot = robot
        self.scene = scene
        self.move_group = move_group
        self.display_trajectory_publisher = display_trajectory_publisher
        self.planning_frame = planning_frame
        self.eef_link = eef_link
        self.group_names = group_names

    def ValveOn(self):
        thestring = b'\xA0\x01\x01\xA2'
        # thestring = b'\xA0\x02\x01\xA3'
        self.ser.write(thestring)
    
         
    def ValveOff(self):
        thestring = b'\xA0\x01\x00\xA1'
        # thestring = b'\xA0\x02\x00\xA2'
        self.ser.write(thestring)

    def RosSpin(sefl):
        rospy.spin()
        
        
    def nodeCallback(self,message):
       
        try:

            self.J1 = round(math.degrees(message.position[0]),3) 
            self.J2 = round(math.degrees(message.position[1]),3) 
            self.J3 = round(math.degrees(message.position[2]),3) 
            self.J4 = round(math.degrees(message.position[3]),3) 
            self.J5 = round(math.degrees(message.position[4]),3) 
            self.J6 = round(math.degrees(message.position[5]),3) 
 

            # listen to transform
            (trans,rot) = self.tflistener.lookupTransform('/link6', '/base_link', rospy.Time(0))
            
            # print the transform
            #os.system('clear')

            self.X =round(trans[0]*100,3)
            self.Y =round(trans[1]*100,3)
            self.Z =round(trans[2]*100,3)


            quaternion = (rot[0],rot[1],rot[2],rot[3])
            euler = tf.transformations.euler_from_quaternion(quaternion)
            self.RX = round(math.degrees(euler[0]),3)
            self.RY = round(math.degrees(euler[1]),3)
            self.RZ = round(math.degrees(euler[2]),3)
            # print('X: ',self.X,'Y: ',self.Y,'Z: ',self.Z)
            # print('RX: ',self.RX,'RY: ',self.RY,'RZ: ',self.RZ)

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            return
        


   

    def Initialize(self):
        rospy.Subscriber("joint_states", JointState, self.nodeCallback, queue_size=1)

        windowListenThread = Thread(target=self.RosSpin)
        windowListenThread.start()
        return




    def all_close(self, goal, actual, tolerance):

        if type(goal) is list:
            for index in range(len(goal)):
                if abs(actual[index] - goal[index]) > tolerance:
                    return False

        elif type(goal) is geometry_msgs.msg.PoseStamped:
            return all_close(goal.pose, actual.pose, tolerance)

        elif type(goal) is geometry_msgs.msg.Pose:
            x0, y0, z0, qx0, qy0, qz0, qw0 = pose_to_list(actual)
            x1, y1, z1, qx1, qy1, qz1, qw1 = pose_to_list(goal)
            # Euclidean distance
            d = dist((x1, y1, z1), (x0, y0, z0))
            # phi = angle between orientations
            cos_phi_half = fabs(qx0 * qx1 + qy0 * qy1 + qz0 * qz1 + qw0 * qw1)
            return d <= tolerance and cos_phi_half >= cos(tolerance / 2.0)

        return True

    def homeRobot(self):

        move_group = self.move_group

        joint_goal = move_group.get_current_joint_values()
        joint_goal[0] = 0
        joint_goal[1] = 0
        joint_goal[2] = 0
        joint_goal[3] = 0
        joint_goal[4] = 0
        joint_goal[5] = 0
       

        move_group.go(joint_goal, wait=False)
        move_group.stop()

    def offsetJoint(self,jointIndex,offset):

        jointIndex = jointIndex - 1
        move_group = self.move_group
        joint_goal = move_group.get_current_joint_values()
        offsetRad = offset/180*3.14
        joint_goal[jointIndex] = joint_goal[jointIndex] +  offsetRad     
        move_group.go(joint_goal, wait=False)
        # move_group.stop()    


    def go_to_pose_goal(self):

        move_group = self.move_group


        pose_goal = geometry_msgs.msg.Pose()
        pose_goal.orientation.w = 1.0
        pose_goal.position.x = 0.4
        pose_goal.position.y = 0.1
        pose_goal.position.z = 0.4

        move_group.set_pose_target(pose_goal)


        success = move_group.go(wait=True)

        move_group.stop()

        move_group.clear_pose_targets()

        current_pose = self.move_group.get_current_pose().pose
        return all_close(pose_goal, current_pose, 0.01)

    def plan_cartesian_path(self, scale=1):

        move_group = self.move_group

        waypoints = []

        wpose = move_group.get_current_pose().pose

        wpose.position.z -= scale * 0.06  # First move up (z)
        waypoints.append(copy.deepcopy(wpose))
       

        # wpose.position.y += scale * 0.05  # and sideways (y)
        # waypoints.append(copy.deepcopy(wpose))
        # wpose.position.y -= scale * 0.05  # and sideways (y)
        # waypoints.append(copy.deepcopy(wpose))

        # wpose.position.x += scale * 0.05 # Second move forward/backwards in (x)
        # waypoints.append(copy.deepcopy(wpose))

        # wpose.position.x -= scale * 0.05 # Second move forward/backwards in (x)
        # waypoints.append(copy.deepcopy(wpose))

        wpose.position.z += scale * 0.06  # First move up (z)
        waypoints.append(copy.deepcopy(wpose))  

        (plan, fraction) = move_group.compute_cartesian_path(
            waypoints, 0.0005, 0.0  # waypoints to follow  # eef_step
        )  # jump_threshold

        # Note: We are just planning, not asking move_group to actually move the robot yet:

        self.execute_plan(plan)

        return plan, fraction

        ## END_SUB_TUTORIAL

    

    def execute_plan(self, plan):

        move_group = self.move_group
        move_group.execute(plan, wait=False)

    def tool_move(self,poseOffset,poseIndex):
        
        move_group = self.move_group     

        offsetPose = Pose()
        
        if poseIndex == 0:
            offsetPose.position.x = poseOffset / 0.9
        if poseIndex == 1:
            offsetPose.position.y = poseOffset / 0.8
        if poseIndex == 2:
            offsetPose.position.z = poseOffset
        

        offsetPose.orientation.x = 0
        offsetPose.orientation.y = 0
        offsetPose.orientation.z = 0
        offsetPose.orientation.w = 1

        offset = PoseStamped()
        offset.pose = offsetPose

        now = rospy.Time.now()
        self.tflistener.waitForTransform('base_link', 'link6', now ,rospy.Duration(1) )

        tf_buffer = tf2_ros.Buffer(rospy.Duration(1200.0)) #tf buffer length
        tf_listener = tf2_ros.TransformListener(tf_buffer)

        isSucess = False

        while isSucess == False:
            try:
                transform = tf_buffer.lookup_transform("base_link",
                    'link6', #source frame
                    rospy.Time(0), #get the tf at first available time
                    rospy.Duration(1.0))
                isSucess = True
            except:
                continue

        pose_transformed = tf2_geometry_msgs.do_transform_pose(offset, transform)

        # move_group.set_pose_target(pose_transformed.pose)
        # move_group.go()


        waypoints = []

        wpose = move_group.get_current_pose().pose

        # wpose.position.z -= scale * 0.06  # First move up (z)
        # waypoints.append(copy.deepcopy(wpose))
       

     
        waypoints.append(copy.deepcopy(pose_transformed.pose))
        (plan, fraction) = move_group.compute_cartesian_path(
            waypoints, 0.0005, 0.0  # waypoints to follow  # eef_step
        )  # jump_threshold

        self.execute_plan(plan)

