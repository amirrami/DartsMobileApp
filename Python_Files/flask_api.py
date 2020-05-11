from flask import Flask, send_from_directory, redirect,request
import os
from Main_darts import setBackgroundImage,getScore
app = Flask(__name__)

from gevent.pywsgi import WSGIServer

from PIL import Image

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def main():
    return redirect("https://github.com/gxercavins/image-api/blob/master/README.md", code=302)


# upload selected image and forward to processing page
@app.route("/get_dart_board_image", methods=["POST"])
def get_dartBoard():
    target = os.path.join(APP_ROOT, 'static/images/')

    # retrieve file from html file-picker
    upload = request.files.getlist("datBoard_image")[0]
    print("File name: {}".format(upload.filename))
    filename = upload.filename

    # file support verification
    ext = os.path.splitext(filename)[1]
    if (ext == ".jpg") or (ext == ".png") or (ext == ".bmp"):
        print("File accepted")
    else:
        return False

    # save file
    destination = "/".join([target, filename])
    print("File saved to to:", destination)
    upload.save(destination)


    # forward to processing page
    if setBackgroundImage(destination):
        return "Done"
    else:
        return "Please take another Board Image" 

# upload selected image and forward to processing page
@app.route("/get_dart_score", methods=["POST"])
def get_score():
    target = os.path.join(APP_ROOT, 'static/images/')

    # retrieve file from html file-picker
    upload = request.files.getlist("dart_image")[0]
    print("File name: {}".format(upload.filename))
    filename = upload.filename

    # file support verification
    ext = os.path.splitext(filename)[1]
    if (ext == ".jpg") or (ext == ".png") or (ext == ".bmp"):
        print("File accepted")
    else:
        return False

    # save file
    destination = "/".join([target, filename])
    print("File saved to to:", destination)
    upload.save(destination)

    score , _ = getScore(destination)
    # forward to processing page
    if score is False:
        return "Please take another dart Image"
    else:
        return {"score":score} 

# retrieve file from 'static/images' directory
@app.route('/get_output_image',methods=["GET"])
def send_image():
    return send_from_directory("static/images", "outputImage.jpg")



if __name__ == "__main__":
    http_server = WSGIServer(('192.168.1.15', 5000), app)
    http_server.serve_forever()