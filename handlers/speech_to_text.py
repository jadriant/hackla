import os
import requests

def speech_to_text(input_speech):
    speech_to_text_endpoint = os.environ.get('SPEECH_TO_TEXT_ENDPOINT')
    if speech_to_text_endpoint == None:
        return (None, 'Unable to reach speech to text server')
    
    speech_to_text_endpoint_path = speech_to_text_endpoint + '/speech-to-text'
    payload = {
        'input_audio': input_speech
    }

    res = requests.get(speech_to_text_endpoint_path, json=payload)
    if res.status_code != 200:
        return (None, 'Unable to process speech to text')
    
    complex_medical_terms = res.json().get('med_complex', '')
    if complex_medical_terms == '':
        return (None, 'Unable to retrieve medical terms from server')
    
    return (complex_medical_terms, None)