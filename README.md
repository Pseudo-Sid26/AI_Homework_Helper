# 📚✨ AI Homework Helper ✨🤖

Welcome to **AI Homework Helper**, your advanced, AI-driven assistant designed to help students from class 1 to class 7 with their homework! Leveraging cutting-edge **Optical Character Recognition (OCR)** and **Generative AI models**, this tool extracts text from images, PDFs, or direct input and provides concise, accurate answers. Plus, it comes with parental controls to ensure safe usage by children. 🛡️

---

## 🌟 **Features** 🌟

- 📝 **Text Extraction:** Effortlessly extract questions from images and PDFs using **Tesseract**, **EasyOCR**, and **Keras-OCR**.
- 🤖 **AI-Powered Answer Generation:** Get precise and clear answers using the **Gemini model**.
- 👨‍👩‍👧 **Parental Controls:** Keep kids safe with notifications sent to parents and filters for inappropriate content.
- 💻 **User-Friendly Interface:** Enjoy a simple and intuitive web interface built with **Flask**.
- 🔒 **Full-Screen Mode:** Ensure focused learning by entering a distraction-free, full-screen mode.
- 📧 **Email Notifications:** Parents receive real-time email alerts whenever a question is asked.

---

## 🛠️ **Installation** 🛠️

Follow these steps to set up **AI Homework Helper** on your local machine:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/ai-homework-helper.git
    cd ai-homework-helper
    ```

2. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the environment variables**:
   - Create a `.env` file in the project root.
   - Add your configuration:
     ```dotenv
     MAIL_USERNAME=your-email@gmail.com
     MAIL_PASSWORD=your-email-password
     GOOGLE_API_KEY=your-google-api-key
     ```

5. **Run the Flask application**:
    ```bash
    python app.py
    ```

---

## ⚙️ **Configuration** ⚙️

To utilize the parental control and email notification features, ensure your email server and blocked words list are configured correctly:

- **Email Configuration:** Update the `MAIL_USERNAME` and `MAIL_PASSWORD` with your email credentials in `app.py`.
- **Blocked Words:** Modify the `blocked_words` list in `app.py` to add or remove inappropriate words.

---

## 🚀 **Usage** 🚀

1. **Upload an image or PDF:** Use the interface to upload homework questions in image or PDF format.
2. **Enter a question:** Alternatively, type a question directly into the text box.
3. **Get an answer:** The AI generates a concise answer based on the input.
4. **Receive notifications:** Parents receive an email notification whenever a question is asked.

---

## 🗂️ **Project Structure** 🗂️

├── ai_helper.py # Contains core functions for AI processing 
├── app.py # Main Flask application file 
├── templates 
      └── index.html # Frontend interface 
├── static 
      └── styles.css # Styling for the web interface 
├── requirements.txt # Dependencies required to run the project
├── README.md # Project README file 
└── .env # Environment variables



## 🧰 **Tech Stack** 🧰

- **Backend:** Python, Flask
- **AI Models:** Gemini, Tesseract OCR, EasyOCR, Keras-OCR
- **Frontend:** HTML, CSS, JavaScript
- **Email Service:** Flask-Mail, Mailgun API

---

## 🌍 **Future Enhancements** 🌍

- 🌐 **Multilingual Support:** Extend support for multiple languages.
- 🔍 **Advanced Filtering:** Implement AI-based content filtering for enhanced parental control.
- 📱 **Mobile App Integration:** Create a mobile app for easier access on the go.
- 🎮 **Gamification:** Introduce rewards and badges to motivate students.

---

## 🤝 **Contributing** 🤝

We welcome contributions from the community! If you'd like to contribute:

1. **Fork the repository.**
2. **Create a new branch:** `git checkout -b feature-branch`.
3. **Commit your changes:** `git commit -m 'Add some feature'`.
4. **Push to the branch:** `git push origin feature-branch`.
5. **Open a Pull Request.**

---

Thank you for checking out **AI Homework Helper**! 🎓💡 Let's make homework easy and fun for everyone! 😊
