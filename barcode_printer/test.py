from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont

# Your barcode data
barcode_data = "123456789"

# Generate the barcode
barcode = Code128(barcode_data, writer=ImageWriter())
barcode_image = barcode.render()

# Convert the barcode image to a Pillow Image object
barcode_pil_image = Image.open(barcode_image)

# Create a blank image to paste the barcode onto


# Define the position to paste the barcode onto the background
barcode_position = (50, 50)

# Paste the barcode onto the background
background_image.paste(barcode_pil_image, barcode_position)

# Create a drawing object
draw = ImageDraw.Draw(background_image)

# Choose a font (you'll need to provide the path to a TTF font file)
font_path = "consola.ttf"
font_size = 24
font = ImageFont.truetype(font_path, size=font_size)

# Specify the text to be added
text = "Barcode: {}".format(barcode_data)

# Add the text to the image
text_position = (50, 150)
draw.text(text_position, text, font=font, fill="black")

# Save or display the modified image
background_image.save("output_with_text.png")
background_image.show()
