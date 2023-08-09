from flask import Flask, render_template, Response,request
import cv2
from AGV import AGV

from typing import ValuesView
import PySimpleGUI as GUI
import TFListener as tf 
import time

# Initialization

app = Flask(__name__)

poseListener = tf.TFListener()
# servoControl = sc.ServoControl()  
import ServoControl as sc


def generate_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Typsudo snap install chatgpt-desktope: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/video_feed')


def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def AGVControl():
    return render_template('AGVControl.html')


@app.route('/RobotControl')
def RobotControl():
    return render_template('RobotControl.html')


@app.route('/getAGVCMD', methods=['GET','POST'])
def getAGVCMD():
    # return "This is the GET data"
    if request.method == 'GET':
        return "This is the GET data"
    if request.method == 'POST':
        name = request.get_data(as_text=True)
        if name == "RobotTurnLeft":
            agv.turnLeft()
        if name == "RobotTurnRight":
            agv.turnRight()
        if name == "RobotForward":
            agv.forward()
        if name == "RobotBackward":
            agv.backward()
        if name == "RobotStop":
            agv.stop()
        if "Speed" in name:
            speed = name[5:]
            speed = int(speed)
            agv._setSpeed(speed)
        print(name)
        # agv.getCMD(name)

    return "nice"
   

@app.route('/getRobotCMD', methods=['GET','POST'])
def getRobotCMD():
    # return "This is the GET data"
    if request.method == 'GET':
        return "This is the GET data"
    if request.method == 'POST':
        name = request.get_data(as_text=True)
        if name == "btX":
            poseListener.tool_move(0,0.01)
        if name == "btY":
            poseListener.tool_move1(1,0.01)
        if name == "btX":
            poseListener.tool_move(2,0.01)


        
        if name == "btJ1":
            poseListener.offsetJoint(1,step)
        if name == "btJ2":
            poseListener.offsetJoint(2,step)
        if name == "btJ3":
            poseListener.offsetJoint(3,step)
        if name == "btJ4":
            poseListener.offsetJoint(4,step)
        if name == "btJ5":
            poseListener.offsetJoint(5,step)
        if name == "btJ6":
            poseListener.offsetJoint(6,step)
  
        if "Step" in name:
            step = name[5:]
            step = int(step)
           
        print(name)
        # agv.getCMD(name)

    return "nice"
   

 

if __name__ == '__main__':
    agv = AGV()
    agv.init()
    # poseListener.Initialize()


    app.run(host='0.0.0.0', port=5000, debug=True)
    print(1)