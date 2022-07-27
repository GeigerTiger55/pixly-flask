"""Flask app """

from flask import Flask, request, redirect, render_template

from forms import (UploadImageForm)

import os

from werkzeug.utils import secure_filename


# gives access to env variables
from dotenv import load_dotenv
load_dotenv()


# extensions we want to allow
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.config['S3_BUCKET'] = os.environ['S3_BUCKET_NAME']
app.config['S3_KEY'] = os.environ['AWS_ACCESS_KEY']
app.config['S3_SECRET'] = os.environ['AWS_SECRET_KEY']
app.config['S3_LOCATION'] = 'http://{}.s3.amazonaws.com/'.format(app.config['S3_BUCKET'])

# csrf forms
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


import boto3
s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config['S3_KEY'],
   aws_secret_access_key=app.config['S3_SECRET']
)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file_to_s3(file, bucket_name, acl="public-read"):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type    #Set appropriate content type as per the file
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e
    return "{}{}".format(app.config["S3_LOCATION"], file.filename)



@app.route("/add", methods=["GET"])
def show_upload_form():
    form = UploadImageForm()
    return render_template("/upload.html", form=form)


# post request attached to submit button
@app.route("/add", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No user_file key in request.files"
    file = request.files["file"]
    if file.filename == "":
        return "Please select a file"
    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, app.config["S3_BUCKET"])
        return render_template("/sent.html",  image_aws_url=str(output))
    else:
        return redirect("/")

