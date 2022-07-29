""" AWSimages API tests"""

# FIXME: Tests not working !!

# import os
from unittest import TestCase

# import imageio as iio
from awsimages import upload_file_to_s3
# from PIL import Image

# read an image

class AwsimageTestCase(TestCase):
    def setUp(self):
        # TODO: do we need to do anything here?
        print('start')

    def tearDown(self):
        # TODO: delete file from aws
        print('done')

    def test_add_image(self):
        # FIXME: this is out of date - output is now an object
        # doesn't work
        with open('test_image.jpg', "rb") as data:
            # print('image', img)
            output = upload_file_to_s3(data)
            print('output', output)
            # self.assertIsInstance( output, str)