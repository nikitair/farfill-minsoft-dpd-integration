import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import barcode
from barcode.writer import ImageWriter
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from io import BytesIO

def create_barcode_image(data, barcode_type='code128', writer_options=None):
    options = writer_options if writer_options else {
        'module_width': 0.21 * mm,  # Smallest bar/space in mm
        'quiet_zone': 2.5 * mm      # quiet_zone in mm
    }
    barcode_class = barcode.get_barcode_class(barcode_type)
    barcode_obj = barcode_class(data, writer=ImageWriter())
    output = BytesIO()
    barcode_obj.write(output, options)
    output.seek(0)
    return output


# Define the label creation function
def create_label(commands, output_filename="created_label.pdf"):
    c = canvas.Canvas(output_filename, pagesize=letter)
    page_width, page_height = letter
    top_margin = 15 * mm
    
    # Split the command string into individual commands
    command_lines = commands.split('\n')
    for command in command_lines:
        # Skip empty lines
        if command.strip() == '':
            continue

        parts = command.strip().split(',')
        cmd_type = parts[0]

        if cmd_type.startswith('A'):  # Text command
            x = float(parts[1]) * mm
            y = page_height - (float(parts[2]) * mm + top_margin)
            text = parts[7].strip('"')
            font_size = int(parts[3])
            c.setFont("Helvetica", font_size)
            c.drawString(x, y, text)

        elif cmd_type.startswith('B'):  # Barcode command
            barcode_data = parts[7].strip('"').lstrip('%')
            x = float(parts[1]) * mm
            y = page_height - (float(parts[2]) * mm + top_margin)
            barcode_width = float(parts[5]) * mm
            barcode_height = float(parts[6]) * mm
            # Define barcode options for custom width and height
            barcode_options = {
                'module_width': float(parts[3]) * mm,
                'module_height': barcode_height,
                'quiet_zone': 2.5 * mm,
                'text_distance': 1.0 * mm,
                'font_size': 6,
                'dpi': 300
            }
            barcode_image = create_barcode_image(barcode_data, writer_options=barcode_options)
            c.drawImage(barcode_image, x, y - barcode_height, width=barcode_width, height=barcode_height)
    
    c.showPage()
    c.save()


# API call setup
label_endpoint = "https://api.dpd.co.uk/shipping/shipment/1126224384/label/"
label_headers = {
    "Accept": "text/vnd.eltron-epl",
    "GeoSession": "f8a29d27-c2c6-4c11-afda-9177fcb22290",
    "GeoClient": "account/118990"
}

# Make the API call and retrieve the label commands
response = requests.get(label_endpoint, headers=label_headers)
response_text = response.text

# Run the label creation with the commands fetched from the API
create_label(response_text, "created_label.pdf")