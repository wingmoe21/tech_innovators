import os

from bot import bot
from flask import Flask, jsonify, render_template, request, session
from quiz import get_quiz
from summary import get_summary
from summary_gpt import get_summary_gpt

from flask_session import Session  # You may need to install this package

app = Flask(__name__, template_folder='pages', static_folder='pages/static')
secret_key = os.urandom(16)  # Generates a 16-byte (128-bit) random string
app.secret_key = secret_key  # Replace with a real secret key
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


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



if __name__ == '__main__':
    app.run(debug=True)
