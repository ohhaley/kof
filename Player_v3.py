from llama_cpp import Llama
from pydantic import BaseModel
from huggingface_hub import hf_hub_download

# gemma-3-4b-it-Q4_0.gguf
# llm = Llama(model_path=r"Qwen3-4b-Instruct.gguf", n_gpu_layers=-1, verbose=False, logits_all=False, n_ctx=4096)




# llm = Llama.from_pretrained(
# 	repo_id="byteshape/Qwen3-4B-Instruct-2507-GGUF",
# 	filename="Qwen3-4B-Instruct-2507-Q5_K_S-4.74bpw.gguf",
# )


def get_model(context_window = 4096):
    repo_id = "byteshape/Qwen3-4B-Instruct-2507-GGUF"
    filename="Qwen3-4B-Instruct-2507-Q5_K_S-4.74bpw.gguf"
    model_path = hf_hub_download(repo_id=repo_id, filename=filename)
    llm = Llama(
        model_path=model_path,
        n_ctx = context_window,
        verbose=False
    )
    return llm

llm = get_model()

class PlayerInfo():
    name: str
    alignment: str
    role: str
    
    def __init__(self, nm, al, rl):
        self.name = nm
        self.alignment = al
        self.role = rl

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

    def get_players(self): return self.players

class Vote(BaseModel):
    did_vote: bool

class Question(BaseModel):
    target: Player
    question: str

class QuestionData:
    target: Player
    question: str
    questioner: Player

    def __init__(self, t, q, qr):
        self.target = t
        self.question = q
        self.questioner = qr

def get_suspicion_list(player_list: PlayerList):
    string = ""
    players_listed = player_list.get_players()
    for player in players_listed:
        string += f"You think there is a {int(player.suspicion * 100.0)}% chance that {player.name} is on the EVIL team.\n"
    return string.strip()

def identify_self(player_info:PlayerInfo):
    return {"role": "user", "content": "Who are you?"}, {"role": "assistant", "content": f"I am {player_info.name}, my role is the {player_info.role}"}

# Given a history of information regarding other players, the llm will first think through.
# This assumes the player is good currently.
def build_suspicions(history: list[str], suspicions: PlayerList, model: Llama, player_info: PlayerInfo):
    hist = combine_history(history)

    if player_info.alignment == "GOOD":
        system_prompt = f"You are playing a social deduction game where your goal is to find evil players." \
                    f"You are player {player_info.name}, you are {player_info.alignment}, your role is the {player_info.role}." \
                    f"Given a list of information and a list that you previously made of how likely you thought each player is EVIL, list all players along with how likely they are to be EVIL and why." \
                    f"There can only be one of each role."
    else:
        system_prompt = f"You are playing a social deduction game where your goal is to pretend your role is a good character, eliminate good players and keep the demon alive." \
                    f"You are player {player_info.name}, you are {player_info.alignment}, your role is the {player_info.role}." \
                    f"Given a list of information and a list that you previously made of how likely you thought each player is EVIL, list all players along with how likely they are to be EVIL and why." \
                    f"There can only be one of each role."
                    
    suspicions_list = get_suspicion_list(suspicions)

    first_prompt = f"Analyze the following information and provide your reasoning:\nInformation:\n{hist}\nPrevious probabilities that players are on the EVIL team:\n{suspicions_list}"
    second_prompt = f"From your reasoning, update the list of players to account for any change in how likely they are to be EVIL. List your expectation that players are EVIL as a floating point value between 0.0 and 1.0, representing a percentage. 1.0 means a player is certainly EVIL; 0.5 means a player could equally be GOOD or EVIL; 0.0 means a player is certainly GOOD."

    response, response2 = use_llm(system_prompt=system_prompt, first_prompt=first_prompt, second_prompt=second_prompt, player_info=player_info, model=model, output_format=PlayerList.model_json_schema())
    return response2["choices"][0]["message"]["content"]

