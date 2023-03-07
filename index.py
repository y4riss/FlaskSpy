
from flask import Flask
from flask import request
from flask import render_template
import base64
import numpy as np
import threading
import cv2
from pynput.keyboard import Key, Controller



keyboard = Controller()
app = Flask(__name__)

def update(frame):
    cv2.imshow('stalking :D', frame)
    cv2.waitKey(500)
    cv2.destroyAllWindows()



@app.route('/stream',methods=['POST'])
def stalk():

    # extract base64 encoded string from client
    img_str = request.form.get('frame').split('data:image/png;base64,')[-1]
    
    # convert base64 encoded string into byte string
    img_bytes = base64.b64decode(img_str)

    # convert the byte string into a numpy array
    image = np.frombuffer(img_bytes,np.uint8)

    # convert a numpy array to opencv compatible img
    frame = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # display the fram in  a window
    display_thread = threading.Thread(target=update, args=(frame,))
    display_thread.start()
    return ''

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True,threaded=True)