import requests
import base64
import img2pdf
from html2image import Html2Image

# URL запиту до API для отримання етикетки
label_endpoint = f"https://api.dpd.co.uk/shipping/shipment/1126684719/label/"

# Заголовки для запиту
label_headers = {
    "Accept": "text/html",
    "GeoSession": "f8a29d27-c2c6-4c11-afda-9177fcb22290",
    "GeoClient": "account/118990"
}

# Виконуємо запит
response = requests.get(label_endpoint, headers=label_headers)
response_text = response.text

htmlimg = Html2Image()
htmlimg.screenshot(html_str=response_text, save_as='label.png')


image_path = 'label.png'
try:
    with open(image_path, 'rb') as img_file:
        img_data = img_file.read()
except FileNotFoundError:
    print(f"Помилка: файл '{image_path}' не знайдено.")
    exit()


LabelAsBase64 = base64.b64encode(img_data).decode('utf-8')


pdf_path = 'label.pdf'
with open(pdf_path, 'wb') as pdf_file:
    pdf_file.write(img2pdf.convert(img_data))


with open(pdf_path, 'rb') as pdf_file:
    pdf_data = pdf_file.read()

CustomsPDFDocumentAsBase64 = base64.b64encode(pdf_data).decode('utf-8')




