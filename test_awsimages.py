"""awsimages api tests"""

import os
from unittest import TestCase

import imageio as iio
from awsimages import upload_file_to_s3
from PIL import Image
 
# read an image
img = open(r"test_image.jpg", 'rb')
# img = Image.open('test_image.jpg')
class AwsimageTestCase(TestCase):
    def setUp(self):
        # TODO: do we need to do anything here?
        print('start', img)

    def tearDown(self):
        # TODO: delete file from aws
        print('done')

    def test_add_image(self):
        print('image', img)
        output = upload_file_to_s3(img)
        print('output',output)
        # self.assertIsInstance( output, str)