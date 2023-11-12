# 🩺 Med GT

Hello there 👋 Med GT is a medical translation tool that streamlines doctor-patient communication. It's meant to facilitate conversation, taking in speech as an input, running it through a medical simplification model, a translation model, and converting the outputs back into text.

## 🧱 Structure

This is the main server that communicates between the frontend web client and 4 ML models hosted separately in Huggingface 🤗

## 💻 Usage

To run this server, fill in `.env.copy` and rename it to `.env`, then simply call

```
python server.py
```

Some informal tests have been setup but without the usual rigour of unit tests, and they can be found under `/test`.

## Testing

```
cd ./test
python test_speech_to_text.py
python test_translator.py
```

- `TODO:` test_text_to_speech.py
- `TODO:` test_med_processor.py

When calling APIs to Huggingface Spaces, it might take awhile for the containers to spin up (because they become inactive after 1h), so please retry the testing after ~2min has passed.

## Authors

This project was part of our ongoing paper to enhance doctor-patient communication, especially in third world countries. The authors involved in training our own models and building this end-to-end application are:

- Yoonsoo Nam
- Jadrian Tan
- Scott Susanto
- Alfred Tan
- Wilson Tan

Feel free to learn more about our project in the [paper linked above](./paper.pdf).
