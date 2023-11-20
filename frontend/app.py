from flask import Flask, render_template

app = Flask(__name__, template_folder='pages', static_folder='pages/static')

@app.route('/')
def home():
    return render_template('home.html')  # Replace with your home page file name
@app.route('/chatbot')
def chatbot():
    return render_template('page1.html')  # Replace with your home page file name

if __name__ == '__main__':
    app.run(debug=True)
