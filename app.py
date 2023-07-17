from flask import Flask, render_template, Response,request
import cv2

app = Flask(__name__)

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
def index():
    return render_template('index.html')


@app.route('/getRobotCMD', methods=['GET','POST'])
def getRobotCMD():
    # return "This is the GET data"
    if request.method == 'GET':
        return "This is the GET data"
    if request.method == 'POST':
        name = request.get_data(as_text=True)
        print(name)
    return "nice"
   

 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=True)
    # app.run( debug=True)