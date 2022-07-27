"""Flask app """

from flask import Flask, request, redirect, render_template
# jsonify

from forms import (UploadImageForm)

import os



from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.config['S3_BUCKET'] = os.environ['S3_BUCKET_NAME']
app.config['S3_KEY'] = os.environ['AWS_ACCESS_KEY']
app.config['S3_SECRET'] = os.environ['AWS_SECRET_KEY']
# app.config['S3_LOCATION'] = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY





@app.route("/", methods=["POST"])
def upload_file():
    if "user_file" not in request.files:
        return "No user_file key in request.files"
    file = request.files["user_file"]
    if file.filename == "":
        return "Please select a file"
    if file:
        file.filename = secure_filename(file.filename)
        output = send_to_s3(file, app.config["S3_BUCKET"])
        return str(output)
    else:
        return redirect("/")


@app.get("/add")
def show_upload_form():
    form = UploadImageForm()
    return render_template("/upload.html",form=form)
