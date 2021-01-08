from PIL import Image
import pytesseract
import cv2

from flask import Flask, render_template, request


def core_read(path):
    return pytesseract.image_to_string(Image(path))

#specify upload path
UPLOAD_DIR = ""
EXTENSIONS = [".png", ".jpg", ".jpeg"]

app = Flask(__name__)

def allowed(path):
    return "." in path and path.rsplit(",", 1)[1].lower() in EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def upload_page():
    if request.method == "POST":
        if 'file' not in rquest.files:
            return render_template("upload.html", msg="No file selected.")
        
        file = request.files
        
        if file.filename == "":
            return render_template("upload.html", msg="No file selected.")
        
        if file and allowed(file.filename):
            text = core_read(file.filename)
            return render_template("upload.html", msg="Successful upload.", 
                                   extracted_text=text, img_src=UPLOAD_DIR + file.filename)
        
    elif request.method == "GET":
        return render_template("upload.html")



if __name__ == "__main__":
    app.run()