from PIL import Image
from PIL.ExifTags import TAGS

def get_exif_data(imagepath):
    image = Image.open(imagepath)
    image_metadata = ''
    info_dict = {
        "Filename": image.filename,
        "Image Size": image.size,
        "Image Height": image.height,
        "Image Width": image.width,
        "Image Format": image.format,
        "Image Mode": image.mode,
        "Image is Animated": getattr(image, "is_animated", False),
        "Frames in Image": getattr(image, "n_frames", 1)
    }

    for label, value in info_dict.items():
        image_metadata += (f"{label:25}: {value}\n")

    exifdata = image.getexif()

    # iterating over all EXIF data fields
    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes
        if isinstance(data, bytes):
            data = data.decode()
        image_metadata += (f"{tag:25}: {data}\n")


    return image_metadata