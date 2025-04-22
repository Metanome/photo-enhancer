from PIL import Image, ImageEnhance, ImageFilter

def enhance_image(input_path, output_path, brightness=2.5, contrast=1.0, sharpness=1.0):
    image = Image.open(input_path)

    # Brightness enhancement
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness)

    # Contrast enhancement
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast)

    # Sharpness enhancement
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(sharpness)

    # Denoise
    image = image.filter(ImageFilter.MedianFilter(size=3))

    # Save enhanced image
    image.save(output_path)
