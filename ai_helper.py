import os
import pytesseract
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import google.generativeai as genai
import re
import fitz  # PyMuPDF

# Specify the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\"Your path"\OCR-Tessaract\tesseract.exe'  # Update path as needed

# Set Google API key for Gemini
api_key = os.getenv('GOOGLE_API_KEY', 'Gemini API key')
genai.configure(api_key=api_key)


def generate_answer_gemini(question):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Question: {question}\nProvide a short and concise answer."

        response = model.generate_content(prompt)
        answer = response.text.strip()

        if not answer:
            print("Received empty answer from model.")

        concise_answer = shorten_answer(answer)
        return concise_answer
    except Exception as e:
        print(f"Error generating answer: {e}")
        return "Sorry, there was an error processing your request."


def shorten_answer(answer):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', answer)
    concise_answer = " ".join(sentences[:2])
    return concise_answer


def preprocess_image(image):
    image = image.convert('L')  # Convert to grayscale
    image = ImageOps.invert(image)  # Invert the image
    image = ImageEnhance.Contrast(image).enhance(3)  # Increase contrast
    image = ImageEnhance.Sharpness(image).enhance(2)  # Sharpen the image
    image = image.filter(ImageFilter.MedianFilter())  # Apply median filter
    return image


def extract_text_tesseract(file_path):
    """ Extract text from an image file or PDF using Tesseract OCR. """
    try:
        # Check if the file is a PDF
        if file_path.lower().endswith('.pdf'):
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                text += pytesseract.image_to_string(img)
            return text
        else:
            # Handle image files
            with Image.open(file_path) as img:
                text = pytesseract.image_to_string(img)
            return text
    except Exception as e:
        raise ValueError(f"Error extracting text: {e}")
