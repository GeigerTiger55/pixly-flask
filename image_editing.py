from PIL import Image
import io
from tempfile import TemporaryFile

TEMP_FILE = 'result.jpg'

def convert_to_BW(image_object):
    print('convert_to_BW,imagepath', image_object)
    image = Image.open(image_object)
    fp = TemporaryFile()
    image = image.convert("L")
    b = io.BytesIO()
    image.save(b, "JPEG")
    # image.show()
    b.seek(0)
    return b



