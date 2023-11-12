from flask import Flask, request as req, jsonify
from dotenv import load_dotenv
import os
import requests

app = Flask(__name__)
load_dotenv()

@app.route('/', methods=['GET', 'POST'])
def index():
    return 'Hello World!'

@app.route('/process', methods=['POST'])
def simplify():
    # input_audio = req.json.get('input_audio', '')
    # if input_audio == '':
    #     return jsonify({
    #         'error': 'Unable to obtain input audio'
    #     }), 404
    
    # speech_to_text_endpoint = os.environ.get('SPEECH_TO_TEXT_ENDPOINT')
    # if speech_to_text_endpoint == None:
    #     return jsonify({
    #         'error': 'Unable to reach speech to text server'
    #     }), 500
    
    # speech_to_text_endpoint_path = speech_to_text_endpoint + '/speech-to-text'
    # payload = {
    #     'input_audio': input_audio
    # }

    # res = requests.get(speech_to_text_endpoint_path, json=payload)
    # if res.status_code != 200:
    #     return jsonify({
    #         'error': 'Unable to process speech to text'
    #     }), 500

    complex_medical_terms = req.json.get('med_complex', '')
    if complex_medical_terms == '':
        return jsonify({
            'error': 'Unable to process input medical terms'
        }), 404 

    med_easi_endpoint = os.environ.get('MED_PROCESSOR_ENDPOINT')
    if med_easi_endpoint == None:
        return jsonify({
            'error': 'Unable to reach medical processing server'
        }), 500
    
    med_easi_endpoint_path = med_easi_endpoint + '/med-processor'
    payload = {
        'med_complex': complex_medical_terms
    }

    res = requests.get(med_easi_endpoint_path, json=payload)
    if res.status_code != 200:
        return jsonify({
            'error': 'Unable to process medical terms'
        }), 500
    
    simple_medical_terms = res.json().get('med_simple', '')
    if simple_medical_terms == '':
        return jsonify({
            'error': 'Unable to retrieve medical terms from server'
        }), 500
    
    translator_endpoint = os.environ.get('TRANSLATOR_ENDPOINT')
    if translator_endpoint == None:
        return jsonify({
            'error': 'Unable to reach translator'
        })
    
    translator_endpoint_path = translator_endpoint + '/translator'
    payload = {
        'input_lang': simple_medical_terms
    }

    res = requests.get(translator_endpoint_path, json=payload)
    if res.status_code != 200:
        return jsonify({
            'error': 'Unable to translate language'
        })
    
    output_lang = res.json().get('output_lang', '')
    if output_lang == '':
        return jsonify({
            'error': 'Unable to get output language from translator'
        })
    
    text_to_speech_endpoint = os.environ.get('TEXT_TO_SPEECH_ENDPOINT')
    if text_to_speech_endpoint == None:
        return jsonify({
            'error': 'Unable to reach text to speech server'
        })
    
    text_to_speech_endpoint_path = text_to_speech_endpoint + '/text-to-speech'
    payload = {
        'med_simple': output_lang
    }

    res = requests.get(text_to_speech_endpoint_path, json=payload)
    if res.status_code != 200:
        return jsonify({
            'error': 'Unable to get text to speech'
        })
    
    output_speech = res.json().get('output_speech', '')
    if output_speech == '':
        return jsonify({
            'error': 'Unable to get output speech from text to speech'
        })
    
    return jsonify({
        'translated_med_simple': output_speech
    })


if __name__ == '__main__':
    app.run(host='localhost', port=5050, debug=True)