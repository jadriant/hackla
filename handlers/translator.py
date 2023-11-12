import os
import requests
from dotenv import load_dotenv

load_dotenv()

def translate(simple_medical_terms, input_lang_choice, output_lang_choice):
    translator_endpoint = os.environ.get('TRANSLATOR_ENDPOINT')
    if translator_endpoint == None:
        return (None, 'Unable to reach translator server')
    
    translator_endpoint_path = translator_endpoint + '/run/predict'
    payload = {
        'data': [
            input_lang_choice,
            output_lang_choice,
            simple_medical_terms,
        ]
    }

    res = requests.post(translator_endpoint_path, json=payload)
    if res.status_code != 200:
        return (None, 'Unable to translate medical terms')
    
    output_lang = res.json().get('data', '')[0]
    if output_lang == '':
        return (None, 'Unable to retrieve translation from server')
    
    return (output_lang, None)
