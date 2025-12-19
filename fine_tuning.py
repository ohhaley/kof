import evaluate
import json
import math
import numpy as np
import pandas as pd
import random
from datasets import load_dataset, Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer

repo_id = 'Qwen/Qwen3-4B-Instruct-2507'

def convert_to_dict(string):
    if pd.isna(string) or str(string).strip() == "":
        return {}
    try:
        return json.loads(string.replace("'", '"'))
    except Exception as e:
        return f"Error: {e}"

def tokenize_func(examples):
    tokenizer = AutoTokenizer.from_pretrained(repo_id)
    return tokenizer(examples["text"], padding="max_length", truncation=True)

def compute_metrics(eval_pred):
    metric = evaluate.load("accuracy")
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

def split_data(data, training_percentage, seed):
    random.seed(seed)
    shuffled_data = data.sample(frac=1, random_state=seed)
    total_rows = shuffled_data.shape[0]
    training_rows = int(training_percentage * total_rows)
    training = shuffled_data.iloc[:training_rows, :]
    testing = shuffled_data.iloc[training_rows:, :]
    return training, testing

def format_messages(entry):
    messages = [
        {'role': 'user', 'content': entry['prompt'],
         'role': 'assistant', 'content': entry['reasoning']}
    ]
    tokenizer = AutoTokenizer.from_pretrained(repo_id)
    texts = [
        tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
        for msg in messages
    ]

    return tokenizer(texts, truncation=True, padding='max_length')

# Read in the fine tuning csv
# ---------- PREPROCESSING ----------
def preprocess_data(file_name):

    column_names = ['prompt', 'reasoning', 'response 2', 'label']
    data = pd.read_csv(file_name, header=None, names=column_names, sep='\[\[::\]\]', engine='python', on_bad_lines='skip')

    # game_info is a prefix to remove from 'prompt 1'
    with open("systemprompt.md", 'r') as f: game_info = f.read()
    data['prompt'] = data['prompt'].str.removeprefix(game_info)

    # Convert response 2 to a dict from a string
    # data['response 2'] = data['response 2'].apply(convert_to_dict)

    dataset = Dataset.from_pandas(data)

    formatted_data = dataset.map(format_messages)

    print(formatted_data)

    # tokenized_data = formatted_data.map(tokenize_func, batched=True)

    # Shuffle and split data into two sets
    # Do this last as well
    return formatted_data, 0

td, ed = preprocess_data('finetune_Naci_2_games_200t_4.74_overnight.csv')
print(td.head())

def fine_tune():

    # num labels = 1 makes it regression i guess
    model = AutoModelForSequenceClassification.from_pretrained(repo_id, num_labels=1)

    # our training thing does it by epochs like our neural nets i guess
    training_arguments = TrainingArguments("test_trainer", evaluation_strategy="epoch")

    trainer = Trainer(model=model, args=training_arguments, train_dataset=td, eval_dataset=ed, compute_metrics=compute_metrics)

    # trainer is now trained.
    trainer.train()

# TODO
# how do we export the fine tuned model
# make sure to get data in and randomize, split, etc.
# what formats of data can we even accept?
# HOW DO WE MAKE IT CLEAR THE LABEL IS WHAT WE WANT TO BE PREDICTED