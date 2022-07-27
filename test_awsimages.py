"""awsimages api tests"""

import os
from unittest import TestCase

import imageio as iio
from awsimages import upload_file_to_s3
 
# read an image
img = open(r"test_image.jpg", 'r')

class AwsimageTestCase(TestCase):
    def setUp(self):
        # TODO: do we need to do anything here?
        print('start name', img.name)

    def tearDown(self):
        # TODO: delete file from aws
        print('done')

    def test_add_image(self):
        output = upload_file_to_s3(img)
        print('output',output)
        self.assertIsInstance( output, str)