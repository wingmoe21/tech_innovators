import io
import os

from google.cloud import vision
from pdf2image import convert_from_path


def process_pdf(uploaded_file):
    images = convert_pdf_to_images(uploaded_file)
    # text_file_path = os.path.join("C:\\Users\\mald2\\OneDrive\\Desktop\\capstone\\tech_innovators\\content\\upload\\uploaded_file.txt")
    # directory = os.path.dirname(text_file_path)
    # os.makedirs(directory, exist_ok=True)
    descriptions =[]
    for image in images:
        description = interpret_image(image)
        descriptions.append(description)
    return descriptions


# Function to convert PDF pages to images
def convert_pdf_to_images(pdf_path):
    return convert_from_path(pdf_path)

# Function to interpret an image
def interpret_image(image_content):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\mald2\\Downloads\\capstone-405521-be463f8a80c5.json"
    # Initialize the Google Vision API client
    client = vision.ImageAnnotatorClient()

    content = io.BytesIO()
    image_content.save(content, format='JPEG')
    content = content.getvalue()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    return response.text_annotations[0].description