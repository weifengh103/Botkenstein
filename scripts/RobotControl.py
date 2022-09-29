#!/usr/bin/python3.8

from __future__ import print_function
from six.moves import input

import time
import tf
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import tf2_geometry_msgs
import tf2_ros

from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose
from visualization_msgs.msg import Marker, MarkerArray

from math import pi, tau, dist, fabs, cos


from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list



class RobotControl(object):


    def __init__(self):

      
      
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node("move_group_python_interface_tutorial", anonymous=True)
        self.tl = tf.TransformListener()
     
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

    def go_to_joint_state(self):

        move_group = self.move_group

        joint_goal = move_group.get_current_joint_values()
        joint_goal[0] = 0
        joint_goal[1] = 0
        joint_goal[2] = 0
        joint_goal[3] = 0
        joint_goal[4] = 0
        joint_goal[5] = 0
       

        move_group.go(joint_goal, wait=True)
        move_group.stop()

  


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
        wpose.position.z -= scale * 0.1  # First move up (z)
        waypoints.append(copy.deepcopy(wpose))
        wpose.position.z += scale * 0.1  # First move up (z)
        waypoints.append(copy.deepcopy(wpose))  

        wpose.position.y += scale * 0.10  # and sideways (y)
        waypoints.append(copy.deepcopy(wpose))
        wpose.position.y -= scale * 0.10  # and sideways (y)
        waypoints.append(copy.deepcopy(wpose))

        wpose.position.x += scale * 0.1 # Second move forward/backwards in (x)
        waypoints.append(copy.deepcopy(wpose))

        wpose.position.x -= scale * 0.1 # Second move forward/backwards in (x)
        waypoints.append(copy.deepcopy(wpose))


        (plan, fraction) = move_group.compute_cartesian_path(
            waypoints, 0.1, 0.0  # waypoints to follow  # eef_step
        )  # jump_threshold

        # Note: We are just planning, not asking move_group to actually move the robot yet:

        self.execute_plan(plan)

        return plan, fraction

        ## END_SUB_TUTORIAL

    

    def execute_plan(self, plan):

        move_group = self.move_group
        move_group.execute(plan, wait=True)

    def tool_move(self):
        
        move_group = self.move_group     

        offsetPose = Pose()
        offsetPose.position.x = 0
        offsetPose.position.y = 0
        offsetPose.position.z = 0.15

        offsetPose.orientation.x = 0
        offsetPose.orientation.y = 0
        offsetPose.orientation.z = 0
        offsetPose.orientation.w = 1

        offset = PoseStamped()
        offset.pose = offsetPose

        now = rospy.Time.now()
        self.tl.waitForTransform('base_link', 'link6', now ,rospy.Duration(1) )

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
        print("pose_transformed",pose_transformed.pose)
        move_group.set_pose_target(pose_transformed.pose)
        move_group.go()


