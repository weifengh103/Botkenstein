
import RPi.GPIO as GPIO
import time


#  /opt/nvidia/jetson-io/jetson-io.py
class AGV:
    
    # Left Motor Pins
    _lPWMPin = 33
    _lStatusPin1 = 35
    _lStatusPin2 = 37

    # Right Motor Pins
    # _rPWMPin = 15
    _rPWMPin = 32
    _rStatusPin1 = 36
    _rStatusPin2= 38

    # Speed
    _currSpeed = 50

    
    
 

    def init(self):
        GPIO.cleanup() 
        # output_pin = 32
        # Pin Setup:
        # Board pin-numbering scheme
        GPIO.setmode(GPIO.BOARD)
        # set pin as an output pin with optional initial state of HIGH
        GPIO.setup(self._lStatusPin1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._lStatusPin2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._rStatusPin1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._rStatusPin2, GPIO.OUT, initial=GPIO.LOW)

        self._lPWM = GPIO.PWM(self._lPWMPin, 100)
        self._rPWM = GPIO.PWM(self._rPWMPin, 100)

        self._lPWM.ChangeDutyCycle(self._currSpeed)
        self._rPWM.ChangeDutyCycle(self._currSpeed)

        self._lPWM.start(self._currSpeed)
        self._rPWM.start(self._currSpeed)
        

    def getCMD(self,CMD):
        print(CMD)

    def _setSpeed(self,speed):
        # speed = speed/100*255
        self._lPWM.ChangeDutyCycle(speed)
        self._rPWM.ChangeDutyCycle(speed)

    def forward(self):
        GPIO.output(self._lStatusPin1,GPIO.HIGH)
        GPIO.output(self._lStatusPin2,GPIO.LOW)

        GPIO.output(self._rStatusPin1,GPIO.HIGH)
        GPIO.output(self._rStatusPin2,GPIO.LOW)

    def backward(self):
        GPIO.output(self._lStatusPin1,GPIO.LOW)
        GPIO.output(self._lStatusPin2,GPIO.HIGH)

        GPIO.output(self._rStatusPin1,GPIO.LOW)
        GPIO.output(self._rStatusPin2,GPIO.HIGH)

    def turnLeft(self):
        GPIO.output(self._lStatusPin1,GPIO.LOW)
        GPIO.output(self._lStatusPin2,GPIO.HIGH)

        GPIO.output(self._rStatusPin1,GPIO.HIGH)
        GPIO.output(self._rStatusPin2,GPIO.LOW)  

    def turnRight(self):
        GPIO.output(self._lStatusPin1,GPIO.HIGH)
        GPIO.output(self._lStatusPin2,GPIO.LOW)

        GPIO.output(self._rStatusPin1,GPIO.LOW)
        GPIO.output(self._rStatusPin2,GPIO.HIGH) 

    def stop(self):
        GPIO.output(self._lStatusPin1,GPIO.LOW)
        GPIO.output(self._lStatusPin2,GPIO.LOW)

        GPIO.output(self._rStatusPin1,GPIO.LOW)
        GPIO.output(self._rStatusPin2,GPIO.LOW)
    
    def allHigh(self):


        GPIO.output(self._lStatusPin1,GPIO.HIGH)
        GPIO.output(self._lStatusPin1,GPIO.HIGH)

        GPIO.output(self._rStatusPin1,GPIO.HIGH)
        GPIO.output(self._rStatusPin1,GPIO.HIGH)



    def test(self):
        # p = GPIO.PWM(self._rPWMPin, 100)
        val = 25
        incr = 5
        # p.start(val)

        self.forward()

        print("PWM running. PrLeftess CTRL+C to exit.")
        try:
            while True:
                time.sleep(0.25)
                if val >= 100:
                    incr = -incr
                if val <= 20:
                    incr = -incr
                val += incr
                self._lPWM.ChangeDutyCycle(val)
                self._rPWM.ChangeDutyCycle(val)
        finally:
            self.stop()
            GPIO.cleanup()




    # if __name__ == '__main__':
    #     init()


# agv = AGV()
# agv.init()

# agv.test()

# # agv.forward()
# # agv._setSpeed(10)
# # agv._setSpeed(20)
# # agv._setSpeed(50)
# # agv._setSpeed(70)
# # agv._setSpeed(100)
# # agv.backward()
# # agv.turnLeft()
# # agv.turnRight()
# agv.stop()
# GPIO.cleanup()
