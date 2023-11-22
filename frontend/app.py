from bot import bot
from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder='pages', static_folder='pages/static')

@app.route('/')
def home():
    return render_template('home.html')  # Replace with your home page file name

@app.route('/chatbot', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        return render_template('page1.html')  # Replace with your home page file name
    else:
        # When a message is sent from the interface, handle the POST request
        data = request.get_json()
        user_input = data['message']
        # The 'bot' function is called with the user input and expected to return a response
        bot_response = bot("Recording3.txt", user_input)
        return jsonify({'reply': bot_response})

@app.route('/summary')
def summary():
    return render_template('summary.html')  # Replace with your home page file name

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')  # Replace with your home page file name

if __name__ == '__main__':
    app.run(debug=True)
