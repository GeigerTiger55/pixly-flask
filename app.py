"""Flask app """

import os
from flask import Flask, request, redirect, render_template, g
from werkzeug.utils import secure_filename

from models import db, connect_db, Image
from forms import (SaveImageForm, UploadImageForm, CSRFProtection)
from exifdata import get_exif_data
from awsimages import upload_file_to_s3, download_file_from_s3, allowed_file
from image_editing import convert_to_BW

# gives access to env variables
from dotenv import load_dotenv
load_dotenv()

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


@app.before_request
def add_csrf_only_form():
    """Add a CSRF-only form so that every route can use it."""

    g.csrf_form = CSRFProtection()


@app.route("/")
def homepage():
    """Redirects to images page."""
    return redirect("/images")


# post request attached to submit button
@app.route("/add", methods=["POST", "GET"])
def upload_image():
    """Adds an image:

    Show form if GET. If valid, upload image and redirect to edit page.
    """
    form = UploadImageForm()
    if form.validate_on_submit():
        if "file" not in request.files:
            # TODO: turn into flash message
            return "No user_file key in request.files"
        file = request.files["file"]

        if file.filename == "":
            # TODO: turn into flash message
            return "Please select a file"

        if file and allowed_file(file.filename):
            file.filename = secure_filename(file.filename)
            exif_metadata = get_exif_data(file)
            file.seek(0)
            aws_info = upload_file_to_s3(file)
            new_image = Image(
                aws_url=aws_info['aws_url'],
                aws_filename=aws_info['aws_filename'],
                author=form.author.data,
                title=form.title.data,
                exif_metadata=exif_metadata
                )
            db.session.add(new_image)
            db.session.commit()

            save_form = SaveImageForm()

            return render_template("/edit.html",  
                image_aws_url=aws_info['aws_url'], 
                image=new_image,
                form=save_form,
                bw=False,
                )
        else:
            # TODO: flash message cannot up file type - not allowed file
            return redirect("/")
    else:
        return render_template("/upload.html", form=form)

################### DISPLAY IMAGE ROUTES ##############################3

@app.route("/images", methods=["GET"])
def display_images():
    """Page showing all images, can be filtered.

    Can take a 'q' param in querystring to search EXIF data.
    """
    search = request.args.get('q')

    if not search:
        images = Image.query.all()
    else:
        search = search.replace(" "," | ")
        images = Image.query.filter(Image.__ts_vector__.match(search)).all()
    return render_template("/display_images.html", images=images)


@app.route("/images/<int:image_id>", methods=["GET"])
def display_image_page(image_id):
    """Page showing image and image data.
    """
    image = Image.query.get_or_404(image_id)
    return render_template("/image.html", image=image)

#################### EDIT/SAVE IMAGE ROUTES #########################

@app.route("/edit/bw/<int:image_id>", methods=["POST"])
def edit_image(image_id):
    """Make image black & white and upload to S3.
    """
    image = Image.query.get_or_404(image_id)
    image_object = download_file_from_s3(image.aws_filename)
    edited_image_obj = convert_to_BW(image_object)
    temp_image_info = upload_file_to_s3(edited_image_obj)
    # TODO: add black and wite image to database
    # TODO: need to decide what we want to do with image
    # - whether it is undoable or not
    save_form = SaveImageForm()
    return render_template('/edit.html', 
        image_aws_url=temp_image_info['aws_url'],
        image=image,
        bw=True,
        form=save_form,
        )

@app.route("/save/<int:image_id>", methods=["POST"])
def save_image(image_id):
    """Save image and render image display page.

    TODO: add form validation
    """
    form = SaveImageForm()
    image = Image.query.get_or_404(image_id)
    image.aws_url = form.aws_url.data
    db.session.commit()

    return render_template("/image.html", image=image)
