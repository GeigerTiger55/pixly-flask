"""Image model tests."""

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

db.create_all()


TEST_AWS_IMAGE_URL = "https://pixly-app.s3.us-west-1.amazonaws.com/337d5b411b955a480ef0d5c878f5ecd2.jpeg"

class ImageModelTestCase(TestCase):
    def setUp(self):
        Image.query.delete()

        image1 = Image(aws_url=TEST_AWS_IMAGE_URL)
        breakpoint()

        db.session.commit()
        self.image1_id=image1.id

        # what does the client do?
        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_image_model(self):
        image1 = Image.query.get(self.image1_id)

        # Image should have 1 data point
        # //TODO: check this
        self.assertEqual(len(image1), 1)


    # #################### Following tests


    # def test_valid_signup(self):
    #     u1 = User.query.get(self.u1_id)

    #     self.assertEqual(u1.username, "u1")
    #     self.assertEqual(u1.email, "u1@email.com")
    #     self.assertNotEqual(u1.password, "password")
    #     # Bcrypt strings should start with $2b$
    #     self.assertTrue(u1.password.startswith("$2b$"))

    # # #################### Authentication Tests

    # def test_valid_authentication(self):
    #     u1 = User.query.get(self.u1_id)

    #     u = User.authenticate("u1", "password")
    #     self.assertEqual(u, u1)

    # def test_invalid_username(self):
    #     self.assertFalse(User.authenticate("bad-username", "password"))

    # def test_wrong_password(self):
    #     self.assertFalse(User.authenticate("u1", "bad-password"))
