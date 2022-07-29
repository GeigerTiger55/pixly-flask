from PIL import Image
import io

def convert_to_BW(image_object):
    """ Converts image from color to black & white
    - Takes an image object
    - Returns a file object """
    image = Image.open(image_object)
    image = image.convert("L")
    b = io.BytesIO()
    image.save(b, "JPEG")
    # image.show()
    b.seek(0)
    return b



# FIXME: needs to be fixed to get sepia to work
# def convert_to_Sepia(image_path):
#     img = Image.open(image_path)
#     width, height = img.size

#     pixels = img.load() # create the pixel map

#     for py in range(height):
#         for px in range(width):
#             r, g, b = img.getpixel((px, py))

#             tr = int(0.393 * r + 0.769 * g + 0.189 * b)
#             tg = int(0.349 * r + 0.686 * g + 0.168 * b)
#             tb = int(0.272 * r + 0.534 * g + 0.131 * b)

#             if tr > 255:
#                 tr = 255

#             if tg > 255:
#                 tg = 255

#             if tb > 255:
#                 tb = 255

#             pixels[px, py] = (tr,tg,tb)

#     return img