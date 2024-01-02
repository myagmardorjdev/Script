from PIL import Image, ImageDraw, ImageFont
from barcode import Code128
from flask import *
from io import BytesIO
import win32print
from datetime import datetime
import io
from barcode.writer import ImageWriter
def print_image(image_path, printer_name):
    # Open the image using Pillow
    img = Image.open(image_path)

    # Get the printer handle
    printer_handle = win32print.OpenPrinter(printer_name)

    # Get the default printer properties
    default_printer_props = win32print.GetPrinter(printer_handle, 2)

    # Set the printer parameters
    hDevMode, hDevNames, hPrintDC = win32print.DocumentProperties(0, printer_handle, printer_name, default_printer_props[0])

    # Create a new print job
    job_handle = win32print.StartDocPrinter(printer_handle, 1, (image_path, None, "RAW"))

    # Start the print job
    win32print.StartPagePrinter(printer_handle)

    # Print the image
    win32print.WritePrinter(printer_handle, img.tobytes())

    # End the print job
    win32print.EndPagePrinter(printer_handle)
    win32print.EndDocPrinter(printer_handle)

    # Close the printer handle
    win32print.ClosePrinter(printer_handle)
def draw_vertical_line(image, x_position,x_position1,y_position,y_position1, color):
    draw = ImageDraw.Draw(image)
    draw.line((x_position, x_position1, y_position, y_position1), fill=color, width=1)
def generate_white_png_with_text(width_mm, height_mm, output_file, text_content,barcode_data,barcode_text,price,isdate,isSansar,expire):
    # Convert mm to pixels (assuming 1mm = 3.77953 pixels)
    width_pixels = int(width_mm * 3.77953)
    height_pixels = int(height_mm * 3.77953)
    if isSansar == 1:
        image_path = "C:/Users/myagmardorj/Git/lesson3/barcode_printer/sansar.png"
    else:
        image_path = "C:/Users/myagmardorj/Git/lesson3/barcode_printer/carrefour.png"
    additional_image = Image.open(image_path)
    additional_image = additional_image.resize((220,50))
    if width_mm == 60:
        additional_image_position = ( 0, 68)
    else:
        additional_image_position = (55, 100)

    # Create a new white image
    image = Image.new("RGB", (width_pixels, height_pixels), "white")

    # Create a drawing object
    draw = ImageDraw.Draw(image)

        # Specify the text content and font
    text_content = text_content
    if width_mm == 60:
        font_size1 = 20
    else:
        font_size1 = 24
    font_family = "arial.ttf"
    font = ImageFont.truetype(font_family, size=font_size1)  # You can use a different font
    
    # Specify the position to place the text (adjust as needed)
    text_position = (3, 2) # дээрээсээ 2 pixels

    # Add text to the image
    draw.text(text_position, text_content, fill="black", font=font)
    if width_mm == 60:
        font_size2 = 14
    else:
        font_size2 = 16
    font = ImageFont.truetype(font_family, size=font_size2) 

    text_position = (3,7+font_size1)
    draw.text(text_position, price, fill="black", font=font)
    if isdate == 0:
        text_positiondate = (width_pixels/2+width_pixels/7,7+font_size1)
        now = datetime.now()
        draw.text(text_positiondate, str(now.year)+"-"+str(now.month)+"-"+str(now.day),  fill="black", font=font)
    # Create a BytesIO object to store the barcode image data
    if width_mm == 60:
        font_size = 18
    else:
        font_size = 16
    font = ImageFont.truetype(font_family, size=font_size) 

    text_position = (3,33+font_size)
    draw.text(text_position, barcode_text, fill="black", font=font)
    if isdate == 1:
        text_positiondate = (width_pixels/2+width_pixels/7,33+font_size)
        now = datetime.now()
        #draw.text(text_positiondate,"Цаг "+ str(now.hour)+":"+str(now.minute),  fill="black", font=font)

    barcode_stream = BytesIO()
    #expire text
    if width_mm != 60:
        text_position = (3,52+font_size)
        draw.text(text_position,"Хадгалах хоног: "+str(expire), fill="black", font=font)

    Code128(barcode_data, writer=ImageWriter()).write(barcode_stream)

    barcode_image = Image.open(barcode_stream)
    if width_mm == 60:
        barcode_image = barcode_image.resize((260,125))
        barcode_position = (-15,80)
    elif width_mm == 90:
        barcode_image = barcode_image.resize((300,100))
        barcode_position = (17,158)
    elif width_mm == 297:
        barcode_image = barcode_image.resize((300,80))
        barcode_position = (int(height_mm/11),int(height_pixels-height_pixels/7))
    
    # Paste the barcode onto the image
    image.paste(barcode_image, barcode_position)

    #image.paste(additional_image, additional_image_position)
    if width_mm == 60:
        #draw_vertical_line(image, 0,height_mm-(height_mm/4)-4,width_pixels,height_mm-(height_mm/4)-4, "black")
        #draw_vertical_line(image, width_pixels/2+width_pixels/7-4,height_mm-(height_mm/4)-3,width_pixels/2+width_pixels/7-4,height_mm+height_mm/3+4, "black")
        #draw_vertical_line(image, 0,height_mm+height_mm/3+4,width_pixels,height_mm+height_mm/3+4, "black")
        #draw_vertical_line(image, 0,height_mm-(height_mm/4)-3,0,height_mm+height_mm/3+4, "black")
        #draw_vertical_line(image, width_pixels-1,height_mm-(height_mm/4)-3,width_pixels-1,height_mm+height_mm/3+4, "black")
        pass
    elif width_mm == 90:
        draw_vertical_line(image, 0,31,340,31, "black")
        draw_vertical_line(image, 0,85,340,85, "black")
        draw_vertical_line(image, 210,31,210,85, "black")
        draw_vertical_line(image, 0,31,0,85, "black")
        draw_vertical_line(image, 339,31,339,85, "black")
        
    # Save the image to a PNG file
    image.save(output_file, "PNG")

    #return image

if __name__ == "__main__":
    # Set the dimensions, output file name, and text content
    width_mm = 60
    height_mm = 45
    output_file = "output_with_text.png"
    text_content = "Хэлний өнгөр арилгагч"
    barcode_text = "8938500053467"
    barcode = "8938500053467"
    price = ""
    isdate = 1

    # Generate the white PNG image with text
    generate_white_png_with_text(width_mm, height_mm, output_file, text_content,barcode,barcode_text,price,isdate,1,"хугацааа")

    print(f"White PNG image with text generated: {output_file}")