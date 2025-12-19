import pandas as pd
from datasets import load_dataset, Dataset
from transformers import AutoTokenizer
from trl import SFTTrainer, SFTConfig

repo_id = 'Qwen/Qwen3-4B-Instruct-2507'
tokenizer = AutoTokenizer.from_pretrained(repo_id)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.chat_template = (
    "{% for message in messages %}"
    "{{ '<|im_start|>' + message['role'] + '\\n' }}"
    "{% if message['role'] == 'assistant' %}"
        "{% generation %}"
        "{% if message.get('thinking') %}"
            "{{ '<think>\\n' + message['thinking'] + '\\n</think>\\n' }}"
        "{% endif %}"
        "{{ message['content'] }}"
        "{% endgeneration %}"
    "{% else %}"
        "{{ message['content'] }}"
    "{% endif %}"
    "{{ '<|im_end|>\\n' }}"
    "{% endfor %}"
    "{% if add_generation_prompt %}"
    "{{ '<|im_start|>assistant\\n' }}"
    "{% endif %}"
)

def format_messages(entry):
    messages = [
        {'role': 'user', 'content': entry['prompt']},
        {'role': 'assistant', 'content': entry['reasoning']}
    ]
    return pd.Series({'messages': messages, 'label': entry['label']})

def validate_dataset(dataset, tokenizer):
    print("--- Validating Dataset for Assistant Tokens ---")
    found_issue = False
    
    for i in range(min(5, len(dataset))):  # Check first 5 samples
        sample = dataset[i]
        # Simulate what the trainer does
        formatted_text = tokenizer.apply_chat_template(sample['messages'], tokenize=False)
        
        # Check if 'assistant' header exists in the string
        if "<|im_start|>assistant" not in formatted_text:
            print(f"Row {i} is missing assistant markers!")
            print(f"Content: {formatted_text[:100]}...")
            found_issue = True
            
    if not found_issue:
        print("Chat template looks good.")


# Read in the fine tuning csv
# ---------- PREPROCESSING ----------
def preprocess_data(file_name):

    good_threshold = 2.3
    evil_threshold = 1.0

    thresholds = {
        'WASHERWOMAN': good_threshold,
        'LIBRARIAN': good_threshold,
        'INVESTIGATOR': good_threshold,
        'CHEF': good_threshold,
        'EMPATH': good_threshold,
        'FORTUNETELLER': good_threshold,
        'UNDERTAKER': good_threshold,
        'MONK': good_threshold,
        'RAVENKEEPER': good_threshold,
        'VIRGIN': good_threshold,
        'SLAYER': good_threshold,
        'SOLDIER': good_threshold,
        'MAYOR': good_threshold,
        'BUTLER': good_threshold,
        'SAINT': good_threshold,
        'RECLUSE': good_threshold,
        'DRUNK': good_threshold,

        'POISONER': evil_threshold,
        'SPY': evil_threshold,
        'BARON': evil_threshold,
        'SCARLET WOMAN': evil_threshold,
        'IMP': evil_threshold
    }

    evil_roles = ['POISONER','SPY','BARON','SCARLET WOMAN','IMP']

    column_names = ['name', 'role', 'prompt', 'reasoning', 'response 2', 'label']
    data = pd.read_csv(file_name, header=None, names=column_names, sep='\[\[::\]\]', engine='python', on_bad_lines='skip')

    data = data.dropna(subset=['prompt', 'reasoning'])
    data = data[data['reasoning'].str.strip() != ""]

    # game_info is a prefix to remove from 'prompt 1'
    with open("systemprompt.md", 'r') as f: game_info = f.read()
    data['prompt'] = data['prompt'].str.removeprefix(game_info)

    val = pd.to_numeric(data['label'], errors='coerce')
    thresh = data['role'].map(thresholds)

    mask = (data['role'].isin(evil_roles) & (val > thresh)) | (~data['role'].isin(evil_roles) & (val < thresh))

    filtered_data = data[mask]

    # Convert response 2 to a dict from a string
    # data['response 2'] = data['response 2'].apply(convert_to_dict)

    # dataset = Dataset.from_pandas(data)
    dataset = filtered_data.apply(format_messages, axis=1)
    # tokenized_data = formatted_data.map(tokenize_func, batched=True)

    # Shuffle and split data into two sets
    # Do this last as well
    d_dataset = Dataset.from_pandas(dataset)
    dataset_split = d_dataset.train_test_split(test_size=0.1)

    train_dataset = dataset_split["train"]
    eval_dataset = dataset_split["test"]
    return train_dataset, eval_dataset

def fine_tune():

    td, ed = preprocess_data('finetune_Naci_2_games_200t_4.74_overnight.csv')
    validate_dataset(td, tokenizer)

    sft_config = SFTConfig(
        output_dir="./qwen3-sft-output",
        max_length=2048,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        learning_rate=2e-5,
        bf16=False, # Use bfloat16 for Qwen3 if your GPU supports it
        logging_steps=10,
        eval_strategy='epoch',
        eval_steps=50,
        do_eval=True,
        assistant_only_loss=True,
        packing=False
    )

    trainer = SFTTrainer(
        model=repo_id,
        train_dataset=td,
        eval_dataset=ed,
        args=sft_config,
        processing_class=tokenizer
    )

    # trainer is now trained.
    trainer.train()

fine_tune()

# TODO
# make sure to get data in and randomize, split, etc.
# what formats of data can we even accept?
# HOW DO WE MAKE IT CLEAR THE LABEL IS WHAT WE WANT TO BE PREDICTED