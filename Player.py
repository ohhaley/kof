from llama_cpp import Llama
from pydantic import BaseModel

example_history = ["Red claimed to be a villager.", 
                    "Green claimed to be the investigator.",
                    "Blue claimed to be the chef.",
                    "Yellow claimed to be the fortune teller.",
                    "Green says Blue is the chef.",
                    "Blue says Green is good.",
                    "Yellow says Red is good."
                    "Blue agrees Red is good."]

model = Llama(model_path=r"gemma-3-1b-it-Q3_K_M.gguf", n_gpu_layers=-1, logits_all=True, verbose=False, n_ctx=2048)

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
            "content": hist
        }
    ]

# Initial response asking for suspicion reasoning
response = model.create_chat_completion(
    messages=message_template, temperature=0.1
)

print(response["choices"][0]["message"]["content"])
message_template.append({"role": "assistant", "content": response["choices"][0]["message"]["content"]})
message_template.append({"role": "user", "content": "From your reasoning, list the players along with a float value to indicate how suspicious each player is."})

response2 = model.create_chat_completion(
    messages=message_template,
    response_format={"type": "json_object", "schema": PlayerList.model_json_schema()},
    temperature=0.1
)
print(response2["choices"][0]["message"]["content"])