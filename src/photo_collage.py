from PIL import Image, ImageOps
import os
import random
from concurrent.futures import ThreadPoolExecutor


def crop_to_square(image):
    width, height = image.size
    size = min(width, height)
    left = (width - size) // 2
    top = (height - size) // 2
    right = (width + size) // 2
    bottom = (height + size) // 2
    return image.crop((left, top, right, bottom))


def load_and_process_image(image_path, slot_size):
    image = Image.open(image_path)
    image = ImageOps.exif_transpose(image)
    image = crop_to_square(image)
    image = ImageOps.fit(image, (slot_size, slot_size))
    return image


def create_collage(image_folder, image_size, number):
    collage_size = (number * image_size, number * image_size)
    collage = Image.new('RGB', collage_size)
    slot_size = collage_size[0] // number

    valid_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp")
    image_paths = [
        os.path.join(image_folder, f)
        for f in os.listdir(image_folder)
        if f.lower().endswith(valid_extensions) and not f.startswith('.')
    ]

    random.shuffle(image_paths)

    with ThreadPoolExecutor() as executor:
        images = list(executor.map(lambda p: load_and_process_image(
            p, slot_size), image_paths[:number*number]))

    for i, image in enumerate(images):
        row = i // number
        col = i % number
        collage.paste(image, (col * slot_size, row * slot_size))

    return collage
