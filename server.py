from flask import (
    Flask,
    request as req,
    jsonify
)
from dotenv import load_dotenv
import wave

from handlers.speech_to_text import speech_to_text
from handlers.med_processor import decomplicate
from handlers.translator import translate
from handlers.text_to_speech import text_to_speech

from pydub import AudioSegment

def convert_webm_to_wav(webm_file_storage):
    filename = webm_file_storage.filename
    base_name = filename.split('.')[0]
    wav_file_path = base_name + '.wav'  # Specify the directory to save
    
    audio = AudioSegment.from_file(webm_file_storage, format="webm")
    audio.export(wav_file_path, format="wav")
    return wav_file_path

app = Flask(__name__)
load_dotenv()

@app.route('/doctor-speaks', methods=['POST'])
def process_doc():
    """
    This function needs decomplication for medical jargon, and
    is converted from English to a foreign language.
    """

    file = req.files['file']

    input_lang_choice, output_lang_choice = '英语', '韩语'

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    else:
        print("received file")
        print(file.filename)

    if file:
        wav_file = convert_webm_to_wav(file)
    else:
        print("Error")
        return jsonify({'error': 'Error processing file'}), 400

    complex_medical_terms, err = speech_to_text(wav_file)

    if err != None:
        return jsonify({
            'error': err
        })

    print(complex_medical_terms)

    simple_medical_terms, err = decomplicate(complex_medical_terms)
    if err != None:
        return jsonify({
            'error': err
        })

    output_lang, err = translate(simple_medical_terms, input_lang_choice, output_lang_choice)
    if err != None:
        return jsonify({
            'error': err
        })
    
    return text_to_speech(output_lang)

@app.route('/patient-speaks', methods=['POST'])
def process_patient():
    """
    This function does not need decomplication for medical jargon, and
    is converted from a foreign language to English.
    """
    
    file = req.files['file']

    input_lang_choice, output_lang_choice = '韩文', '韩语'

    if file:
        wav_file = convert_webm_to_wav(file)
    else:
        print("Error")
        return jsonify({'error': 'Error processing file'}), 400
    
    simple_question, err = speech_to_text(wav_file)
    if err != None:
        return jsonify({
            'error': err
        })

    en_lang, err = translate(simple_question, input_lang_choice, output_lang_choice)
    if err != None:
        return jsonify({
            'error': err
        })
    
    return text_to_speech(en_lang)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)