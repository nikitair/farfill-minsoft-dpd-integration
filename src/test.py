import requests
import base64
import img2pdf
import pdfkit
from pdf2image import convert_from_path
import fitz

label_endpoint = f"https://api.dpd.co.uk/shipping/shipment/1127171565/label/"

# Заголовки для запиту
label_headers = {
    "Accept": "text/html",
    "GeoSession": "1622103f-eba4-4227-af86-3980bc50f3be",
    "GeoClient": "account/118990"
}

# Виконуємо запит
response = requests.get(label_endpoint, headers=label_headers)
response_text = response.text



pdf_file = 'lable.pdf'

# # Options for wkhtmltopdf, you can customize as needed
# options = {
#     'page-size': 'Letter',
#     'margin-top': '0.75in',
#     'margin-right': '0.75in',
#     'margin-bottom': '0.75in',
#     'margin-left': '0.75in',
# }

# # Convert HTML to PDF
# # pdfkit.from_string(response_text, pdf_file, options=options)
# pdfkit.from_string(response_text, pdf_file, options=options, configuration={'path': 'D:\\wkhtmltopdf'})
# with open(pdf_file, 'rb') as pdf_file:
#     pdf_data = pdf_file.read()
    
# CustomsPDFDocumentAsBase64 = base64.b64encode(pdf_data).decode('utf-8')

# images = convert_from_path(pdf_file)
# for i, image in enumerate(images):
#     image.save(f"page_{i+1}.png", "PNG")

# LabelAsBase64 = base64.b64encode(image).decode('utf-8')



# pdf_document = fitz.open(pdf_path)

# # Конвертація кожної сторінки у PNG-зображення
# for page_number in range(len(pdf_document)):
#     # Отримання сторінки
#     page = pdf_document.load_page(page_number)
#     # Конвертація у растрове зображення формату PNG
#     image = page.get_pixmap(alpha=False)
#     # Збереження зображення
#     image.save(f"{output_folder}/page_{page_number + 1}.png")

#     # Закриття PDF-файлу
#     pdf_document.close()


# Path where you want to save the PNG images
output_path = 'images/'

# Convert PDF to PNG images
pages = convert_from_path(pdf_file)

# Save each page as a PNG image
for i, page in enumerate(pages):
    page.save(f"{output_path}page_{i+1}.png", 'PNG')