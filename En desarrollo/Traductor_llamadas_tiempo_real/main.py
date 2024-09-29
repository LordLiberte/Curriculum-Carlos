"""Este documento es la linea general del proyecto. Se basa en un sistema que permite hablar y realizar una traducción directa de lo que habla"""

import pyttsx3
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('API_KEY_DeepL')
