# pixly-flask

Image lighttable / editor
(Login/authentication isn’t required; any web user can do everything)
Users can view photos stored in the system
Users can add a JPG photo using an upload form and picking a file on their computer (you’ll need to learn how to allow image uploads!)
System will retrieve metadata from the photo (location of photo, model of camera, etc) and store it into the database (you’ll need to learn how to read the metadata from photos!)
Images themselves are stored to Amazon S3, not in the database (you’ll get to practice using AWS!)
Users can search image data from the EXIF fields (you can learn about PostgreSQL full-text search)
Users can perform simple image edits (for example): - turning color photos into B&W - adding sepia tones - reducing the size of the image - adding a border around the image<img width="866" alt="Screen Shot 2022-08-22 at 7 07 49 PM" src="https://user-images.githubusercontent.com/728518/186053096-cb8942cc-2e93-43f2-9939-9c3af6e19ef2.png">
<img width="866" alt="Screen Shot 2022-08-22 at 7 07 49 PM" src="https://user-images.githubusercontent.com/728518/186053247-167e7cce-c436-4704-94cc-80e78e28277a.png">
