from PIL import Image, ImageOps

def crop_text_from_image(image_path, output_path):
    # Load the image
    image = Image.open(image_path)

    # Convert to grayscale
    grayscale_image = ImageOps.grayscale(image)

    # Create a binary mask
    threshold = 128
    binary_image = grayscale_image.point(lambda p: p > threshold and 255) 

    # Invert the binary mask to have text in black and background in white
    inverted_binary_image = ImageOps.invert(binary_image)

    # Find the bounding box of the text
    bbox = inverted_binary_image.getbbox()

    if bbox:
        # Crop the image using the bounding box
        cropped_image = image.crop(bbox)

        # Create an alpha mask (same size as the cropped image)
        alpha = Image.new('L', cropped_image.size, 255)
        cropped_gray = ImageOps.grayscale(cropped_image)
        alpha_mask = cropped_gray.point(lambda p: 255 if p < threshold else 0)

        # Add the alpha channel to the cropped image
        cropped_image.putalpha(alpha_mask)

        # Save the resulting image with transparency
        cropped_image.save(output_path, format="PNG")
        print(f"Cropped image with transparent background saved as {output_path}")
    else:
        print("No text found in the image.")

# Example usage
crop_text_from_image('Untitled.png', 'cropped_output.png')