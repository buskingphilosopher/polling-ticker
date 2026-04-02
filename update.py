import requests
import csv
import json
from io import StringIO

# Download polling data
url = "https://raw.githubusercontent.com/fivethirtyeight/data/master/polls/president_polls.csv"
response = requests.get(url)
response.raise_for_status()

# Read CSV
csv_data = StringIO(response.text)
reader = list(csv.DictReader(csv_data))

# Get the latest 5 polls
reader.sort(key=lambda x: x['enddate'], reverse=True)
latest_polls = reader[:5]

headlines = []
for poll in latest_polls:
    try:
        candidate = poll['answer']
        pct = float(poll['pct'])
        state = poll['state'] if poll['state'] else "US"
        text = f"{candidate}: {pct:.0f}% ({state})"
        headlines.append(text)
    except (KeyError, ValueError):
        continue

# Save to JSON
with open('data.json', 'w') as f:
    json.dump(headlines, f)
