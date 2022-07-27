from flask_wtf import FlaskForm

from wtforms import FileField

class UploadImageForm(FlaskForm):
    '''Form for uploading image'''

    file = FileField()
