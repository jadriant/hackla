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

@app.route('/doctor-speaks', methods=['POST'])
def process_doc():
    """
    This function needs decomplication for medical jargon, and
    is converted from English to a foreign language.
    """

    file = request.files['file']


    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    else:
        print("received file")
        print(file.filename)

    if file and allowed_file(file.filename):
        try:
            # Process the .wav file
            with wave.open(file, 'rb') as wav_file:
                # Extract Raw Audio from Wav File
                signal = wav_file.readframes(-1)
                signal = np.frombuffer(signal, dtype='int16')
                fs = wav_file.getframerate()
                if wav_file.getnchannels() == 2:
                    print('Just mono files')
                    sys.exit(0)
    except:
        print("Error")
        return jsonify({'error': 'Error processing file'}), 400

    complex_medical_terms, err = speech_to_text(file)

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
    
    file = request.files['file']


    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    else:
        print("received file")
        print(file.filename)

    if file and allowed_file(file.filename):
        try:
            # Process the .wav file
            with wave.open(file, 'rb') as wav_file:
                # Extract Raw Audio from Wav File
                signal = wav_file.readframes(-1)
                signal = np.frombuffer(signal, dtype='int16')
                fs = wav_file.getframerate()
                if wav_file.getnchannels() == 2:
                    print('Just mono files')
                    sys.exit(0)
    except:
        print("Error")
        return jsonify({'error': 'Error processing file'}), 400

    complex_medical_terms, err = speech_to_text(file)
    
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