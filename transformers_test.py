from transformers import T5Tokenizer, T5ForConditionalGeneration, DataCollatorWithPadding, TrainingArguments, Trainer
from datasets import load_dataset, load_metric
import numpy as np
from sklearn.model_selection import train_test_split


model_name = "google/flan-t5-base"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

#preprocessing
dataset = load_dataset("Open-Orca/OpenOrca")


def tokenize_function(data):
    return tokenizer(data['system_prompt'], data['question'], data['response'], padding="max_length", truncation=True) 

tokenized_dataset = dataset.map(tokenize_function, batched=True)
train_dataset, eval_dataset = train_test_split(tokenized_dataset["train"], test_size=0.2, random_state=42)


#training
collator = DataCollatorWithPadding(tokenized_dataset)
args = TrainingArguments(
    "T5/test_trainer",
    evaluation_strategy="epoch",
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=6,
    learning_rate=2e-5,
    weight_decay=0.01)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

trainer = Trainer(
    model,
    TrainingArguments=args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    data_collator=collator,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

trainer.train()
predictions = trainer.predict(tokenized_dataset["validation"])
metric = load_metric("glue", "mrpc")
preds = np.argmax(predictions.predictions, axis=-1)
metric.compute(predictions=preds, references=predictions.label_ids)


model.save_pretrained('T5/test_model')
tokenizer.save_pretrained('T5/test_tokenizer')

print(tokenizer)