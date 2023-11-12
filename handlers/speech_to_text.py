import os
from gradio_client import Client

from dotenv import load_dotenv

load_dotenv()

def speech_to_text(input_speech):
    speech_to_text_endpoint = os.environ.get('SPEECH_TO_TEXT_ENDPOINT')
    if speech_to_text_endpoint == None:
        return (None, 'Unable to reach speech to text server')
        
    client = Client(speech_to_text_endpoint)
    
    complex_medical_terms = client.predict(
        input_speech,
        'transcribe',
        api_name='/predict'
    )
    if complex_medical_terms == '':
        return (None, 'Unable to retrieve medical terms from server')
    
    return (complex_medical_terms, None)