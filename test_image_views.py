"""Image View tests."""

# FIXME: Tests not working !!

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py

import os
from unittest import TestCase

from models import Image, db

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///pixly_test"

# Now we can import app

from app import app

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False

class ImageFormViewTestCase(TestCase):
    def showForm(self):
        with self.client as c:
            resp = c.get("/add")
            self.assertIn("<!-- upload form marker -->", str(resp.data))

# TODO: class ImageUploadViewTestCase(TestCase):
#     def uploadImage(self):
#         with self.client as c:
#             resp = c.post("/add", data=)

