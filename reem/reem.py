from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfReader
import os

app = Flask(__name__)

# مجلد لتخزين الملفات المؤقتة
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        # تأكد من وجود مجلد uploads
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)

        processed_text = process_pdf(file_path)
        
        # احفظ النص في ملف نصي
        text_file_path = os.path.join(UPLOAD_FOLDER, f"{os.path.splitext(uploaded_file.filename)[0]}_output.txt")
        with open(text_file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(processed_text)

        # استخدم الطريق الكامل لملف النص عند إرساله
        return send_file(os.path.abspath(text_file_path), as_attachment=True)
    else:
        return render_template('index.html', error='يجب تحديد ملف PDF.')

def process_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    return text

if __name__ == '__main__':
    app.run(debug=True)
