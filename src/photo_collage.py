from PIL import Image, ImageOps
import os
import random


def crop_to_square(image):
    width, height = image.size
    size = min(width, height)
    left = (width - size) // 2
    top = (height - size) // 2
    right = (width + size) // 2
    bottom = (height + size) // 2
    return image.crop((left, top, right, bottom))


def create_collage(image_folder, image_size, number):
    collage_size = (number * image_size, number * image_size)
    collage = Image.new('RGB', collage_size)
    slot_size = collage_size[0] // number

    images = []

    for filename in os.listdir(image_folder):
        if filename[0] != '.':
            image_path = os.path.join(image_folder, filename)
            img = Image.open(image_path)
            img = ImageOps.exif_transpose(img)
            img = crop_to_square(img)
            img = img.resize((slot_size, slot_size))
            images.append(img)

    random.shuffle(images)

    count = 0
    for i in range(number):
        for j in range(number):
            collage.paste(images[count], (j * slot_size, i * slot_size))
            count += 1

    return collage
