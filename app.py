"""Flask app """

from flask import Flask, request, redirect, render_template
from forms import (UploadImageForm)
from awsimages import upload_file_to_s3

import os

from werkzeug.utils import secure_filename

from models import (
    db, connect_db, Image
)




# gives access to env variables
from dotenv import load_dotenv
load_dotenv()


# extensions we want to allow
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URL'].replace('postgres://','postgresql://'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

connect_db(app)
db.drop_all()
db.create_all()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
    print ('request.files',request.files)
    if file.filename == "":
        return "Please select a file"
    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        print('what is file???', file)
        aws_location = upload_file_to_s3(file)
        print(aws_location)
        # add file to db
        # new_image = Image(str(aws_location))
        # db.session.add(new_image)
        # db.session.commit()
        return render_template("/sent.html",  image_aws_url=str(aws_location))
    else:
        return redirect("/")

