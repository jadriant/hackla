from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import argparse
from medModel import load_model

parser = argparse.ArgumentParser()
parser.add_argument('--model_path', '-mp', type=str, default=None)
args = parser.parse_args()

tokenizer, model = load_model("t5-large", args.model_path)

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/simplify')
def simplify():
    complex_medical_terms = request.args.get('med_complex')
    if complex_medical_terms == None:
        return jsonify({
            'error': 'Unable to process input medical terms'
        }), 404    

    med_easi_endpoint = os.environ.get('MED_EASI_ENDPOINT')
    print('Endpoint:', med_easi_endpoint)
    if med_easi_endpoint == '':
        return jsonify({
            'error': 'Unable to reach medical translation server'
        }), 500    

    input_str = "$simple$ ; $expert$ = " + complex_medical_terms
    print('Input:', input_str)
    input_ids = tokenizer.encode(input_str, return_tensors="pt")
    outputs = model.generate(input_ids)

    simplified_medical_terms = tokenizer.decode(outputs[0])

    return jsonify({
        'simplified_medical_terms': simplified_medical_terms
    }), 200



if __name__ == '__main__':
    app.run(debug=True)