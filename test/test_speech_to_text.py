import sys
import os

sys.path.append(os.path.abspath('../'))

from handlers.speech_to_text import speech_to_text
from utils import print_green

def test_speech_to_text(input_speech_path):
    output_speech, err = speech_to_text(input_speech_path)
    assert err == None
    assert output_speech == ' I love translating complex medical jargon to simplified commonplace terms.'
    print_green('PASSED: test_speech_to_text()')

test_speech_to_text('./test.wav')