def request_information(history: list[str], suspicions: PlayerList, model: Llama, player_info: PlayerInfo):
    hist = combine_history(history)
    if player_info.alignment == "GOOD":
        system_prompt = f"You are playing a social deduction game where your goal is to find evil players." \
                        f"You are player {player_info.name}, you are {player_info.alignment}, your role is the {player_info.role}." \
                        f"Given a list of information and a list of how likely you think each player is EVIL, decide whether to ask another player for more information, and if so, what question to ask."
    else:
        system_prompt = f"You are playing a social deduction game where your goal is to pretend your role is a good character, eliminate good players and keep the demon alive." \
                        f"You are player {player_info.name}, you are {player_info.alignment}, your role is the {player_info.role}." \
                        f"Given a list of information and a list of how likely you think each player is EVIL, decide whether to ask another player for more information, and if so, what question to ask."
        
    suspicions_list = get_suspicion_list(suspicions)
    first_prompt = f"Analyze the following information and list of how likely you think each player is EVIL, and decide if there is a player that could provide more information, and what question to ask:\nInformation:\n{hist}\nChances each player is evil:\n{suspicions_list}"
    second_prompt = f"From your reasoning, if there is a question to ask, return which player to approach and what question to ask."

    response, response2 = use_llm(system_prompt=system_prompt, first_prompt=first_prompt, second_prompt=second_prompt, player_info=player_info, model=model, output_format=Question.model_json_schema())
    return response2["choices"][0]["message"]["content"]

def answer_question(history: list[str], suspicions: PlayerList, question_info: QuestionData, model: Llama, player_info: PlayerInfo):
    hist = combine_history(history)

    if player_info.alignment == "GOOD":
        system_prompt = f"You are playing a social deduction game where your goal is to find evil players." \
                        f"You are player {player_info.name}, you are {player_info.alignment}, your role is the {player_info.role}." \
                        f"You have been asked a question by a player. Given a list of information and a list of how likely you think each player is EVIL, respond to the player." \
                        f"Consider based on suspicion if you should respond truthfully, lie, or refuse to answer."
    else:
        system_prompt = f"You are playing a social deduction game where your goal is to pretend to be a good character, eliminate good players, and keep the DEMON alive." \
                        f"You are player {player_info.name}, you are {player_info.alignment}, your role is the {player_info.role}." \
                        f"You have been asked a question by a player. Given a list of information and a list of how likely you think each player is EVIL, respond to the player." \

    suspicions_list = get_suspicion_list(suspicions)
    
    first_prompt = f"Analyze the following information and list of how likely you think each player is EVIL and decide how to respond to this player:\nInformation:\n{hist}\nChances each player is evil:\n{suspicions_list}\nQuestioner:{question_info.questioner}\nQuestion:{question_info.question}"
    second_prompt = f"From your reasoning, return an answer to the question asked."
    response, response2 = use_llm(system_prompt=system_prompt, first_prompt=first_prompt, second_prompt=second_prompt, player_info=player_info, model=model)
    return response2["choices"][0]["message"]["content"]

# Given the history of information and the player's suspicions, should the model nominate to vote someone?
def nominate_player(history: list[str], suspicions: PlayerList, model: Llama, player_info: PlayerInfo):
    hist = combine_history(history)

    if player_info.alignment == "GOOD":
        system_prompt = f"You are playing a social deduction game where your goal is to eliminate evil players." \
                        f"You are player {player_info.name}, you are {player_info.alignment}, your role is the {player_info.role}." \
                        f"Given all information currently available to you and a list of how likely each player is EVIL that you have previously constructed, decide if there are any players that are suspicious enough that they should be put up for a vote for elimination."
    else:
       system_prompt = f"You are playing a social deduction game where your goal is to pretend to be a good character, eliminate good players, and keep the DEMON alive." \
                        f"You are player {player_info.name}, you are {player_info.alignment}, your role is the {player_info.role}." \
                        f"Given all information currently available to you and a list of how likely each player is EVIL that you have previously constructed, decide if there are any players that you want to put up for a vote for elimination."
    
    
    suspicions_list = get_suspicion_list(suspicions)
    
    first_prompt = f"Analyze the following information and list of how likely you think each player is EVIL and decide if there is a suitable nominee, there may not be one:\nInformation:\n{hist}\nSuspicions:\n{suspicions_list}"
    second_prompt = f"From your reasoning, give a player for nomination if there is one, otherwise return nothing."
    response, response2 = use_llm(system_prompt=system_prompt, first_prompt=first_prompt, second_prompt=second_prompt, player_info=player_info, model=model, output_format=Player.model_json_schema())
    return response2["choices"][0]["message"]["content"]

