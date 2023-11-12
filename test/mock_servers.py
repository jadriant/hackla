from flask import Flask, request as req, jsonify

app = Flask(__name__)

@app.route('/speech-to-text')
def speech_to_text():
    input_audio = req.json.get('input_audio', '')
    if input_audio == '':
        return jsonify({
            'error': 'Unable to obtain input audio'
        }), 404
    
    return jsonify({
        'med_complex': 'This is some complex shit'
    }), 200

@app.route('/med-processor')
def med_easi():
    complex_medical_terms = req.json.get('med_complex', '')
    if complex_medical_terms == '':
        return jsonify({
            'error': 'Unable to process input medical terms'
        }), 404
    
    return jsonify({
        'med_simple': 'This line has been simplified 🔥'
    }), 200

@app.route('/translator')
def translator():
    input_lang = req.json.get('input_lang', '')
    if input_lang == '':
        return jsonify({
            'error': 'Unable to obtain input language'
        }), 404

    output_lang = '这是输出语言'
    return jsonify({
        'output_lang': output_lang
    }), 200

@app.route('/text-to-speech')
def text_to_speech():
    simple_medical_terms = req.json.get('med_simple', '')
    if simple_medical_terms == '':
        return jsonify({
            'error': 'Unable to get simplified medical terms'
        })
    
    output_speech = 'some .wav file'
    return jsonify({
        'output_speech': output_speech
    })

if __name__ == '__main__':
    app.run(host='localhost', port=5051, debug=True)