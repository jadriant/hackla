from flask import Response
from elevenlabs import set_api_key, generate, stream
from dotenv import load_dotenv
import os

load_dotenv()
set_api_key(os.environ.get('ELEVEN_LABS_API_KEY'))

def text_to_speech(output_lang):
    output_speech = generate(text=output_lang, stream=True)
    return Response(output_speech, content_type='application/octet-stream')

text_to_speech('Hello World!')