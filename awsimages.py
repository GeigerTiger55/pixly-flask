import os
import requests
import boto3
from werkzeug.utils import secure_filename


# gives access to env variables
from dotenv import load_dotenv
load_dotenv()

S3_BUCKET = os.environ['S3_BUCKET_NAME']
S3_KEY = os.environ['AWS_ACCESS_KEY']
S3_SECRET = os.environ['AWS_SECRET_KEY']
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)


s3 = boto3.client(
   "s3",
   aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET
)

def upload_file_to_s3(file, acl="public-read"):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    https://rajrajhans.com/2020/06/2-ways-to-upload-files-to-s3-in-flask/
    https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
    """
    try:
        # NOTE: this code broke the upload
        # filename = ''
        # if 'filename' in file:
        #     filename = file.filename
        # else:
        #     filename = file.name
        # breakpoint()
        # print('file.content_type', file.content_type)
        s3.upload_fileobj(
            file,
            S3_BUCKET,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type    #Set appropriate content type as per the file
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e
    return "{}{}".format(S3_LOCATION, file.filename)