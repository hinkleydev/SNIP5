import json

with open("data/snippets.json") as file:
    data = json.load(file)

print(data)
