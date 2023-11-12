import sys
import os

sys.path.append(os.path.abspath('../'))

from handlers.med_processor import decomplicate
from utils import print_green

def test_med_processor(complex_medical_terms):
    # TODO: @yoonsoo1
    simple_medical_terms, err = decomplicate(complex_medical_terms)
    assert err == None
    print(simple_medical_terms)
    print_green('PASSED: test_med_processor()')

test_med_processor('With diaphragmatic involvement, splinting of the chest and pain in one or both shoulders may occur. '
                   'Other manifestations of FMF include acute pleurisy (in 30 %); arthritis (in 25 %), usually involving the knee, ankle, and hip; '
                   'an erysipelas - like rash of the lower leg; and scrotal swelling and pain caused by inflammation of the tunica vaginalis of the testis. '
                   'Pericarditis occurs very rarely.')