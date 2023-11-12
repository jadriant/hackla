from flask import (
    Flask,
    request as req,
    jsonify
)
from dotenv import load_dotenv

from handlers.speech_to_text import speech_to_text
from handlers.med_processor import decomplicate
from handlers.translator import translate
from handlers.text_to_speech import text_to_speech

app = Flask(__name__)
load_dotenv()

@app.route('/', methods=['GET', 'POST'])
def index():
    return 'Hello World!'

@app.route('/doctor-speaks', methods=['POST'])
def process_doc():
    """
    This function needs decomplication for medical jargon, and
    is converted from English to a foreign language.
    """
    
    input_audio = req.json.get('input_audio', '')
    if input_audio == '':
        return jsonify({
            'error': 'Unable to obtain input audio'
        }), 404
    
    complex_medical_terms, err = speech_to_text(input_audio)
    if err != None:
        return jsonify({
            'error': err
        })

    simple_medical_terms, err = decomplicate(complex_medical_terms)
    if err != None:
        return jsonify({
            'error': err
        })

    output_lang, err = translate(simple_medical_terms)
    if err != None:
        return jsonify({
            'error': err
        })
    
    translated_med_simple, err = text_to_speech(output_lang)
    if err != None:
        return jsonify({
            'error': err
        })
    
    return jsonify({
        'translated_med_simple': translated_med_simple
    })

@app.route('/patient-speaks', methods=['POST'])
def process_patient():
    """
    This function does not need decomplication for medical jargon, and
    is converted from a foreign language to English.
    """
    
    input_audio = req.json.get('input_audio', '')
    if input_audio == '':
        return jsonify({
            'error': 'Unable to obtain input audio'
        }), 404
    
    simple_question, err = speech_to_text(input_audio)
    if err != None:
        return jsonify({
            'error': err
        })

    en_lang, err = translate(simple_question)
    if err != None:
        return jsonify({
            'error': err
        })
    
    en_question, err = text_to_speech(en_lang)
    if err != None:
        return jsonify({
            'error': err
        })
    
    return jsonify({
        'en_question': en_question
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)