from flask_wtf import FlaskForm

from wtforms import FileField, StringField

from wtforms.validators import DataRequired

class UploadImageForm(FlaskForm):
    '''Form for uploading image'''

    file = FileField("Image", validators = [DataRequired()])
    author = StringField("Author")
    title = StringField("Image Title")

