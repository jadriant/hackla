import sys
import os

sys.path.append(os.path.abspath('../'))

from handlers.translator import translate
from utils import print_green

def test_translate():
    simple_medical_terms = 'hello world'
    input_lang_choice = '英语'
    output_lang_choice = '中文'
    output_lang, err = translate(simple_medical_terms, input_lang_choice, output_lang_choice)
    assert err == None
    assert output_lang == '你好,世界'
    print_green('PASSED: test_translate()')

test_translate()