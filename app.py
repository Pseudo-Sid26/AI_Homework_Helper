from flask import Flask, request, redirect, render_template, session, url_for, jsonify
from flask_mail import Mail, Message
import os
import re
import logging
from ai_helper import generate_answer_gemini, extract_text_tesseract
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'Sid$123'  # Change this to a random secret key

DEFAULT_USERNAME = "user123"
DEFAULT_PASSWORD = "pass$#%123"

# Simulated user database (for demo purposes)
users_db = {}

@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD:
        # Redirect to the main question-answer page
        return redirect(url_for('question_answer_page'))
    else:
        # Handle login failure (show an error message)
        return render_template('landing_page.html', error="Invalid username or password.")

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['signupUsername']
    email = request.form['signupEmail']
    password = request.form['signupPassword']

    if username in users_db:
        return render_template('landing_page.html', error="Username already exists. Please choose another one.")

    # Store user with hashed password
    users_db[username] = {
        'email': email,
        'password': generate_password_hash(password)
    }

    # Store the username in the session
    session['username'] = username
    return redirect(url_for('question_answer_page'))  # Redirect to question answer page after signup

@app.route('/main')
def main_page():
    if 'username' in session:
        return render_template('index.html', username=session['username'])  # Pass the username to the template
    return redirect(url_for('landing_page'))

@app.route('/question_answer_page')
def question_answer_page():
    if 'username' in session:
        return render_template('index.html', username=session['username'])  # Render the actual question-answering page
    return redirect(url_for('landing_page'))

# Configuration for email notifications
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'Your mail@gmail.com'  # Your email
app.config['MAIL_PASSWORD'] = 'Google acc. App pwd'  # Use an App Password if using 2-Step Verification
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'Your mail@gmail.com'

mail = Mail(app)

# Define a list of blocked words
blocked_words = ['badword1', 'badword2', 'badword3']

# Simulate a database (for demo purposes)
student_activity_log = []

# Set a folder to save uploaded files
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def send_notification_to_parent(question):
    """ Send an email notification to the parent. """
    msg = Message("Question Asked by Student",
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=["parent-email@domain.com"])  # Replace with parent's email
    msg.body = f"The following question was asked: {question}"
    try:
        mail.send(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def is_content_blocked(question):
    """ Check for obscene content in the question. """
    pattern = re.compile('|'.join(blocked_words), re.IGNORECASE)
    return bool(pattern.search(question))

@app.route('/process', methods=['POST'])
def process_question():
    try:
        question = ""

        # Handle file upload or direct text input
        if 'file' in request.files and request.files['file']:
            file = request.files['file']
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            print(f"Extracting text from: {file_path}")  # Debug print
            question = extract_text_tesseract(file_path)  # Pass file path to Tesseract
        else:
            question = request.form.get('question', '')

        # Validate the input
        if not question:
            return jsonify({"error": "No question provided"}), 400

        if is_content_blocked(question):
            return jsonify({"error": "Blocked content. Please provide appropriate content."}), 400

        # Log student activity and notify parent
        student_activity_log.append(question)
        send_notification_to_parent(question)

        # Generate answer using the Gemini model
        answer = generate_answer_gemini(question)

        if answer == "Sorry, there was an error processing your request.":
            return jsonify({"error": "Error generating answer from the model."}), 500

        return jsonify({"answer": answer})

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({"error": f"An internal error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
