import requests
import simpleaudio as sa
from io import BytesIO
from pydub import AudioSegment

def play_stream(url):
    """
    This one is harder to test. Goodluck 😈
    """
    response = requests.get(url, stream=True)
    buffer = BytesIO()

    try:
        for chunk in response.iter_content(chunk_size=1024):
            buffer.write(chunk)
            buffer.seek(0)

            # Using pydub to handle different audio formats
            audio_segment = AudioSegment.from_file(buffer, format="mp3")
            play_obj = sa.play_buffer(
                audio_segment.raw_data, 
                num_channels=audio_segment.channels, 
                bytes_per_sample=audio_segment.sample_width, 
                sample_rate=audio_segment.frame_rate
            )

            buffer.seek(0)
            buffer.truncate()

            play_obj.wait_done()
    finally:
        buffer.close()

stream_url = 'http://127.0.0.1:5050/text_to_speech'
play_stream(stream_url)
