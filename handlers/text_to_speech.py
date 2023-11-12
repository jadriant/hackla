import os
import requests

def text_to_speech(output_lang):
    text_to_speech_endpoint = os.environ.get('TEXT_TO_SPEECH_ENDPOINT')
    if text_to_speech_endpoint == None:
        return (None, 'Unable to reach text to speech server')
    
    text_to_speech_endpoint_path = text_to_speech_endpoint + '/text-to-speech'
    payload = {
        'med_simple': output_lang
    }

    res = requests.get(text_to_speech_endpoint_path, json=payload)
    if res.status_code != 200:
        return (None, 'Unable to process text to speech')
    
    output_speech = res.json().get('output_speech', '')
    if output_speech == '':
        return (None, 'Unable to retrieve speech from server')
    
    return (output_speech, None)