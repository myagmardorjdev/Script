from PIL import Image, ImageDraw, ImageFont
from barcode import Code128
from barcode.writer import ImageWriter

def generate_barcode_with_custom_font_and_margin(barcode_data, output_file, font_path, margin_left):
    # Generate the barcode image using python-barcode
    barcode = Code128(barcode_data, writer=ImageWriter())
    barcode_stream = barcode.render()

    # Create a new Image object from the barcode stream
    barcode_image = Image.open(barcode_stream)

    # Create a drawing object
    draw = ImageDraw.Draw(barcode_image)

    # Load your custom font (replace "path/to/your/font.ttf" with the actual path)
    custom_font = ImageFont.truetype(font_path, size=12)

    # Get the text size to calculate the position
    text_width, text_height = draw.textsize(barcode_data, custom_font)

    # Calculate the position with the left margin
    text_position = (margin_left, barcode_image.height - text_height - 5)

    # Draw the barcode data using the custom font
    draw.text(text_position, barcode_data, font=custom_font, fill="black")

    # Save the final image with the barcode and custom font
    barcode_image.save(output_file, "PNG")

if __name__ == "__main__":
    # Specify the barcode data, output file, font path, and margin left
    barcode_data = "123456789"
    output_file = "output_barcode_with_custom_font_and_margin.png"
    
    # Specify the path to your custom TrueType font file
    font_path = "path/to/your/font.ttf"

    # Set the left margin for the text
    left_margin = 20  # Adjust the margin as needed

    # Generate the barcode with the custom font and left margin
    generate_barcode_with_custom_font_and_margin(barcode_data, output_file, font_path, left_margin)

    print(f"Barcode with custom font and left margin saved to: {output_file}")
