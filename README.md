# pixly-flask

Image lighttable / editor
(Login/authentication isn’t required; any web user can do everything)
Users can view photos stored in the system
<img width="866" alt="Screen Shot 2022-08-22 at 7 07 49 PM" src="https://user-images.githubusercontent.com/728518/186053247-167e7cce-c436-4704-94cc-80e78e28277a.png">


Users can add a JPG photo using an upload form and picking a file on their computer. File is stored on AWS
<img width="784" alt="Screen Shot 2022-08-22 at 7 11 11 PM" src="https://user-images.githubusercontent.com/728518/186053568-49d29fa5-f02e-4d2d-82ce-1bd6629003d4.png">


System retrieves metadata from the photo (location of photo, model of camera, etc) and stores it into the database




Images themselves are stored to Amazon S3, not in the database (you’ll get to practice using AWS!)
Users can search image data from the EXIF fields (you can learn about PostgreSQL full-text search)
Users can perform simple image edits (for example): - turning color photos into B&W - adding sepia tones - reducing the size of the image - adding a border around the image

