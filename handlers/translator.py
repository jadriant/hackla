import os
import requests

def translate(simple_medical_terms):
    translator_endpoint = os.environ.get('TRANSLATOR_ENDPOINT')
    if translator_endpoint == None:
        return (None, 'Unable to reach translator server')
    
    translator_endpoint_path = translator_endpoint + '/translator'
    payload = {
        'input_lang': simple_medical_terms
    }

    res = requests.get(translator_endpoint_path, json=payload)
    if res.status_code != 200:
        return (None, 'Unable to translate medical terms')
    
    output_lang = res.json().get('output_lang', '')
    if output_lang == '':
        return (None, 'Unable to retrieve translation from server')
    
    return (output_lang, None)