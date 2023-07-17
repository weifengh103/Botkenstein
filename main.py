from flask import Flask, render_template, request, Response
import cv2

app = Flask(__name__)
video_capture = cv2.VideoCapture(0)  # Use the default camera (change if needed)

def generate_frames():
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/')
# def index():
#     return render_template('cam.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    # return render_template('cam.html')
    return render_template('index.html')

@app.route('/get_data', methods=['GET','POST'])
def get_data():
    # return "This is the GET data"
    if request.method == 'GET':
        return "This is the GET data"
    if request.method == 'POST':
        name = request.form['name']
   

    return "Saved data: " + name


@app.route('/get_data', methods=['GET','POST'])
def get_data():
    # return "This is the GET data"
    if request.method == 'GET':
        return "This is the GET data"
    if request.method == 'POST':
        name = request.form['name']
   

    return "Saved data: " + name

@app.route('/save_data', methods=['POST'])
def save_data():
    name = request.form['name']
    return "Saved data: " + name

if __name__ == '__main__':
    app.run(debug=True)








# from flask import Flask, render_template, request

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/get_data', methods=['GET','POST'])
# def get_data():
#     # return "This is the GET data"
#     if request.method == 'GET':
#         return "This is the GET data"
#     if request.method == 'POST':
#         name = request.form['name']
#     return "Saved data: " + name



# @app.route('/save_data', methods=['POST'])
# def save_data():
#     name = request.form['name']
#     return "Saved data: " + name

# if __name__ == '__main__':
#     app.run(debug=True)


















# import threading
# import time
# from flask import Flask, render_template, jsonify

# app = Flask(__name__)

# variable = "Hello, World!"
# variable2 = ""
# lock = threading.Lock()

# def update_variable():
#     global variable
#     global variable2
#     while True:
#         with lock:
#             variable = "Updated: " + time.ctime()
#             print(variable2)
#         time.sleep(1)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/get_variable', methods=['GET'])
# def get_variable():
#     with lock:
#         return jsonify(variable)
    
# @app.route('/poet_variable', methods=['POST'])
# def pose_variable():
#     with lock:
#         return jsonify(variable2)

# if __name__ == '__main__':
#     thread = threading.Thread(target=update_variable)
#     thread.daemon = True
#     thread.start()
#     app.run(debug=True)
