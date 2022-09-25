#if (ARDUINO >= 100)
#include <Arduino.h>
#else
#include <WProgram.h>
#endif
#include <ros.h>
#include <std_msgs/Float64.h>
#include <sensor_msgs/JointState.h>
#include <stdlib.h>

ros::NodeHandle nh;

float angle[6] = {0,0,0,0,0,0};

void cmd_cb(const sensor_msgs::JointState& cmd_arm)
{
  angle[0] = cmd_arm.position[0];
  angle[1] = cmd_arm.position[1];
  angle[2] = cmd_arm.position[2];
  angle[3] = cmd_arm.position[3];
  angle[4] = cmd_arm.position[4];
  angle[5] = cmd_arm.position[5];
 }

std_msgs::Float64 mydata;
ros::Subscriber<sensor_msgs::JointState> sub("/move_group/fake_controller_joint_states", cmd_cb);
ros::Publisher chatter("chatter", &mydata);

void setup()
{
  nh.getHardware()->setBaud(115200);
  nh.initNode();
  nh.subscribe(sub);
  nh.advertise(chatter);
}

void loop()
{
  mydata.data = angle[1];
  chatter.publish( &mydata );
  nh.spinOnce();
  delay(1);
}
