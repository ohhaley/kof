#adapted from https://www.dailydoseofds.com/p/step-by-step-guide-to-fine-tune-qwen3/
from unsloth import FastLanguageModel
import torch

MODEL = "unsloth/Qwen3-14B"

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = MODEL,
    max_seq_length=2048,
    dtype=None,
    load_in_4bit=True,
    full_finetuning=False
)

model = FastLanguageModel.get_peft_model(
    model,
    target_modules=["q_proj","k_proj","v_proj","o_proj"],
    use_gradient_checkpointing="unsloth",
    r=16,
    lora_alpha=4,
    lora_dropout=0,
    bias="none"
)

from datasets import load_dataset

name = "mlabonne/FineTome-100k"
non_reasoning_data = load_dataset(name,split="train")

#print(non_reasoning_data[0])

print(type(non_reasoning_data))

#non_reasoning_data = load_dataset("json",data_files="test_ft.json")

#print(type(non_reasoning_data))

from unsloth.chat_templates import standardize_sharegpt

dataset = standardize_sharegpt(non_reasoning_data)

#from ChatGPT. Full prompt can be found in gpt-prompt.txt
def apply_template(row):
    row["text"] = tokenizer.apply_chat_template(
        row["conversations"],
        tokenize = False
    )
    return row

#non_reasoning_conv = tokenizer.apply_chat_template(dataset["conversations"])
#similarly from ChatGPT
dataset = dataset.map(apply_template)

from trl import SFTTrainer, SFTConfig

trainer = SFTTrainer(model = model,
                     tokenizer = tokenizer,
                     train_dataset=dataset,
                     args = SFTConfig(
                         per_device_train_batch_size=2,
                         gradient_accumulation_steps=4,
                         max_steps=3,
                         learning_rate=1e-4,
                         optim="adamw_8bit",
                         weight_decay=0.01,
                     ))

trainer_stats = trainer.train()
print(trainer_stats)