# Given a history of information and suspicions, the model has to decide if there is a nominee they are willing to vote for.
def vote_player(history: list[str], suspicions: PlayerList, nominee: Player, model: Llama, player_info):
    hist = combine_history(history)
    
    system_prompt = f"You are playing a social deduction game where your goal is to decide if you should vote a player for elimination." \
                    f"You are player {player_info.name}, you are {player_info.alignment}, your role is the {player_info.role}." \
                    f"Given all information currently available to you and a list of how likely you think each player is EVIL that you have previously constructed, decide if the nominee is someone you want to vote to execute."

    suspicions_list = get_suspicion_list(suspicions)
    nominees_list = get_suspicion_list(PlayerList(players = [nominee]))

    first_prompt = f"Analyze the following information and list of how likely you think each player is EVIL and decide whether or not to vote for the nominee:\nInformation:\n{hist}\nChances you think each player is EVIL:\n{suspicions_list}\nNominee:\n{nominees_list}"
    second_prompt = f"From your reasoning, if you decide to vote for the nominee return True, otherwise return False."

    response, response2 = use_llm(system_prompt=system_prompt, first_prompt=first_prompt, second_prompt=second_prompt, player_info=player_info, model=model, output_format=Vote.model_json_schema())

    return response2["choices"][0]["message"]["content"]

def choose_players(history: list[str], suspicions: PlayerList, model: Llama, player_info: PlayerInfo, num):
    hist = combine_history(history)

    if player_info.alignment == "GOOD":
        system_prompt = f"You are playing a social deduction game where your goal is to find evil players." \
                        f"You are player {player_info.name}, you are {player_info.alignment}, your role is the {player_info.role}." \
                        f"Given all information currently available to you and a list of how likely you think each player is EVIL that you have previously constructed, decide what players to choose for your ability."
    else:
        system_prompt = f"You are playing a social deduction game where your goal is to pretend to be a good character, eliminate good players, and keep the demon alive." \
                        f"You are player {player_info.name}, you are {player_info.alignment}, your role is the {player_info.role}." \
                        f"Given all information currently available to you and a list of how likely you think each player is EVIL that you have previously constructed, decide what players to choose for your ability."
    suspicions_list = get_suspicion_list(suspicions)
    
    first_prompt = f"Analyze the following information and existing chances you think each player is EVIL, and decide the {num} players to choose for your ability: \nInformation:\n{hist}\nChances you think each player is EVIL: \n{suspicions_list}"
    second_prompt = f"From your reasoning, give a list of the {num} players to choose for your ability. There must be {num} of them in the list."
    response, response2 = use_llm(system_prompt=system_prompt, first_prompt=first_prompt, second_prompt=second_prompt, player_info=player_info, model=model, output_format=PlayerList.model_json_schema())
    return response2["choices"][0]["message"]["content"]

def talk_publicly(history: list[str], suspicions: PlayerList, model: Llama, player_info: PlayerInfo):
    hist = combine_history(history)

    suspicions_list = get_suspicion_list(suspicions)

    if player_info.alignment == "GOOD":
        system_prompt = f"You are playing a social deduction game where your goal is to find evil players." \
                        f"You are player {player_info.name}, you are {player_info.alignment}, your role is the {player_info.role}." \
                        f"Given all information currently available to you and a list of how likely you think each player is EVIL you have previously constructed, decide if you would like to say anything publicly to every other player in the game."
    else:
        system_prompt = f"You are playing a social deduction game where your goal is to pretend to be a good character, eliminate good players, and keep the demon alive." \
                        f"You are player {player_info.name}, you are {player_info.alignment}, your role is the {player_info.role}." \
                        f"Given all information currently available to you and a list of how likely you think each player is EVIL you have previously constructed, decide if you would like to say anything publicly."
    
    first_prompt = f"Analyze the following information and existing chances you think that each player is EVIL and decide if you want to say anything publicly, you may not say anything: \nInformation\n{hist}\nChances you think each player is EVIL: \n{suspicions_list}."
    second_prompt = f"From your reasoning, give a message to say publicly or return nothing."
    response, response2 = use_llm(system_prompt, first_prompt, second_prompt, player_info, model)
    return response2["choices"][0]["message"]["content"]

