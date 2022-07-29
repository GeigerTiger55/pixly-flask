"""Image model tests."""

# FIXME: Tests not working !!

# run these tests like:
#
#    python -m unittest test_user_model.py

import os
from unittest import TestCase

from models import db, Image

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///pixly_test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


TEST_AWS_IMAGE_URL = "https://pixly-app.s3.us-west-1.amazonaws.com/337d5b411b955a480ef0d5c878f5ecd2.jpeg"

class ImageModelTestCase(TestCase):
    def setUp(self):
        Image.query.delete()

        # FIXME: need to add args below
        image1 = Image(aws_url=TEST_AWS_IMAGE_URL)

        db.session.add(image1)
        db.session.commit()

        self.image1_id=image1.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_image_model(self):
        image1 = Image.query.get(self.image1_id)

        self.assertEqual(image1.aws_url, TEST_AWS_IMAGE_URL)

