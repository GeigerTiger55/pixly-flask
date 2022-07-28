"""Flask app """

from flask import Flask, request, redirect, render_template, g
from forms import (UploadImageForm, CSRFProtection)
from awsimages import upload_file_to_s3
from exifdata import get_exif_data

import os

from werkzeug.utils import secure_filename

from models import db, connect_db, Image
from image_editing import convert_to_BW



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
# db.drop_all()
# db.create_all()


# TODO: move function
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.before_request
def add_csrf_only_form():
    """Add a CSRF-only form so that every route can use it."""

    g.csrf_form = CSRFProtection()

@app.route("/")
def homepage():
    return redirect("/images")


# post request attached to submit button
@app.route("/add", methods=["POST", "GET"])
def upload_image():
    form = UploadImageForm()
    if form.validate_on_submit():
        if "file" not in request.files:
            return "No user_file key in request.files"
        file = request.files["file"]

        print ('request.files',request.files)
        if file.filename == "":
            return "Please select a file"
        if file and allowed_file(file.filename):
            file.filename = secure_filename(file.filename)
            exif_metadata = get_exif_data(file)
            print('*****exif_metadata', exif_metadata)
            file.seek(0)
            aws_location = upload_file_to_s3(file)

            aws_str = str(aws_location)
            new_image = Image(
                aws_url=aws_str,
                author=form.author.data,
                title=form.title.data,
                exif_metadata=exif_metadata
                )
            db.session.add(new_image)
            db.session.commit()

            # gets id from db
            g.image = Image.query.get_or_404(new_image.id)

            return render_template("/edit.html",  image_aws_url=aws_str)
        else:
            return redirect("/")
    else:
        return render_template("/upload.html", form=form)


@app.route("/images", methods=["GET"])
def display_images():
    """Page showing all images, can be filtered.

    Can take a 'q' param in querystring to search EXIF data
    """
    search = request.args.get('q')

    if not search:
        images = Image.query.all()
        # breakpoint()
    else:
        #TODO: update to use Full Text Search
        search = search.replace(" "," | ")
        images = Image.query.filter(Image.__ts_vector__.match(search)).all()
    return render_template("/display_images.html", images=images)


@app.route("/images/<int:image_id>", methods=["GET"])
def display_image_page(image_id):
    """Page showing image and image data.
    """
    image = Image.query.get_or_404(image_id)
    return render_template("/image.html", image=image)


@app.route("/edit/bw", methods=["POST"])
def edit_image():
    edited_image = convert_to_BW(g.image.aws_url)
    # edited_image.show()
    return render_template("/image.html", image=edited_image)
