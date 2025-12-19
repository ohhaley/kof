import pandas as pd
import re

column_names = ['name','role','prompt', 'reasoning', 'response', 'label']
data = pd.read_csv("finetune_game8.csv", header=None, names=column_names, sep=r"[[::]]", engine='python', on_bad_lines='skip')

data["name"]=data["name"].str[:-3]
data["role"]=data["role"].str[1:-3]
data["prompt"]=data["prompt"].str[1:-3]
data["reasoning"]=data["reasoning"].str[1:-3]
data["response"]=data["response"].str[1:-3]
data["label"]=data["label"].str[1:]

data["prompt"] = data["prompt"].str.replace("\"","")
data["prompt"] = data["prompt"].str.replace("\'","")
data["prompt"] = data["prompt"].str.replace("\\n","")
data["prompt"] = data["prompt"].str.replace("\\","")

data["reasoning"] = data["reasoning"].str.replace("\"","")
data["reasoning"] = data["reasoning"].str.replace("\'","")
data["reasoning"] = data["reasoning"].str.replace("\\n","")
data["reasoning"] = data["reasoning"].str.replace("\\","")

with open("systemprompt.md", 'r') as f: game_info = f.read()
data['prompt'] = data['prompt'].str.removeprefix(game_info)

print(data["prompt"].head())

f = open("test_ft_with_data.json","w")
f.write("[\n\n")
for i in range(0,data.shape[0]):
    f.write("{\"conversations\": [{\"from\": \"human\", \"value\": \n\"")
    f.write(data["prompt"][i])
    f.write("\"\n}, {\"from\": \"gpt\", \"value\": \n\"")
    f.write(data["reasoning"][i])
    f.write("\"\n}], \"source\": \"infini-instruct-top-500k\", \"score\":\n")
    f.write(data["label"][i])
    f.write("\n},\n\n")
    if "\"" in data["reasoning"][i]:
        print("Quote found!")
    if "\"" in data["reasoning"][i].strip("\""):
        print("Quote STILL found!")
f.write("\n\n]")
