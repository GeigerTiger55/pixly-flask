# pixly-flask

View demo here: https://r26-pixly.herokuapp.com/

Image lighttable / editor

Users can view photos stored in the system, upload a JPG, and convert the image to black and white.
<img width="866" alt="Screen Shot 2022-08-22 at 7 07 49 PM" src="https://user-images.githubusercontent.com/728518/186053247-167e7cce-c436-4704-94cc-80e78e28277a.png">


Users can add a JPG photo using an upload form and picking a file on their computer. Image is stored on AWS.
<img width="784" alt="Screen Shot 2022-08-22 at 7 11 11 PM" src="https://user-images.githubusercontent.com/728518/186053568-49d29fa5-f02e-4d2d-82ce-1bd6629003d4.png">


System retrieves metadata from the photo (location of photo, model of camera, etc) and stores it into the database.
Users can search image data from the EXIF fields (using full text search)
<img width="567" alt="Screen Shot 2022-08-22 at 7 16 58 PM" src="https://user-images.githubusercontent.com/728518/186054211-34f15a71-d198-4d32-be77-6f167a7fab40.png">






