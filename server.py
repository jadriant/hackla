from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

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
    


if __name__ == '__main__':
    app.run(debug=True)