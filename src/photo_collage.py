import torch
import torchvision.transforms as transforms
from PIL import Image, ImageOps
import os
import random
from concurrent.futures import ThreadPoolExecutor

device = torch.device('cuda' if torch.cuda.is_available(
) else 'mps' if torch.backends.mps.is_available() else 'cpu')

print(f"Using device: {device}")


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

    transform = transforms.Compose([
        transforms.Resize((slot_size, slot_size)),
        transforms.ToTensor()
    ])

    image = transform(image).to(device)
    image = transforms.ToPILImage()(image.cpu())
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

    for idx, image in enumerate(images):
        x = (idx % number) * slot_size
        y = (idx // number) * slot_size
        collage.paste(image, (x, y))

    return collage
