import os

from bot import bot
from flask import (Flask, jsonify, redirect, render_template, request, session,
                   url_for)
from quiz import get_quiz
from summary import get_summary
from summary_gpt import get_summary_gpt
from uploadpdf import process_pdf

from flask_session import Session  # You may need to install this package

app = Flask(__name__, template_folder='pages', static_folder='pages/static')
secret_key = os.urandom(16)  # Generates a 16-byte (128-bit) random string
app.secret_key = secret_key  # Replace with a real secret key
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# مجلد لتخزين الملفات المؤقتة
UPLOAD_FOLDER = 'C:\\Users\\mald2\\OneDrive\\Desktop\\capstone\\tech_innovators\\content\\pdf_f'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chatbot', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        return render_template('chatbot.html')
    else:
        # When a message is sent from the interface, handle the POST request
        data = request.get_json()
        user_input = data['message']
        # The 'bot' function is called with the user input and expected to return a response
        file_path = session.get('file_path', '')
        bot_response = bot(file_path, user_input)
        return jsonify({'reply': bot_response})
    
@app.route('/lecture_chatbot', methods=['POST'])
def dropdown_chatbot():
    data = request.json
    selected_lecture = data['lecture']
    session['file_path'] = f"content/final_f/{selected_lecture}.txt"
    return session['file_path']

@app.route('/summary', methods=['GET','POST'])
def summary():
    if request.method == 'GET':
        return render_template('summary.html')
    
@app.route('/lecture_summary', methods=['POST'])
def dropdown_summary():
    data = request.json
    selected_lecture = data['lecture']
    session['file_path'] = f"content/final_f/{selected_lecture}.txt"
    #output = get_summary(session['file_path'])
    output = get_summary_gpt(session['file_path'])
    return output

    
@app.route('/quiz', methods=['GET','POST'])
def quiz():
    if request.method == 'GET':
        return render_template('quiz.html')

@app.route('/lecture_quiz', methods=['POST'])
def dropdown_quiz():
    data = request.json
    selected_lecture = data['lecture']
    session['file_path'] = f"content/final_f/{selected_lecture}.txt"
    output = get_quiz(session['file_path'])
    print(output)
    return output

@app.route('/upload_chat', methods=['POST'])
def upload_chat():
    if request.method == 'POST':
        f = request.files['file']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        con1, con2, con3 = process_pdf(file_path)
        # Path to the file you want to delete
        output_file_path = "C:\\Users\\mald2\\OneDrive\\Desktop\\capstone\\tech_innovators\\content\\uploads\\output.txt"

        # Check if file exists and delete it
        if os.path.exists(output_file_path):
            os.remove(output_file_path)
        with open(output_file_path, 'a', encoding='utf-8') as f:
            f.write("Transcript of the audio for the lecture:\n")
            for i in con1:
                f.write(i)
            f.write("\n\nThe content from the lecture slides:\n")
            for i in con2:
                f.write(f"{i}\n")
            f.write("\n\n")
            for i in con3:
                f.write(f"{i}\n")
    return redirect(url_for('chat_uploaded'))

@app.route('/uploaded_chatbot', methods=['GET', 'POST'])
def chat_uploaded():
    if request.method == 'GET':
        return render_template('chatbot_upload.html')
    else:
        # When a message is sent from the interface, handle the POST request
        data = request.get_json()
        user_input = data['message']
        # The 'bot' function is called with the user input and expected to return a response
        file_path = "content/uploads/output.txt"
        bot_response = bot(file_path, user_input)
        return jsonify({'reply': bot_response})

@app.route('/uploaded_quiz', methods=['GET','POST'])
def quiz_uploaded():
    if request.method == 'GET':
        return render_template('quiz_upload.html')
    else:
        file_path = "content/uploads/output.txt"
        output = get_quiz(file_path)
        return jsonify(output)

    
@app.route('/upload_quiz', methods=['POST'])
def upload_quiz():
    if request.method == 'POST':
        f = request.files['file']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        con1, con2, con3 = process_pdf(file_path)
        # Path to the file you want to delete
        output_file_path = "C:\\Users\\mald2\\OneDrive\\Desktop\\capstone\\tech_innovators\\content\\uploads\\output.txt"

        # Check if file exists and delete it
        if os.path.exists(output_file_path):
            os.remove(output_file_path)
        with open(output_file_path, 'a', encoding='utf-8') as f:
            f.write("Transcript of the audio for the lecture:\n")
            for i in con1:
                f.write(i)
            f.write("\n\nThe content from the lecture slides:\n")
            for i in con2:
                f.write(f"{i}\n")
            f.write("\n\n")
            for i in con3:
                f.write(f"{i}\n")
    return jsonify({'message': 'File uploaded successfully'})

@app.route('/uploaded_summary', methods=['GET','POST'])
def summary_uploaded():
    if request.method == 'GET':
        return render_template('summary_upload.html')
    else:
        file_path = "content/uploads/output.txt"
        output = get_summary_gpt(file_path)
        return jsonify(output)

@app.route('/upload_summary', methods=['GET','POST'])
def upload_summary():
    if request.method == 'POST':
        f = request.files['file']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        con1, con2, con3 = process_pdf(file_path)
        # Path to the file you want to delete
        output_file_path = "C:\\Users\\mald2\\OneDrive\\Desktop\\capstone\\tech_innovators\\content\\uploads\\output.txt"

        # Check if file exists and delete it
        if os.path.exists(output_file_path):
            os.remove(output_file_path)
        with open(output_file_path, 'a', encoding='utf-8') as f:
            f.write("Transcript of the audio for the lecture:\n")
            for i in con1:
                f.write(i)
            f.write("\n\nThe content from the lecture slides:\n")
            for i in con2:
                f.write(f"{i}\n")
            f.write("\n\n")
            for i in con3:
                f.write(f"{i}\n")
    return jsonify({'message': 'File uploaded successfully'})


if __name__ == '__main__':
    app.run(debug=True)