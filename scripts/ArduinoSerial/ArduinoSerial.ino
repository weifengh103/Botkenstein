#include <LiquidCrystal.h>
#include "Wire.h"
#include "HCPCA9685.h"
#define  I2CAdd 0x40

//Init Motor
HCPCA9685 HCPCA9685(I2CAdd);

//Init LCD
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

//Init string array
String str;
String strs[6];

float j1;
float j2;
float j3;
float j4;
float j5;
float j6; 

void setup() 
{
  
  Serial.begin(115200);
  delay(200);
  Serial.setTimeout(1);

  HCPCA9685.Init(SERVO_MODE);
  HCPCA9685.Sleep(false);
 

  
  lcd.begin(16, 2);
}

void loop() 
{
  while (!Serial.available());
  
  str = Serial.readString();
 // Serial.println(str);
  int StringCount = 0;
  while (str.length() > 0)
  {
    int index = str.indexOf(',');
    if (index == -1) // No space found
    {
      strs[StringCount++] = str;
      break;
    }
    else
    {
      strs[StringCount++] = str.substring(0, index);
      str = str.substring(index+1);
    }
  }

  // Show the resulting substrings
//  for (int i = 0; i < StringCount; i++)
//  {
//    Serial.print(i);
//    Serial.print(": \"");
//    Serial.print(strs[i]);
//    Serial.println("\"");
//  }


  j1 = strs[0].toFloat();
  j2 = strs[1].toFloat();
  j3 = strs[2].toFloat();
  j4 = strs[3].toFloat();
  j5 = strs[4].toFloat();
  j6 = strs[5].toFloat();
  
  lcd.setCursor(0, 0);
  lcd.print(j1);
  
  MoveJ1(90+j1);
  MoveJ2(120+j2);
  MoveJ3(90+j3);
  MoveJ4(90+j4);
  MoveJ5(40+j5);
  MoveJ6(90+j6);
  delay(100); 
  
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
