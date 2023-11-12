import os
import requests

def decomplicate(complex_medical_terms):
    med_processor_endpoint = os.environ.get('MED_PROCESSOR_ENDPOINT')
    if med_processor_endpoint == None:
        return (None, 'Unable to reach medical processing server')
    
    med_processor_endpoint_path = med_processor_endpoint + '/med-processor'
    payload = {
        'med_complex': complex_medical_terms
    }

    res = requests.get(med_processor_endpoint_path, json=payload)
    if res.status_code != 200:
        return (None, 'Unable to process medical terms')
    
    simple_medical_terms = res.json().get('med_simple', '')
    if simple_medical_terms == '':
        return (None, 'Unable to retrieve medical terms from server')
    
    return (simple_medical_terms, None)
