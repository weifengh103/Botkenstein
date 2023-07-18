
import RPi.GPIO as GPIO
import time



class AGV:
    
    # Left Motor Pins
    _lPWMPin = 31
    _lStatusPin1 = 33
    _lStatusPin2 = 35

    # Right Motor Pins
    _rPWMPin = 32
    _rStatusPin1 = 34
    _rStatusPin2= 36

    # Speed
    _currSpeed = 255/2

    def init(self):
        # output_pin = 32
        # Pin Setup:
        # Board pin-numbering scheme
        GPIO.setmode(GPIO.BOARD)
        # set pin as an output pin with optional initial state of HIGH
        GPIO.setup(self._lPWMPin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._lStatusPin1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._lStatusPin2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._rPWMPin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._rStatusPin1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._rStatusPin2, GPIO.OUT, initial=GPIO.LOW)

    def getCMD(self,CMD):
        print(CMD)

    def _setSpeed(self):
        GPIO.gpio(self._lPWMPin,self._currSpeed)
        GPIO.gpio(self._rPWMPin,self._currSpeed)

    def forward(self):
        # self.setSpeed()
        GPIO.output(self._lStatusPin1,GPIO.HIGH)
        GPIO.output(self._lStatusPin1,GPIO.LOW)

        GPIO.output(self._rStatusPin1,GPIO.HIGH)
        GPIO.output(self._rStatusPin1,GPIO.LOW)

    def backward(self):
        # self.setSpeed()
        GPIO.output(self._lStatusPin1,GPIO.HIGH)
        GPIO.output(self._lStatusPin1,GPIO.LOW)

        GPIO.output(self._rStatusPin1,GPIO.HIGH)
        GPIO.output(self._rStatusPin1,GPIO.LOW)

    def turnLeft(self):
        # self.setSpeed()
        GPIO.output(self._lStatusPin1,GPIO.HIGH)
        GPIO.output(self._lStatusPin1,GPIO.LOW)

        GPIO.output(self._rStatusPin1,GPIO.HIGH)
        GPIO.output(self._rStatusPin1,GPIO.LOW)  

    def turnRight(self):
        # self.setSpeed()
        GPIO.output(self._lStatusPin1,GPIO.HIGH)
        GPIO.output(self._lStatusPin1,GPIO.LOW)

        GPIO.output(self._rStatusPin1,GPIO.HIGH)
        GPIO.output(self._rStatusPin1,GPIO.LOW) 

    def stop(self):
        # self.setSpeed()
        GPIO.output(self._lStatusPin1,GPIO.LOW)
        GPIO.output(self._lStatusPin1,GPIO.LOW)

        GPIO.output(self._rStatusPin1,GPIO.LOW)
        GPIO.output(self._rStatusPin1,GPIO.LOW)


    def test(self):
        p = GPIO.PWM(self._rPWMPin, 100)
        val = 25
        incr = 5
        p.start(val)

        print("PWM running. PrLeftess CTRL+C to exit.")
        try:
            while True:
                time.sleep(0.25)
                if val >= 100:
                    incr = -incr
                if val <= 20:
                    incr = -incr
                val += incr
                p.ChangeDutyCycle(val)
        finally:
            p.stop()
            GPIO.cleanup()




    # if __name__ == '__main__':
    #     init()