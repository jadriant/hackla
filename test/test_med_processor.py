import sys
import os

sys.path.append(os.path.abspath('../'))

from handlers.med_processor import decomplicate
from utils import print_green

def test_med_processor():
    complex_medical_terms = 'hello world'
    # TODO: @yoonsoo1