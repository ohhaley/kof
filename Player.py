from llama_cpp import Llama
from pydantic import BaseModel

# This file essentially opens a model using a .gguf file, gives it some game history, and asks it to analyze the players' suspicion levels.
# You can modify the example_history variable to test different game scenarios.
# Make sure to have llama_cpp and pydantic installed in your Python environment.
# The models are multiple GBs in size so I can't upload those to the repo, but have linked to the one I've used below.

# Notable findings so far:
# Mistral Instruct breaks, so maybe reasoning-focused models aren't great, but n=1 basically so who knows
# Gemma3 is highly suspicious of the first player listed it seems, and apparently doesn't read the full history before making judgments.


example_history = ["You are Purple",
                   "You are the librarian.",
                   "Green says Green is the investigator",
                   "Blue says Blue is the chef.",
                   "Green says Green investigated Blue and Blue is the chef.",
                   "Red says Red is the doctor.",
                   "Yellow says Yellow is the doctor."]


# The models themselves are multiple GBs in size so can't be included in the repo. 
# I downloaded the model I'm using here: https://huggingface.co/unsloth/gemma-3-4b-it-GGUF/tree/main
# Just throw the .gguf file into the main /kof folder
# Ministral-3b-instruct.Q6_K.gguf
# gemma-3-1b-it-Q3_K_M.gguf
# Ministral-3b-instruct.Q2_K.gguf

model = Llama(model_path=r"gemma-3-4b-it-Q4_0.gguf", n_gpu_layers=-1, logits_all=True, verbose=False, n_ctx=2048)

def combine_history(history):
    combined = ""
    for entry in history:
        combined += entry + "\n"
    return combined.strip()

# Data structures for the model to respond with
class Player(BaseModel):
    name: str
    suspicion: float

class PlayerList(BaseModel):
    players: list[Player]

hist = combine_history(example_history)

message_template = [
        {
            "role": "system",
            "content": "Given a list of information, list all players along with how suspicious they are and why."
        },
        {
            "role": "user",
            "content": f"Analyze the following game history and provide your reasoning:\n\n{hist}"
        }
    ]

# Initial response asking for suspicion reasoning
response = model.create_chat_completion(
    messages=message_template, temperature=0.1
)
print(response["choices"][0]["message"]["content"])

# Adds the model's response to the history, then asks it to list the players with suspicion scores based on that reasoning.
message_template.append({"role": "assistant", "content": response["choices"][0]["message"]["content"]})
message_template.append({"role": "user", "content": "From your reasoning, list the players along with a float value to indicate how suspicious each player is."})

# Runs the model asking for PlayerList as output using the above as the most recent prompt to follow.
response2 = model.create_chat_completion(
    messages=message_template,
    response_format={"type": "json_object", "schema": PlayerList.model_json_schema()},
    temperature=0.1
)
print(response2["choices"][0]["message"]["content"])