from flask import Response
from elevenlabs import set_api_key, generate
from dotenv import load_dotenv
import os

load_dotenv()
set_api_key(os.environ.get('ELEVEN_LABS_API_KEY'))

def text_to_speech(output_lang):
    """
    I'm optimizing for a better UX, so I set `stream=True` to stream the audio.
    If this proves too hard for React client, set `stream=False` and I believe we
    can save the audio as a file.

    https://elevenlabs.io/docs/api-reference/integration-guides/python-text-to-speech-guide

    Look for keyword `files` here. Afterward you may need to serialize the file before
    sending it over to the client.
    """
    output_speech = generate(text=output_lang, stream=True)
    return Response(output_speech, content_type='application/octet-stream')