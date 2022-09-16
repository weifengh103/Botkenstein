import RobotControl
import rospy

def main():
    try:

      
        tutorial = RobotControl.RobotControl()

        
    
 

        tutorial.go_to_joint_state()

        #print("============ Press `Enter` to plan and display a Cartesian path ...")

        #cartesian_plan, fraction = tutorial.plan_cartesian_path()
        
       # print(
        #    "============ Press `Enter` to display a saved trajectory (this will replay the Cartesian path)  ..."
        #)
        #tutorial.display_trajectory(cartesian_plan)

       # print("============ Press `Enter` to execute a saved path ...")
       # tutorial.execute_plan(cartesian_plan)
        #intput("============ Press `Enter` to execute a saved path ...")
        tutorial.tool_move()
    
        
        input("============ Python tutorial demo complete!")
    except rospy.ROSInterruptException:
        return
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