# All LLM calls go through here.
# The LLM will think using the initial message_template before being called again with their reasoning and the second prompt to give a structured format if asked for. Leave blank if no special output format is needed.
def use_llm(system_prompt: str, first_prompt: str, second_prompt: str, player_info: PlayerInfo, model: Llama, output_format=None, max_tokens = 75):
    identify_q, identify_a = identify_self(player_info)
    with open("systemprompt.md", 'r') as f: game_info = f.read()
    system_prompt = game_info+"\n"+system_prompt

    message_template = [
        {"role": "system", "content": system_prompt},
        identify_q,
        identify_a,
        {"role": "user", "content": first_prompt}
    ]
    response = model.create_chat_completion(messages=message_template, temperature=0.1, max_tokens=max_tokens)
    print(response["choices"][0]["message"]["content"])
    with open("finetune.csv","a") as f:
        f.write(str(message_template).replace('\n', ''))
        f.write("[[::]]")
        f.write(response["choices"][0]["message"]["content"].replace('\n', ''))

    message_template.append({"role": "assistant", "content": response["choices"][0]["message"]["content"]})
    message_template.append({"role": "user", "content": second_prompt})

    if output_format != None:
        response2 = model.create_chat_completion(messages=message_template, response_format={"type": "json_object", "schema": output_format}, temperature=0.1)
    else:
        response2 = model.create_chat_completion(messages=message_template, temperature=0.1, max_tokens=max_tokens)

    print(response2["choices"][0]["message"]["content"])
    with open("finetune.csv","a") as f:
        f.write("[[::]]")
        f.write(str(response2["choices"][0]["message"]["content"]).replace('\n', ''))
    return response, response2

# # An example history of information that should clear Green and place suspicion on Red and Yellow
# example_history = ["Green says Green is the investigator",
#                    "Green says Green investigated Purple and Purple is the townsfolk.",
#                    "Blue says Blue is the chef.",
#                    "Red says Red is the doctor.",
#                    "Yellow says Yellow is the doctor."]

# # Use something like this at the start of the game
# starting_playerlist = PlayerList(players=[Player(name="Green", suspicion=0.0),
#                                           Player(name="Blue", suspicion=0.0),
#                                           Player(name="Red", suspicion=0.0),
#                                           Player(name="Yellow", suspicion=0.0)])

# # Offers two equally suspicious players
# example_suspicions1 = PlayerList(players=[Player(name="Green", suspicion=0.0),
#                                           Player(name="Blue", suspicion=0.0),
#                                           Player(name="Red", suspicion=0.7),
#                                           Player(name="Yellow", suspicion=0.7)])

# # Offers no suspicious players
# example_suspicions2 = PlayerList(players=[Player(name="Green", suspicion=0.0),
#                                           Player(name="Blue", suspicion=0.0),
#                                           Player(name="Red", suspicion=0.0),
#                                           Player(name="Yellow", suspicion=0.0)])

# # Offers multiple slightly suspicious players
# example_suspicions3 = PlayerList(players=[Player(name="Green", suspicion=0.0),
#                                           Player(name="Blue", suspicion=0.1),
#                                           Player(name="Red", suspicion=0.2),
#                                           Player(name="Yellow", suspicion=0.2)])

# # Meant for use with example_suspicions1
# example_nominees1 = PlayerList(players=[Player(name="Red", suspicion=0.7),
#                                         Player(name="Yellow", suspicion=0.7)])

# asker1 = Player(name="Green", suspicion=0.0)
# asker2 = Player(name="Red", suspicion=0.7)

# example_question1 = QuestionData(Player(name="Purple", suspicion=0.0), "What role are you?", asker1)
# example_question2 = QuestionData(Player(name="Purple", suspicion=0.0), "What role are you?", asker2)

# example_question3 = QuestionData(Player(name="Purple", suspicion=0.0), "Who are you suspicious of?", asker1)
# example_question4 = QuestionData(Player(name="Purple", suspicion=0.0), "Who are you suspicious of?", asker2)

# example_question5 = QuestionData(Player(name="Purple", suspicion=0.0), "Do you trust me?", asker1)
# example_question6 = QuestionData(Player(name="Purple", suspicion=0.0), "Do you trust me?", asker2)



# self_info = PlayerInfo("Purple", "Good", "Townsfolk")
# build_suspicions(example_history, starting_playerlist, llm, self_info)
# # nominate_player(example_history, example_suspicions3, llm, self_info)

# # vote_player(example_history, example_suspicions1, example_nominees1, llm, self_info)

# # request_information(example_history, example_suspicions1, llm, self_info)

# # answer_question(example_history, example_suspicions1, example_question1, llm, self_info)
# # answer_question(example_history, example_suspicions1, example_question2, llm, self_info)
# # answer_question(example_history, example_suspicions1, example_question3, llm, self_info)
# # answer_question(example_history, example_suspicions1, example_question4, llm, self_info)
# # answer_question(example_history, example_suspicions1, example_question5, llm, self_info)
# # answer_question(example_history, example_suspicions1, example_question6, llm, self_info)

# # make sure the llm knows who they actually are
# # clarify that suspicion is how suspicious the llm is of them, not how suspicious the player is feeling