import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

def load_model(model_name, model_path=None):
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    # Add map_location parameter
    if model_path == None:
        model = T5ForConditionalGeneration.from_pretrained(model_name)
    else:
        model_dict = torch.load(model_path, map_location='cuda:0' if torch.cuda.is_available() else 'cpu')
        model = T5ForConditionalGeneration.from_pretrained(model_name, state_dict=model_dict['model_state_dict'])

    return (tokenizer, model)


if __name__ == '__main__':
    tokenizer, model = load_model("t5-large")
    # input_str = "$simple$ ; $expert$ = chronic obstructive pulmonary disease"
    input_str = "simplify this: chronic obstructive pulmonary disease"
    input_ids = tokenizer.encode(input_str, return_tensors="pt")
    outputs = model.generate(input_ids)
    simplified_medical_terms = tokenizer.decode(outputs[0])
    print(simplified_medical_terms)