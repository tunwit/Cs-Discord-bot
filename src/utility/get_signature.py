from PIL import Image, ImageOps
import io

def crop_text_from_image(image_path) -> Image:
    image = Image.open(io.BytesIO(image_path))

    grayscale_image = ImageOps.grayscale(image)

    threshold = 128
    binary_image = grayscale_image.point(lambda p: p > threshold and 255) 

    inverted_binary_image = ImageOps.invert(binary_image)

    bbox = inverted_binary_image.getbbox()

    if bbox:
        cropped_image = image.crop(bbox)

        alpha = Image.new('L', cropped_image.size, 255)
        cropped_gray = ImageOps.grayscale(cropped_image)
        alpha_mask = cropped_gray.point(lambda p: 255 if p < threshold else 0)

        cropped_image.putalpha(alpha_mask)
        return cropped_image
    else:
        return None
