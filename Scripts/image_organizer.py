from PIL import Image
from PIL.ExifTags import TAGS
import os
import os.path

def get_image_data():
    # path to the image or video
    imagename = "C:/Users/JervinJosh/Pictures/Camera Roll/surprisa.jpg"

    # read the image data using PIL
    image = Image.open(imagename)

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
    '''exifdata = image.getexif()'''
    for label,value in info_dict.items():
        print(f"{label:25}: {value}")
    def get_date_taken(path):
        return Image.open(path)._getexif()[36867]

    print(get_date_taken(imagename))

folder_path = "D:/Github/EEE-199/Pictures"
images = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
print(images)