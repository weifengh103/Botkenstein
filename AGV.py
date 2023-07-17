
# #!/usr/bin/env python

# # Copyright (c) 2019-2022, NVIDIA CORPORATION. All rights reserved.
# # Permission is hereby granted, free of charge, to any person obtaining a
# # copy of this software and associated documentation files (the "Software"),
# # to deal in the Software without restriction, including without limitation
# # the rights to use, copy, modify, merge, publish, distribute, sublicense,
# # and/or sell copies of the Software, and to permit persons to whom the
# # Software is furnished to do so, subject to the following conditions:
# #
# # The above copyright notice and this permission notice shall be included in
# # all copies or substantial portions of the Software.
# #
# # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# # THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# # FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# # DEALINGS IN THE SOFTWARE.

# import RPi.GPIO as GPIO
# import time

# # Pin Definitions
# output_pin = 12  # BCM pin 18, BOARD pin 12

# def main():
#     # Pin Setup:
#     GPIO.setmode(GPIO.BOARD)  # BCM pin-numbering scheme from Raspberry Pi
#     # set pin as an output pin with optional initial state of HIGH
#     GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.HIGH)

#     print("Starting demo now! Press CTRL+C to exit")
#     curr_value = GPIO.HIGH
#     try:
#         while True:
#             time.sleep(1)
#             # Toggle the output every second
#             print("Outputting {} to pin {}".format(curr_value, output_pin))
#             GPIO.output(output_pin, curr_value)
#             curr_value ^= GPIO.HIGH
#     finally:
#         GPIO.cleanup()

# if __name__ == '__main__':
#     main()

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
        self.setSpeed()
        GPIO.output(self._lStatusPin1,GPIO.HIGH)
        GPIO.output(self._lStatusPin1,GPIO.LOW)

        GPIO.output(self._rStatusPin1,GPIO.HIGH)
        GPIO.output(self._rStatusPin1,GPIO.LOW)

    def backward(self):
        self.setSpeed()
        GPIO.output(self._lStatusPin1,GPIO.HIGH)
        GPIO.output(self._lStatusPin1,GPIO.LOW)

        GPIO.output(self._rStatusPin1,GPIO.HIGH)
        GPIO.output(self._rStatusPin1,GPIO.LOW)

    def turnLeft(self):
        self.setSpeed()
        GPIO.output(self._lStatusPin1,GPIO.HIGH)
        GPIO.output(self._lStatusPin1,GPIO.LOW)

        GPIO.output(self._rStatusPin1,GPIO.HIGH)
        GPIO.output(self._rStatusPin1,GPIO.LOW)  

    def turnRight(self):
        self.setSpeed()
        GPIO.output(self._lStatusPin1,GPIO.HIGH)
        GPIO.output(self._lStatusPin1,GPIO.LOW)

        GPIO.output(self._rStatusPin1,GPIO.HIGH)
        GPIO.output(self._rStatusPin1,GPIO.LOW) 

    def stop(self):
        self.setSpeed()
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




    if __name__ == '__main__':
        init()