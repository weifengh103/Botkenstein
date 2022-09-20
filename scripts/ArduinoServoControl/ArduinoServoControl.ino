#include "ros.h"
#include "Wire.h"
#include "HCPCA9685.h"
#define  I2CAdd 0x40


/* Create an instance of the library */
HCPCA9685 HCPCA9685(I2CAdd);


void setup()
{
  /* Initialise the library and set it to 'servo mode' */
  HCPCA9685.Init(SERVO_MODE);

  /* Wake the device up */
  HCPCA9685.Sleep(false);

  Serial.begin(9600);

//  MoveJ1(90);
  MoveJ2(90);
//  MoveJ3(90);
//  MoveJ4(90);
//  MoveJ5(90);
//  MoveJ6(90);
}


void loop()
{
 int index;
 int moveAngle = 10;
 MoveJ1( 90);
MoveJ2( 90);
//while (true)
//{
//  MoveJ2( 95);
//
//delay(1000);
//MoveJ2( 85);
//
//delay(1000);
//  }


  for (index = -moveAngle; index < moveAngle; index++)
  {
  Serial.print(index);
   MoveJ1(90 + index);
    MoveJ2(120 + index);
     MoveJ3(90 + index);
   MoveJ4(90 + index);
    MoveJ5(90 + index);
    MoveJ6(90 + index);
    delay(40);
  }
  delay(5000);

  for (index = moveAngle; index > -moveAngle; index--)
  {
       MoveJ1(90 + index);
    MoveJ2(120 + index);
    MoveJ3(90 + index);
      MoveJ4(90 + index);
       MoveJ5(90 + index);
    MoveJ6(90 + index);
    delay(40);
  }

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
