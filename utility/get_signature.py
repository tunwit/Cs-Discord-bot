from PIL import Image, ImageOps

def crop_text_from_image(image_path, output_path):
    image = Image.open(image_path)

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

        cropped_image.save(output_path, format="PNG")
        print(f"Cropped image with transparent background saved as {output_path}")
    else:
        print("No text found in the image.")
