app.config['S3_BUCKET'] = "S3_BUCKET_NAME"
app.config['S3_KEY'] = "AWS_ACCESS_KEY"
app.config['S3_SECRET'] = "AWS_ACCESS_SECRET"
app.config['S3_LOCATION'] = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)