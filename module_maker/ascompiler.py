import json

compiled = []

with open("input.aseditor", 'r') as f:
    data = f.readlines()

with open("module.json", 'w') as file:
    json.dump(data, file, indent=4)  # indent for pretty formatting

print("Data written")