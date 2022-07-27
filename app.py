"""Flask app """

from flask import Flask, request, redirect, render_template
# jsonify

from forms import (UploadImageForm)

import boto3, botocore

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


s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config['S3_KEY'],
   aws_secret_access_key=app.config['S3_SECRET']
)


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


@app.get("/add")
def show_upload_form():
    form = UploadImageForm()
    return render_template("/upload.html",form=form)
