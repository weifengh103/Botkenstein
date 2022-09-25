
#include <ros.h>
#include <std_msgs/Float64.h>

#include <sensor_msgs/JointState.h>
#include <stdlib.h>

#include <LiquidCrystal.h>
#include "Wire.h"
#include "HCPCA9685.h"

#define  I2CAdd 0x40

HCPCA9685 HCPCA9685(I2CAdd);


const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);


ros::NodeHandle nh;
float angle[6] = {0,0,0,0,0,0};
float test = 0;
int firstRun = 1;
void cmd_cb(const sensor_msgs::JointState& cmd_arm)
{

  
    
  test = cmd_arm.position[0];
  angle[0] = cmd_arm.position[0];
  angle[1] = cmd_arm.position[1];
  angle[2] = cmd_arm.position[2];
  angle[3] = cmd_arm.position[3];
  angle[4] = cmd_arm.position[4];
  angle[5] = cmd_arm.position[5];

// MoveJ1(90+angle[0]*180/3.14);
 }

std_msgs::Float64 mydata;

 ros::Subscriber<sensor_msgs::JointState> sub("move_group/fake_controller_joint_states", cmd_cb);
 

void setup()
{
//      HCPCA9685.Init(SERVO_MODE);
//  HCPCA9685.Sleep(false);
 

    // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  
  nh.getHardware()->setBaud(115200);
  nh.initNode();
  nh.subscribe(sub);
     
}



void loop()
{

  mydata.data = angle[1];
  nh.spinOnce();
 
  
   lcd.setCursor(0, 0);
  lcd.print(angle[0]*180/3.14);

  //MoveJ1(90+angle[0]*180/3.14);
//     lcd.setCursor(0, 1);
//  lcd.print(angle[1]*180/3.14);
//     lcd.setCursor(11, 0);
//  lcd.print(angle[2]*180/3.14);
//  
//     lcd.setCursor(0, 1);
//  lcd.print(angle[3]*180/3.14);
//     lcd.setCursor(6, 1);
//  lcd.print(angle[4]*180/3.14);
//     lcd.setCursor(11, 1);
//  lcd.print(angle[5]*180/3.14);
//  
   delay(1);
}


void MoveJ1(int angle)
{
  int ConvertAngle;
  ConvertAngle  = map( angle, 0, 180, 0, 400);
  HCPCA9685.Servo(0, ConvertAngle);
}

void MoveJ2(int angle)
{
  int offset = 90 - angle;
  int angleServo22 = 99 + offset;
  int ConvertAngle21;
  int ConvertAngle22;
 
  ConvertAngle21  = map( angle, 0, 180, 0, 400);
  ConvertAngle22  = map( angleServo22, 0, 180, 0, 400);
 
  HCPCA9685.Servo(1, ConvertAngle21);
  HCPCA9685.Servo(2, ConvertAngle22);
}

void MoveJ3(int angle)
{
  int ConvertAngle;
  ConvertAngle  = map( angle, 0, 180, 0, 400);
  HCPCA9685.Servo(3, ConvertAngle);
}

void MoveJ4(int angle)
{
  int ConvertAngle;
  ConvertAngle  = map( angle, 0, 180, 0, 400);
  HCPCA9685.Servo(4, ConvertAngle);
}

void MoveJ5(int angle)
{
  int ConvertAngle;
  ConvertAngle  = map( angle, 0, 180, 0, 400);
  HCPCA9685.Servo(5, ConvertAngle);
}


void MoveJ6(int angle)
{
  int ConvertAngle;
  ConvertAngle  = map( angle, 0, 180, 0, 400);
  HCPCA9685.Servo(6, ConvertAngle);
}
