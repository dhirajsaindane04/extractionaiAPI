import google.generativeai as genai
import json
import logging
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the Google API key from the environment variables
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

logger = logging.getLogger(__name__)

# Configure the generative AI client with the API key
genai.configure(api_key=GOOGLE_API_KEY)

def load_prompt(file_path='prompt.txt'):
    with open(file_path, 'r') as file:
        return file.read()

def get_gemini_response(input_text, image_parts):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = load_prompt()

    response = model.generate_content([input_text, image_parts[0], prompt])
    
    response_text = response.text.strip()
    if response_text.startswith("```json"):
        response_text = response_text[7:-3].strip()

    response_text = ' '.join(response_text.split())

    try:
        response_json = json.loads(response_text)
    except json.JSONDecodeError as e:
        logger.error(f"JSON Decode Error: {e}")
        response_json = {'error': 'Invalid JSON response from the model'}
    
    return response_json
