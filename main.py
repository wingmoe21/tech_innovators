import io
import multiprocessing
import os

import cv2
import fitz
import numpy as np
import whisperx
from moviepy.editor import VideoFileClip
from PIL import Image
from skimage.metrics import structural_similarity as ssim

device = "cuda"
video_path = "C:\\Users\\mald2\\OneDrive\\Desktop\\capstone\\tech_innovators\\VID\\How to declare a pointer to a function.mp4"
batch_size = 2  # reduce if low on GPU mem
compute_type = "float16"  # change to "int8" if low on GPU mem (may reduce accuracy)
# Tolerance to decide whether two images are similar
similarity_threshold = 0.95


""" def convert_mp4_to_mp3(input_file, output_file):
    video_clip = VideoFileClip(input_file)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(output_file)
    audio_clip.close()
 """

""" def whisberX(vid):
    convert_mp4_to_mp3(vid, 'output.mp3')

    # 1. Transcribe with original whisper (batched)
    model = whisperx.load_model("large-v2", device, compute_type=compute_type)

    audio = whisperx.load_audio('output.mp3')
    result = model.transcribe(audio, batch_size=batch_size)

    # 2. Align whisper output
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

    # Save the aligned segments to a text file
    output_file_path = 'aligned_segments.txt'
    with open(output_file_path, 'w') as f:
        for segment in result["segments"]:
            f.write(f"{segment['start']} - {segment['end']}: {segment['text']}\n")
 """

def are_frames_similar(frame_pair):
    frame1, frame2 = frame_pair
    # Calculate the structural similarity index (SSI) between two frames
    # You can use skimage's structural_similarity function for this
    # from skimage.metrics import structural_similarity as compare_ssim
    # Return True if they are similar above the given threshold
    ssi_index, _ = ssim(frame1, frame2, full=True)
    return ssi_index > similarity_threshold


def OCR(vid):


    # Previous frame for comparison
    prev_frame = None
    
    cap = cv2.VideoCapture(video_path)
    frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frames.append(gray_frame)

    cap.release()

    with multiprocessing.Pool() as pool:
        frame_pairs = zip(frames[:-1], frames[1:])
        similar_frames = pool.map(are_frames_similar, frame_pairs)

    unique_slides = []

    for i, is_similar in enumerate(similar_frames):
        if not is_similar:
            slide_image = Image.fromarray(frames[i + 1])
            unique_slides.append(slide_image)

    return unique_slides

    
def save_slides_to_pdf(unique_slides):
    pdf_doc = fitz.open()

    for slide in unique_slides:
        img_byte_arr = io.BytesIO()
        slide.save(img_byte_arr, format='PNG')
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

unique_slides = OCR(video_path)
