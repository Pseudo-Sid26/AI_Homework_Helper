import os
import pandas as pd
from datasets import Dataset
import google.generativeai as genai
import pytesseract
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import easyocr
import re
import keras_ocr
import matplotlib.pyplot as plt
import chardet
from io import BytesIO

# Initialize EasyOCR Reader and Keras-OCR pipeline
reader = easyocr.Reader(['en'])
pipeline = keras_ocr.pipeline.Pipeline()

# Specify the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'E:\STUDIES\AI Project\OCR-Tessaract\tesseract.exe'  # Update path as needed

# Set Google API key for Gemini
api_key = os.getenv('GOOGLE_API_KEY', 'API KEY')
genai.configure(api_key=api_key)


# Load a CSV file as a dataset for fine-tuning
def load_csv_dataset(csv_path):
    try:
        with open(csv_path, 'rb') as f:
            result = chardet.detect(f.read())
        encoding = result['encoding']
        data = pd.read_csv(csv_path, encoding=encoding, engine='python')

        if 'question' not in data.columns or 'answer' not in data.columns:
            raise ValueError("CSV must contain 'question' and 'answer' columns.")

        data = data.dropna(subset=['question', 'answer'])
        data['question'] = data['question'].astype(str)
        data['answer'] = data['answer'].astype(str)
        dataset = Dataset.from_pandas(data)
        return dataset
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None


def generate_answer_gemini(question, context=None):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Question: {question}\nProvide a short and concise answer."
        if context:
            prompt += f"\nContext: {context}"

        print(f"Sending prompt to model: {prompt}")  # Logging the prompt

        response = model.generate_content(prompt)
        answer = response.text.strip()

        if not answer:
            print("Received empty answer from model.")  # Logging empty response

        concise_answer = shorten_answer(answer)
        return concise_answer
    except Exception as e:
        print(f"Error generating answer: {e}")
        return "Sorry, there was an error processing your request."


# Shorten the generated answer to make it concise
def shorten_answer(answer):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', answer)
    concise_answer = " ".join(sentences[:2])
    return concise_answer


# Format the answer into numbered steps
def format_answer_in_steps(answer):
    steps = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', answer)
    formatted_steps = [f"Step {i + 1}: {step.strip()}" for i, step in enumerate(steps) if step.strip()]
    return "\n".join(formatted_steps)


# Preprocess images for OCR
def preprocess_image(image):
    image = image.convert('L')  # Convert to grayscale
    image = ImageOps.invert(image)  # Invert the image
    image = ImageEnhance.Contrast(image).enhance(3)  # Increase contrast
    image = ImageEnhance.Sharpness(image).enhance(2)  # Sharpen the image
    image = image.filter(ImageFilter.MedianFilter())  # Apply median filter
    return image


# Process input from PDF, image, or text
def process_input(input_data):
    """Process input from a PDF, image, or text."""
    if isinstance(input_data, str):
        if os.path.isfile(input_data):
            # If input is a file path, determine file type and process accordingly
            if input_data.lower().endswith('.pdf'):
                pages = convert_from_path(input_data)
                text = "".join(pytesseract.image_to_string(preprocess_image(page)) for page in pages)
                return text
            elif input_data.lower().endswith(('.png', '.jpg', '.jpeg')):
                image = Image.open(input_data)
                return pytesseract.image_to_string(preprocess_image(image))
            else:
                with open(input_data, 'r') as file:
                    return file.read()
        else:
            return input_data  # Direct text input
    elif isinstance(input_data, BytesIO):
        image = Image.open(input_data)
        return pytesseract.image_to_string(preprocess_image(image))
    elif isinstance(input_data, Image.Image):
        return pytesseract.image_to_string(preprocess_image(input_data))
    else:
        raise ValueError("Unsupported input type")


# Text extraction using Tesseract OCR
def extract_text_tesseract(file_path):
    if not os.path.isfile(file_path):
        logging.error(f"File not found: {file_path}")
        return ""
    return process_input(file_path)

# Text extraction using EasyOCR
def extract_text_easyocr(file_path):
    try:
        if file_path.lower().endswith('.pdf'):
            pages = convert_from_path(file_path)
            text = "".join(
                " ".join([result[1] for result in reader.readtext(preprocess_image(page))]) for page in pages)
            return text
        elif file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            image = Image.open(file_path)
            return " ".join([result[1] for result in reader.readtext(preprocess_image(image))])
        else:
            raise ValueError("Unsupported file type for OCR.")
    except Exception as e:
        print(f"Error extracting text with EasyOCR: {e}")
        return ""


# Text extraction using Keras-OCR
def extract_text_kerasocr(image_paths):
    try:
        images = [keras_ocr.tools.read(img) for img in image_paths]
        prediction_groups = pipeline.recognize(images)

        fig, axs = plt.subplots(nrows=len(images), figsize=(10, 20))
        if len(images) == 1:  # Handle case where there's only one image
            axs = [axs]  # Convert single Axes to a list for consistency
        for ax, image, predictions in zip(axs, images, prediction_groups):
            keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)
        plt.show()

        # Print text from the images
        for i, predicted_image in enumerate(prediction_groups):
            print(f"Predicted Text from Image {i + 1}:")
            for text, box in predicted_image:
                print(text)
        return prediction_groups
    except Exception as e:
        print(f"Error extracting text with Keras-OCR: {e}")
        return []


# Generate an answer formatted in steps
def generate_answer_in_steps(question, context=None):
    answer = generate_answer_gemini(question, context)
    return format_answer_in_steps(answer)


# Example usage with Keras-OCR
image_paths = ['/content/Image1.png', '/content/Image2.png']
extracted_texts = extract_text_kerasocr(image_paths)

# Example of question-answer generation
question = "What is the tallest mountain?"
answer_in_steps = generate_answer_in_steps(question)
print(answer_in_steps)
