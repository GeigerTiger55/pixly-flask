from PIL import Image


def convert_to_BW(imagepath):
    image = Image.open(imagepath)
    return image.convert("L")


