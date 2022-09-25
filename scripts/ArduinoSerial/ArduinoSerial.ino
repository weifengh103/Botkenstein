#include <LiquidCrystal.h>
#include "Wire.h"
#include "HCPCA9685.h"
#define  I2CAdd 0x40

HCPCA9685 HCPCA9685(I2CAdd);

const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

float x;

void setup() 
{
  
  Serial.begin(115200);
  Serial.setTimeout(1);

  HCPCA9685.Init(SERVO_MODE);
  HCPCA9685.Sleep(false);
 

  
  lcd.begin(16, 2);
}

void loop() 
{
  while (!Serial.available());
  x = Serial.readString().toFloat();
  
  lcd.setCursor(0, 0);
  lcd.print(x);
  delay(100); 
  MoveJ1(90+x);
  
}

void MoveJ1(int angle)
{
  int ConvertAngle;
  ConvertAngle  = map( angle, 0, 180, 0, 400);
  HCPCA9685.Servo(0, ConvertAngle);
}
