import numpy as np
from datasets import load_dataset, load_metric
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
# from trl import SFTConfig, SFTTrainer
# from peft import get_peft_model, LoraConfig, prepare_model_for_kbit_training

repo_id = 'Qwen/Qwen3-4B-Instruct-2507'

tokenizer = AutoTokenizer.from_pretrained(repo_id)


def tokenize_func(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

metric = load_metric("accuracy")
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

# do this after all data preprocessing
tokenized_datasets = data.map(tokenize_func, batched=True)

# num labels = 1 makes it regression i guess
model = AutoModelForSequenceClassification.from_pretrained(repo_id, num_labels=1)

training_arguments = TrainingArguments("test_trainer", evaluation_strategy="epoch")

trainer = Trainer(model=model, args=training_arguments, train_dataset=blank, eval_dataset=ahh, compute_metrics=compute_metrics)

trainer.train()

