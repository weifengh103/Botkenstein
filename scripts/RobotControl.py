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

from math import pi, tau, dist, fabs, cos


from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list



class MoveGroupPythonInterfaceTutorial(object):


    def __init__(self):
        # super(MoveGroupPythonInterfaceTutorial, self).__init__()

        ## BEGIN_SUB_TUTORIAL setup
        ##
        ## First initialize `moveit_commander`_ and a `rospy`_ node:
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node("move_group_python_interface_tutorial", anonymous=True)
        self.tl = tf.TransformListener()
        ## Instantiate a `RobotCommander`_ object. Provides information such as the robot's
        ## kinematic model and the robot's current joint states
        robot = moveit_commander.RobotCommander()
        scene = moveit_commander.PlanningSceneInterface()
        group_name = "Arm"
        move_group = moveit_commander.MoveGroupCommander(group_name)

        ## Create a `DisplayTrajectory`_ ROS publisher which is used to display
        ## trajectories in Rviz:
        display_trajectory_publisher = rospy.Publisher(
            "/move_group/display_planned_path",
            moveit_msgs.msg.DisplayTrajectory,
            queue_size=20,
        )

        ## END_SUB_TUTORIAL

        ## BEGIN_SUB_TUTORIAL basic_info
        ##
        ## Getting Basic Information
        ## ^^^^^^^^^^^^^^^^^^^^^^^^^
        # We can get the name of the reference frame for this robot:
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
        """
        Convenience method for testing if the values in two lists are within a tolerance of each other.
        For Pose and PoseStamped inputs, the angle between the two quaternions is compared (the angle
        between the identical orientations q and -q is calculated correctly).
        @param: goal       A list of floats, a Pose or a PoseStamped
        @param: actual     A list of floats, a Pose or a PoseStamped
        @param: tolerance  A float
        @returns: bool
        """
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
        joint_goal[0] = 1
        joint_goal[1] = 25 / 180 * pi 
        joint_goal[2] = 56 /180 * pi 
        joint_goal[3] = 0
        joint_goal[4] = -70 / 180 * pi 
        joint_goal[5] = 0 / 180 * pi 
       

        move_group.go(joint_goal, wait=True)
        move_group.stop()


    def go_to_pose_goal(self):
        # Copy class variables to local variables to make the web tutorials more clear.
        # In practice, you should use the class variables directly unless you have a good
        # reason not to.
        move_group = self.move_group

        ## BEGIN_SUB_TUTORIAL plan_to_pose
        ##
        ## Planning to a Pose Goal
        ## ^^^^^^^^^^^^^^^^^^^^^^^
        ## We can plan a motion for this group to a desired pose for the
        ## end-effector:
        pose_goal = geometry_msgs.msg.Pose()
        pose_goal.orientation.w = 1.0
        pose_goal.position.x = 0.4
        pose_goal.position.y = 0.1
        pose_goal.position.z = 0.4

        move_group.set_pose_target(pose_goal)

        ## Now, we call the planner to compute the plan and execute it.
        # `go()` returns a boolean indicating whether the planning and execution was successful.
        success = move_group.go(wait=True)
        # Calling `stop()` ensures that there is no residual movement
        move_group.stop()
        # It is always good to clear your targets after planning with poses.
        # Note: there is no equivalent function for clear_joint_value_targets().
        move_group.clear_pose_targets()

        ## END_SUB_TUTORIAL

        # For testing:
        # Note that since this section of code will not be included in the tutorials
        # we use the class variable rather than the copied state variable
        current_pose = self.move_group.get_current_pose().pose
        return all_close(pose_goal, current_pose, 0.01)

    def plan_cartesian_path(self, scale=1):

        move_group = self.move_group

        waypoints = []

        # wpose = move_group.get_current_pose().pose
        # wpose.position.z -= scale * 0.1  # First move up (z)


        # wpose.position.y += scale * 0.10  # and sideways (y)
        # waypoints.append(copy.deepcopy(wpose))

        # wpose.position.x += scale * 0.1 # Second move forward/backwards in (x)
        # waypoints.append(copy.deepcopy(wpose))

        # wpose.position.y -= scale * 0.1  # Third move sideways (y)
        # waypoints.append(copy.deepcopy(wpose))

        



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


        # We want the Cartesian path to be interpolated at a resolution of 1 cm
        # which is why we will specify 0.01 as the eef_step in Cartesian
        # translation.  We will disable the jump threshold by setting it to 0.0,
        # ignoring the check for infeasible jumps in joint space, which is sufficient
        # for this tutorial.
        (plan, fraction) = move_group.compute_cartesian_path(
            waypoints, 0.1, 0.0  # waypoints to follow  # eef_step
        )  # jump_threshold

        # Note: We are just planning, not asking move_group to actually move the robot yet:


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

        # now = rospy.Time.now()
        # self.tl.waitForTransform('base_link', 'link6', now ,rospy.Duration(1) )

         

        

        # transformed_pose = transform_pose(my_pose, 'base_link', 'link6')

  

        # move_group = self.move_group     
 
        # currPose = move_group.get_current_pose()

        # offsetPose = Pose()
        # offsetPose.position.x = 0
        # offsetPose.position.y = 0
        # offsetPose.position.z = .01
      


        # EEName = move_group.get_end_effector_link()

        # tfBuffer = tf2_ros.Buffer()
        # poseout = PoseStamped()
        # poseout2 = PoseStamped()
        # poseout.header.stamp = rospy.Time(0)
 
        # poseout2 = tfBuffer.transform(currPose.pose, EEName)

        
        # now = rospy.Time.now()


        
        # self.tl.waitForTransform('base_link', EEName, now )

        # poseEE = self.tl.transformPose(EEName, currPose)

        # tl.transform()

        # currPose2.pose.position.x += poseEE.pose.position.x 
        # currPose2.pose.position.y += poseEE.pose.position.y 
        # currPose2.pose.position.z += poseEE.pose.position.z 


        # #currPose2.pose.position.z += 0.01 
        # move_group.get_
        # move_group.set_pose_target(currPose2)
   
        # move_group.go()

