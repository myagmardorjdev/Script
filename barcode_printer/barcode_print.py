from PIL import Image, ImageDraw, ImageFont
from barcode import Code128
from flask import *
from io import BytesIO
import io
from barcode.writer import ImageWriter

def generate_white_png_with_text(width_mm, height_mm, output_file, text_content,barcode_data,barcode_text,price):
    # Convert mm to pixels (assuming 1mm = 3.77953 pixels)
    width_pixels = int(width_mm * 3.77953)
    height_pixels = int(height_mm * 3.77953)
    image_path = "C:/Users/myagmardorj/Git/lesson3/barcode_printer/sansar.png"
    additional_image = Image.open(image_path)
    additional_image = additional_image.resize((220,50))
    additional_image_position = ( 0, 68)

    # Create a new white image
    image = Image.new("RGB", (width_pixels, height_pixels), "white")

    # Create a drawing object
    draw = ImageDraw.Draw(image)

        # Specify the text content and font
    text_content = text_content
    font_size1 = 24
    font_family = "verdana.ttf"
    font = ImageFont.truetype(font_family, size=font_size1)  # You can use a different font

    # Specify the position to place the text (adjust as needed)
    text_position = (10, 2) # дээрээсээ 2 pixels

    # Add text to the image
    draw.text(text_position, text_content, fill="black", font=font)
    font_size2 = 16
    font = ImageFont.truetype(font_family, size=font_size2) 

    text_position = (10,7+font_size1)
    draw.text(text_position, price, fill="black", font=font)
    # Create a BytesIO object to store the barcode image data
    font_size = 16
    font = ImageFont.truetype(font_family, size=font_size) 

    text_position = (10,30+font_size)
    draw.text(text_position, barcode_text, fill="black", font=font)


    barcode_stream = BytesIO()

    # Generate an EAN-13 barcode and write it to the BytesIO object
    Code128(barcode_data, writer=ImageWriter()).write(barcode_stream)

    # Open the generated barcode image using Pillow

    barcode_image = Image.open(barcode_stream)
    barcode_image = barcode_image.resize((260,80))
    barcode_position = (-15,120)
    # Paste the barcode onto the image
    image.paste(barcode_image, barcode_position)

    image.paste(additional_image, additional_image_position)
    # Save the image to a PNG file
    #image.save(output_file, "PNG")

    return image

if __name__ == "__main__":
    # Set the dimensions, output file name, and text content
    width_mm = 60   
    height_mm = 45
    output_file = "output_with_text.png"
    text_content = "Бэлэг 10500"
    barcode_text = "Barcode: 12510500"
    barcode = "12510500"
    price = "Үнэ: 10500"

    # Generate the white PNG image with text
    generate_white_png_with_text(width_mm, height_mm, output_file, text_content,barcode,barcode_text,price)

    print(f"White PNG image with text generated: {output_file}")
