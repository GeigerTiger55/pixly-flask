import os
import boto3
import uuid

from dotenv import load_dotenv
load_dotenv()

S3_BUCKET = os.environ['S3_BUCKET_NAME']
S3_KEY = os.environ['AWS_ACCESS_KEY']
S3_SECRET = os.environ['AWS_SECRET_KEY']
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
TEMP_FILE='temp.jpg'

s3 = boto3.client(
   "s3",
   aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET
)

def allowed_file(filename):
    """Check file matches allowed file extensions.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file_to_s3(file, acl="public-read"):
    """ Uploads a file object to AWS,
    - Takes a file object
    - Returns an object {aws_url, aws_filename}

    Docs used for pattern matching: http://boto3.readthedocs.io/en/latest/guide/s3.html
    https://rajrajhans.com/2020/06/2-ways-to-upload-files-to-s3-in-flask/
    https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
    """
    try:
        filename = (f"{uuid.uuid4()}.jpeg")
        # breakpoint()
        s3.upload_fileobj(
            file,
            S3_BUCKET,
            filename,
            ExtraArgs={
                "ACL": acl
            }
        )
    except ValueError as e:
        print("Something Happened: ", e)
        return e
    return {
        'aws_url':("{}{}".format(S3_LOCATION, filename)),
        'aws_filename':filename,
    }



def download_file_from_s3(filename):
    """ Downloads a file object from AWS
    - Takes a filename
    - Returns a file object
    """
    try:
        s3.download_file(S3_BUCKET, filename, TEMP_FILE)
    except Exception as e:
        print("Something Happened: ", e)
        return e
    print('download_file...', TEMP_FILE)
    # TODO: NOTE explain what is temp_file
    return TEMP_FILE