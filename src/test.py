import requests
import base64
import img2pdf
import pdfkit

# URL запиту до API для отримання етикетки
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

# Options for wkhtmltopdf, you can customize as needed
options = {
    'page-size': 'Letter',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
}

# Convert HTML to PDF
pdfkit.from_string(response_text, pdf_file, options=options)


pdfkit.from_string(response_text, pdf_file, options=options, configuration={'path': 'D:\\wkhtmltopdf'})






# LabelAsBase64 = base64.b64encode(img_data).decode('utf-8')


# pdf_path = 'label.pdf'
# with open(pdf_path, 'wb') as pdf_file:
#     pdf_file.write(img2pdf.convert(img_data))


# with open(pdf_path, 'rb') as pdf_file:
#     pdf_data = pdf_file.read()

# CustomsPDFDocumentAsBase64 = base64.b64encode(pdf_data).decode('utf-8')




