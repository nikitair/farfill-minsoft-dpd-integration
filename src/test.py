import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import barcode
from barcode.writer import ImageWriter
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from io import BytesIO

def create_barcode_image(data, barcode_type='code128', writer_options=None):
    options = writer_options if writer_options else {'module_width': 0.21 * mm, 'quiet_zone': 2.5 * mm}
    barcode_class = barcode.get_barcode_class(barcode_type)
    barcode_obj = barcode_class(data, writer=ImageWriter())
    output = BytesIO()
    barcode_obj.write(output, options)
    output.seek(0)
    return output

def create_label(commands, output_filename="created_label.pdf"):
    c = canvas.Canvas(output_filename, pagesize=letter)
    page_width, page_height = letter

    # Отступ сверху страницы
    top_margin = 15 * mm

    for command in commands:
        parts = command.strip().split(',')
        # Пропустить команды, не содержащие достаточного количества параметров
        if len(parts) < 7:
            continue

        x = float(parts[1]) * mm  # Позиция X
        y = page_height - (float(parts[2]) * mm + top_margin)  # Позиция Y с учетом отступа сверху

        if parts[0].startswith('A'):  # Команда для текста
            font_size = int(parts[4]) * 12  # Размер шрифта (умножен для лучшей читаемости)
            text = parts[-1].strip('"')
            c.setFont("Helvetica", font_size)
            c.drawString(x, y, text)
        elif parts[0].startswith('B'):  # Команда для штрихкода
            barcode_data = parts[-1].strip('"').lstrip('%')
            barcode_options = {
                'module_width': 0.495 * mm,
                'module_height': 25.0 * mm,
                'quiet_zone': 6.5 * mm,
                'text_distance': 5.0 * mm
            }
            barcode_image = create_barcode_image(barcode_data, writer_options=barcode_options)
            barcode_image_reader = ImageReader(barcode_image)
            barcode_width = float(parts[5]) * mm
            barcode_height = float(parts[6]) * mm
            c.drawImage(barcode_image_reader, x, y - barcode_height, width=barcode_width, height=barcode_height)

    c.save()


# API call setup
label_endpoint = "https://api.dpd.co.uk/shipping/shipment/1125991484/label/"
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