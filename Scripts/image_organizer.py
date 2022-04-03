from PIL import Image
from PIL.ExifTags import TAGS
import os
import os.path

def get_image_data(folder_path):
    images = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return images