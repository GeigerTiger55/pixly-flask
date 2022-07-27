"""SQLAlchemy model for Pixly."""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Image(db.Model):
    """Image table."""

    __tablename__ = 'images'

    id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True,
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