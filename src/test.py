import requests
import pdfkit
from pdf2image import convert_from_path
import base64
import os

label_endpoint = f"https://api.dpd.co.uk/shipping/shipment/1127171565/label/"

# Headers for the request
label_headers = {
    "Accept": "text/html",
    "GeoSession": "1622103f-eba4-4227-af86-3980bc50f3be",
    "GeoClient": "account/118990"
}

# Execute the request
response = requests.get(label_endpoint, headers=label_headers)
response_text = response.text

pdf_file = 'label.pdf'

# Convert HTML to PDF
pdfkit.from_string(response_text, pdf_file)

# Path where you want to save the PNG images
output_path = ''

# Convert PDF to PNG images
pages = convert_from_path(pdf_file)

# Save each page as a PNG image
for i, page in enumerate(pages):
    page.save(os.path.join(output_path, f"page_{i+1}.png"), 'PNG')

# Convert PDF to Base64
with open(pdf_file, 'rb') as f:
    pdf_data = f.read()

CustomsPDFDocumentAsBase64 = base64.b64encode(pdf_data).decode('utf-8')
print(f"CustomsPDFDocumentAsBase64: {CustomsPDFDocumentAsBase64}")

# Convert PNG to Base64
with open(os.path.join(output_path, 'page_1.png'), 'rb') as f:
    png_data = f.read()

LabelAsBase64 = base64.b64encode(png_data).decode('utf-8')
print(f"LabelAsBase64: {LabelAsBase64}")
