import json

headlines = [
    "Labour +4 this week ↑",
    "Economy top issue (62%)",
    "Conservatives -2 among under 30s"
]

with open('data.json', 'w') as f:
    json.dump(headlines, f)