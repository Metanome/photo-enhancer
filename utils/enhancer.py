from PIL import Image, ImageEnhance, ImageFilter
import os

def enhance_image(input_path, output_path):
    image = Image.open(input_path)

    # Brightness
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(2.5)

    # Denoise
    image = image.filter(ImageFilter.MedianFilter(size=3))

    # Sharpen
    image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

    # Save enhanced image
    image.save(output_path)
