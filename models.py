"""SQLAlchemy model for Pixly."""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Image(db.Model):
    """Image table."""

    __tablename__ = 'images'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    aws_url = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    upload_timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    exif_metadata = db.Column(
        db.Text,
        nullable=True,
    )



def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
