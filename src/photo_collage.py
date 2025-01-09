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

    valid_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp")
    images = [
        os.path.join(image_folder, f)
        for f in os.listdir(image_folder)
        if f.lower().endswith(valid_extensions) and not f.startswith('.')
    ]

    random.shuffle(images)

    for i, image_path in enumerate(images):
        img = Image.open(image_path)
        img = ImageOps.exif_transpose(img)
        img = crop_to_square(img)
        img = img.resize((slot_size, slot_size))

        row = i // number
        col = i % number
        collage.paste(img, (col * slot_size, row * slot_size))

    return collage
