from PIL import Image, ImageDraw, ImageFont
from barcode import Code128
from flask import *

from io import BytesIO
from datetime import datetime
import io
from barcode.writer import ImageWriter
def draw_vertical_line(image, x_position,x_position1,y_position,y_position1, color):
    draw = ImageDraw.Draw(image)
    draw.line((x_position, x_position1, y_position, y_position1), fill=color, width=1)
def generate_white_png_with_text(width_mm, height_mm, output_file, text_content,barcode_data,item_name,price,isdate,isSansar,expire,innercode,mainprice,begindate):
    # Convert mm to pixels (assuming 1mm = 3.77953 pixels)
    width_pixels = int(width_mm * 3.77953)
    tugruglogo = "₮"
    top_margin297 = 75
    old_price_tugrug_margin = 67
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
        titlefont = 22
        text_position = (3, 2) # дээрээсээ 2 pixels
        font_family = "arial.ttf"
    elif width_mm == 90:
        titlefont = 24
        text_position = (3, 2) # дээрээсээ 2 pixels
        font_family = "arial.ttf"
    elif width_mm == 297:
        text_position = (20, top_margin297*3.7+20) # дээрээсээ 2 pixels
        titlefont = 35 / 72 *96
        #Grey-Sans-Regular-2
        font_family = "C:/Users/myagmardorj/Git/lesson3/barcode_printer/FontsFree-Net-arial-bold.ttf"
    font = ImageFont.truetype(font_family, size=titlefont)  # You can use a different font


    draw.text(text_position, text_content, fill="black", font=font)
    if width_mm == 60:
        font_size2 = 14
        font = ImageFont.truetype(font_family, size=font_size2) 
        text_position = (3,7+titlefont)
        draw.text(text_position, price, fill="black", font=font)
    elif width_mm == 90:
        font_size2 = 16
        font = ImageFont.truetype(font_family, size=font_size2) 
        text_position = (3,7+titlefont)
        draw.text(text_position, price, fill="black", font=font)
    elif width_mm == 297:
        fontwidth = 44
        taslalwidth = 25
        price = price.replace("Үнэ:","")
        fontlen = (len(price)-1)
        price = "{:,}".format(int(price))
        if fontlen < 7:
            font_size2 = 208 /72*96
        else:
            font_size2 = 180 /72*96
            taslalwidth = -5
        
        draw.text((width_pixels-80,120*3.7), tugruglogo, fill="black", font=(ImageFont.truetype(font_family, size=80 /72*96) ))
        
        font = ImageFont.truetype(font_family, size=font_size2) 
        
        text_position = ((width_pixels-(fontwidth*fontlen*3.7))-taslalwidth*3.7,120*3.7)
        draw.text(text_position, price, fill="black", font=font)

        # ? innercode  дотоод код
   
        fonti = 15/72*96
        fontin = ImageFont.truetype('arial.ttf', size=fonti) 

        draw.text((250,height_pixels-50), str(innercode),fill="black", font=fontin)

        # ? Хуучин үнэ 
        fonto = 35/72*96
        mainprice = "{:,}".format(int(mainprice))
        mainpricelen=len(mainprice)
        fontold = ImageFont.truetype(font_family, size=fonto) 
        print(mainpricelen)
        if price != mainprice:
            draw.text((width_pixels-(30*mainpricelen)+(20 if mainpricelen == 9 else 0) -(10 if mainpricelen==5 else 0),old_price_tugrug_margin*3.7+100), str(mainprice),fill="black", font=fontold)
            draw.text((width_pixels-40,old_price_tugrug_margin*3.7+100), tugruglogo, fill="black", font=(ImageFont.truetype(font_family, size=22 /72*96) ))
        # ? Хямдарлын хувь %
        if mainprice != price:
            pass 


    if isdate == 1:
        now = datetime.now()
        if width_mm == 60:
            # Хэвлэсэн он сар өдөр
            text_positiondate = (width_pixels/2+width_pixels/7,7+titlefont)
            draw.text(text_positiondate, str(now.year)+"-"+str(now.month)+"-"+str(now.day),  fill="black", font=font)
        elif width_mm ==90:
            text_positiondate = (width_pixels/2+width_pixels/7,7+titlefont)
            draw.text(text_positiondate, str(now.year)+"-"+str(now.month)+"-"+str(now.day),  fill="black", font=font)
        elif width_mm == 297:
            text_positiondate = (width_pixels-100,width_pixels-355)
            font_size2 = 11/72*96
            font_family = 'arial.ttf'
            font = ImageFont.truetype(font_family, size=font_size2) 
            draw.text(text_positiondate, str(now.year)+"-"+str(now.month)+"-"+str(now.day),  fill="black", font=font)
            font = ImageFont.truetype(font_family, size=15/72*96) 
            if "x" == begindate:
                draw.text((width_pixels-250,width_pixels-400), begindate.replace("-",".").replace(";","-") + " хүртэл",  fill="white", font=font)
            else:
                draw.text((width_pixels-250,width_pixels-400), begindate.replace("-",".").replace(";","-") + " хүртэл",  fill="black", font=font)   

    # Create a BytesIO object to store the barcode image data
    if width_mm == 60:
        font_size = 14
        font = ImageFont.truetype(font_family, size=font_size) 

        text_position = (3,33+font_size)
        draw.text(text_position, item_name, fill="black", font=font)
    elif width_mm ==90:
        font_size = 16
        font = ImageFont.truetype(font_family, size=font_size) 

        text_position = (3,33+font_size)
        draw.text(text_position, item_name, fill="black", font=font)
    elif width_mm == 297:
        font_size = 16
        font = ImageFont.truetype(font_family, size=font_size) 
    
    if isdate == 1:
        text_positiondate = (width_pixels/2+width_pixels/7,33+font_size)
        now = datetime.now()
        if width_mm == 60:
            draw.text(text_positiondate,"Цаг "+ str(now.hour)+":"+str(now.minute),  fill="black", font=font)
        elif width_mm == 90:
            draw.text(text_positiondate,"Цаг "+ str(now.hour)+":"+str(now.minute),  fill="black", font=font)

    barcode_stream = BytesIO()
    #expire text
    if width_mm == 90:
        text_position = (3,52+font_size)
        draw.text(text_position,"Хадгалах хугацаа: "+str(expire), fill="black", font=font)


    Code128(barcode_data, writer=ImageWriter()).write(barcode_stream)

    barcode_image = Image.open(barcode_stream)
    if width_mm == 60:
        barcode_image = barcode_image.resize((260,80))
        barcode_position = (-15,120)
    elif width_mm == 90:
        barcode_image = barcode_image.resize((300,100))
        barcode_position = (17,158)
    elif width_mm == 297:
        font_path = "C:/Users/myagmardorj/Git/lesson3/barcode_printer/FontsFree-Net-arial-bold.ttf"
        fontb = ImageFont.truetype(font_path, size=11/72 *96)

        
        # Specify the text to be added
        textb = "{}".format(barcode_data)

        # Add the text to the image
        textpositionb = (int(height_mm/11),int(height_pixels-24))
        textpositionback2 = (width_pixels-250+(35 if mainpricelen == 7 else 0)+(70 if mainpricelen == 6 else 0)+(90 if mainpricelen == 5 else 0),int(67*3.7+115))
        background_color = (255,255,255)  # White background
        background_color2 = (0,0,0)  # black background
        barcode_number_background = Image.new("RGB", textpositionb, background_color)
        barcode_number_background2 = Image.new("RGB", textpositionback2, background_color2)
        barcode_number_background2=barcode_number_background2.resize((25*mainpricelen,4))
        barcode_number_background=barcode_number_background.resize((200,50))
        barcode_image = barcode_image.resize((200,80))

        barcode_position = (int(height_mm/11),int(height_pixels-80))
    
 
    image.paste(barcode_image, barcode_position)
    
    if width_mm == 297:
        image.paste(barcode_number_background,textpositionb) # баар код
        if mainprice!=price:
            
            image.paste(barcode_number_background2,textpositionback2) # хуучин үнэ дээр зураас татах
        
        draw.text(textpositionb, textb, font=fontb, fill="black")
    
    if width_mm == 60:
        image.paste(additional_image, additional_image_position)
        draw_vertical_line(image, 0,height_mm-(height_mm/4)-4,width_pixels,height_mm-(height_mm/4)-4, "black")
        draw_vertical_line(image, width_pixels/2+width_pixels/7-4,height_mm-(height_mm/4)-3,width_pixels/2+width_pixels/7-4,height_mm+height_mm/3+4, "black")
        draw_vertical_line(image, 0,height_mm+height_mm/3+4,width_pixels,height_mm+height_mm/3+4, "black")
        draw_vertical_line(image, 0,height_mm-(height_mm/4)-3,0,height_mm+height_mm/3+4, "black")
        draw_vertical_line(image, width_pixels-1,height_mm-(height_mm/4)-3,width_pixels-1,height_mm+height_mm/3+4, "black")
    elif width_mm == 90:
        image.paste(additional_image, additional_image_position)
        draw_vertical_line(image, 0,31,340,31, "black")
        draw_vertical_line(image, 0,85,340,85, "black")
        draw_vertical_line(image, 210,31,210,85, "black")
        draw_vertical_line(image, 0,31,0,85, "black")
        draw_vertical_line(image, 339,31,339,85, "black")

    
    #image.save(output_file, "PNG")

    return image

if __name__ == "__main__":
    # Set the dimensions, output file name, and text content
    width_mm = 297   
    height_mm = 210
    output_file = "output_with_text.png"
    text_content = "Улаан дарс, 13% хагас хуурай 750мл"
    item_name = "Код: 12510500"
    barcode = "4660028338316"
    price = "Үнэ: 733820"
    isdate = 1
    innercode = 107000819
    mainprice = 43700
    extrapricelist = [(None, None, 21600.00, 0.00)]
    # Generate the white PNG image with text
    generate_white_png_with_text(width_mm, height_mm, output_file, text_content,barcode,item_name,price,isdate,1,"2023-12-22",innercode,mainprice,extrapricelist)


    print(f"White PNG image with text generated: {output_file}")

