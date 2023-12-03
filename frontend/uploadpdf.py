import base64
import io
import os

import cv2
import fitz
import numpy as np
import requests
import whisperx
from google.cloud import vision
from moviepy.editor import VideoFileClip
from numba import jit
from pdf2image import convert_from_path
from PIL import Image


def process_pdf(uploaded_file):
    unique_slides1 = OCR(uploaded_file)
    pdf_path = save_slides_to_pdf(unique_slides1)
    content1 = whisper(uploaded_file)
    content2 = gpt_photo(pdf_path)
    images = convert_pdf_to_images(pdf_path)
    # text_file_path = os.path.join("C:\\Users\\mald2\\OneDrive\\Desktop\\capstone\\tech_innovators\\content\\upload\\uploaded_file.txt")
    # directory = os.path.dirname(text_file_path)
    # os.makedirs(directory, exist_ok=True)
    content3 =[]
    for image in images:
        description = interpret_image(image)
        content3.append(description)
    # Formatting the merged content
    os.remove("output.pdf")
    return content1, content2, content3

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

@jit(nopython=True)
def are_frames_similar(frame1, frame2, similarity_threshold=0.95):
    mean_x = np.mean(frame1)
    mean_y = np.mean(frame2)
    var_x = np.var(frame1)
    var_y = np.var(frame2)
    covariance = np.mean((frame1 - mean_x) * (frame2 - mean_y))
    c1 = (0.01 * 255) ** 2
    c2 = (0.03 * 255) ** 2
    ssim_index = (2 * mean_x * mean_y + c1) * (2 * covariance + c2) / ((mean_x ** 2 + mean_y ** 2 + c1) * (var_x + var_y + c2))
    return ssim_index > similarity_threshold

def save_slides_to_pdf(unique_slides):
    pdf_path='output.pdf'

    pdf_doc = fitz.open()

    for slide in unique_slides:
        small_slide = slide.resize((int(slide.width * 0.5), int(slide.height * 0.5)))
        img_byte_arr = io.BytesIO()
        small_slide.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        img = fitz.open("png", img_byte_arr)
        rect = img[0].rect
        pdfbytes = img.convert_to_pdf()
        img.close()
        imgPDF = fitz.open("pdf", pdfbytes)
        page = pdf_doc.new_page(width=rect.width, height=rect.height)
        page.show_pdf_page(rect, imgPDF, 0)
    pdf_doc.save(pdf_path)
    pdf_doc.close()
    
    return pdf_path

def read_frames(video_path, frame_interval=5):
    cap = cv2.VideoCapture(video_path)
    frames = []
    current_frame = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_frame += 1
        if current_frame % frame_interval == 0:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frames.append(gray_frame)

    cap.release()
    return frames

def OCR(video_path, frame_interval=5):
    frames = read_frames(video_path, frame_interval)
    similar_frames = []
    num_frames = len(frames)

    for i in range(num_frames - 1):
        if are_frames_similar(frames[i], frames[i + 1]):
            similar_frames.append(True)
        else:
            similar_frames.append(False)

    unique_slides = [Image.fromarray(frames[i + 1]) for i, is_similar in enumerate(similar_frames) if not is_similar]
    return unique_slides

def whisper(file_path):
    device = "cuda"
    batch_size = 1  # reduce if low on GPU mem
    compute_type = "int8"  # change to "int8" if low on GPU mem (may reduce accuracy)
    video_clip = VideoFileClip(file_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile('output.mp3')
    audio_clip.close()

    # 1. Transcribe with original whisper (batched)
    model = whisperx.load_model("large-v2", device, compute_type=compute_type)

    audio = whisperx.load_audio('output.mp3')
    result = model.transcribe(audio, batch_size=batch_size)

    # 2. Align whisper output
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
    res = []
    for segment in result["segments"]:
        res.append(f"{segment['start']} - {segment['end']}: {segment['text']}\n")

    os.remove('output.mp3')
    return res

def gpt_photo(file_path):
    # OpenAI API Key
    api_key = "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"
    images = []
    image_urls = []
    extract_images_from_pdf(file_path, images)
    for image in range(len(images)):
        image_urls.append(f'data:image/jpeg;base64,{encode_image(images[image])}')
    result = []
    result.append(gptURLs(image_urls, api_key))
    for image in range(len(images)):
        os.remove(images[image])
    return result

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def extract_images_from_pdf(file_path, images):
    doc = fitz.open(file_path)
    for i in range(len(doc)):
        for img_index, img in enumerate(doc.get_page_images(i)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            # Constructing a filename for each image
            image_filename = f"image_page_{i}_img_{img_index}.png"

            with open(image_filename, "wb") as image_file:
                image_file.write(image_bytes)

            images.append(image_filename)
    return images

def gptURLs(imagesURL, api):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
    {
        "role": "user",
        "content": [
        {
            "type": "text",
            "text": """I'm using you as an API with automated requests that primarily have images of lecture slides in them and nothing else.  Your goal is to extract the info from each page and summarize it proportionally to the page content and explain the content.

The input will always be of this form:
<images>

And I want you to respond always, without fail, in this form:
Page1: <your output for page 1>
Page2: <your output for page 2>
Page3: <your output for page 3>… and so on

Meaning you should only respond with the explained summarized text. There is no limit for how many words you write.
"""
        },
        ]
    }
    ],
    "max_tokens": 4096
}
    # Adding image URLs to the message
    for url in imagesURL:
        payload["messages"][0]["content"].append(
        {
            "type": "image_url",
            "image_url": {
            "url": url,
            },
        }
    )

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()['choices'][0]['message']['content']