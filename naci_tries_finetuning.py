from datasets import load_dataset, Dataset
from transformers import Trainer
from transformers import TrainingArguments
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
import numpy as np
import evaluate
import pandas as pd

raw_datasets = load_dataset("imdb")
print(raw_datasets["train"]["text"])
print(raw_datasets["train"]["label"])
metric = evaluate.load("accuracy")

tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

def preprocess_data(file_name):

    column_names = ['prompt 1', 'reasoning', 'response 2', 'label']
    data = pd.read_csv(file_name, header=None, names=column_names, sep='\[\[::\]\]', engine='python', on_bad_lines='skip')

    # game_info is a prefix to remove from 'prompt 1'
    with open("systemprompt.md", 'r') as f: game_info = f.read()
    data['prompt 1'] = data['prompt 1'].str.removeprefix(game_info)

    # Convert response 2 to a dict from a string
    # data['response 2'] = data['response 2'].apply(convert_to_dict)

    dataset = Dataset.from_pandas(data)
    return dataset

raw_datasets = preprocess_data("finetune.csv")

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

tokenized_datasets = raw_datasets.map(tokenize_function, batched=True)

small_train_dataset = tokenized_datasets["train"].shuffle(seed=42).select(range(1000)) 
small_eval_dataset = tokenized_datasets["test"].shuffle(seed=42).select(range(1000)) 
full_train_dataset = tokenized_datasets["train"]
full_eval_dataset = tokenized_datasets["test"]

model = AutoModelForSequenceClassification.from_pretrained("bert-base-cased", num_labels=2)

training_args = TrainingArguments(output_dir="test_trainer")

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=small_train_dataset,
    eval_dataset=small_eval_dataset,
    compute_metrics=compute_metrics,
)

trainer.train()

trainer.evaluate()

print(raw_datasets["train"]["text"])
print(raw_datasets["train"]["label"])