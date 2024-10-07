import json

with open('vlr90.json', 'r') as f:
    total_players = json.load(f)
p = []
for x in total_players:
    p.append(x["player"])
with open('playernames.json', 'w') as f:
    json.dump(p, f)