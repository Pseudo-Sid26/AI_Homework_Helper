from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
import os
import re
import logging
from ai_helper import generate_answer_gemini, extract_text_tesseract, extract_text_easyocr, extract_text_kerasocr  # Import necessary functions

app = Flask(__name__)

# Configuration for email notifications
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your mail@gmail.com'  # Your email
app.config['MAIL_PASSWORD'] = 'Google app pwd'  # Use an App Password if using 2-Step Verification
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'your mail@gmail.com'

mail = Mail(app)

# Define a list of obscene/blocked words
blocked_words = ['badword1', 'badword2', 'badword3']

# Simulate a database (for demo purposes)
student_activity_log = []

def send_notification_to_parent(question):
    """ Send an email notification to the parent. """
    msg = Message("Question Asked by Student",
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=["parent-email@domain.com"])  # Replace with parent email
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_question():
    try:
        # Handle file or question input
        if 'file' in request.files and request.files['file']:
            file = request.files['file']
            question = extract_text_tesseract(file) or extract_text_easyocr(file) or extract_text_kerasocr([file])
        else:
            question = request.form.get('question', '')

        # Validate the input
        if not question:
            return jsonify({"error": "No question provided"}), 400

        if is_content_blocked(question):
            return jsonify({"error": "Blocked content. Please provide appropriate content."}), 400

        student_activity_log.append(question)
        send_notification_to_parent(question)
        answer = generate_answer_gemini(question)

        if answer == "Sorry, there was an error processing your request.":
            return jsonify({"error": "Error generating answer from the model."}), 500

        return jsonify({"answer": answer})

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({"error": f"An internal error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
