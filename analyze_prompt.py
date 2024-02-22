from transformers import T5Tokenizer, T5ForConditionalGeneration, AutoTokenizer, RobertaForQuestionAnswering, AutoModelForQuestionAnswering
from datasets import load_dataset
import torch

def get_keywords(input):
    tokenizer = T5Tokenizer.from_pretrained('T5/test_tokenizer')
    model = T5ForConditionalGeneration.from_pretrained('T5/test_model')

    input_text = "get keywords in this input: " + input
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids

    outputs = model.generate(input_ids)
    return str(tokenizer.decode(outputs[0])).replace("<pad>", "").replace("</s>", "").split(" ")

'''ask model if answer sufficiently matches prompt according to keywords'''
def sufficient_answer_criteria(user_input, keywords) -> bool:
    tokenizer = AutoTokenizer.from_pretrained("deepset/roberta-base-squad2")
    model = RobertaForQuestionAnswering.from_pretrained("deepset/roberta-base-squad2")

    out = " ".join([str(keyword + " ") for keyword in keywords])
    print(out)
    question, text = "Is the user input: " + user_input + ", sufficient? Give a Yes or No answer.", out
    #question, text = "Who was Jim Henson?", "Jim Henson was a nice puppet"
    inputs = tokenizer(question, text, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)

    answer_start_index = outputs.start_logits.argmax()
    answer_end_index = outputs.end_logits.argmax()
    predict_answer_tokens = inputs.input_ids[0, answer_start_index : answer_end_index + 1]
    answer = tokenizer.decode(predict_answer_tokens, skip_special_tokens=True)
    print(answer)

    target_start_index = torch.tensor([17])
    target_end_index = torch.tensor([len(question) - 1])
    outputs = model(**inputs, start_positions=target_start_index, end_positions=target_end_index)

    if "yes" in answer.lower():
        return True
    else:
        return False

