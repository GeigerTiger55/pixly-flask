"""SQLAlchemy model for Pixly."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, Index
from ts_vector import TSVector

db = SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask app.
    """
    db.app = app
    db.init_app(app)


class Image(db.Model):
    """Image table
    - id: primary key
    - aws_url: full url to link the image
    - aws_filename: filename used to store/retrieve on AWS
    - author: image author name
    - title: image title
    - upload_timestamp: datetime of upload
    - exif_metadata: photo metadata can be searched, formatted like "Brand: Canon"
    - __ts_vector__: used for full text search of title, exif_metadata, author
    - __table_args__: used for full text search
     """

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

    aws_filename = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    author = db.Column(
        db.Text,
        nullable=False,
        default="Anonymous"
    )

    title = db.Column(
        db.Text,
        nullable=False,
        default="Untitled"
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

    __ts_vector__ = db.Column(
        TSVector(),db.Computed(
         "to_tsvector('english', title || ' ' || exif_metadata || ' ' || author)",
         persisted=True)
    )

    __table_args__ = (Index(
        'ix_image___ts_vector__',
          __ts_vector__,
          postgresql_using='gin'),
    )


