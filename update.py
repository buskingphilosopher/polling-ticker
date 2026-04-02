import requests
import csv
import json
from io import StringIO

# Download mirrored polling data
url = "https://raw.githubusercontent.com/simonw/fivethirtyeight-polls/main/president_polls.csv"
response = requests.get(url)
response.raise_for_status()

# Read CSV
csv_data = StringIO(response.text)
reader = list(csv.DictReader(csv_data))

# Sort by most recent end date
reader.sort(key=lambda x: x.get("end_date") or "", reverse=True)

# Take the top 5 most recent
latest_polls = reader[:5]

headlines = []
for poll in latest_polls:
    try:
        candidate = poll["answer"]
        pct = poll.get("pct", "")
        state = poll.get("state", "") or "US"
        if pct != "":
            pct_val = float(pct)
            headlines.append(f"{candidate}: {pct_val:.0f}% ({state})")
    except Exception as e:
        # Skip any that fail
        continue

# Save to JSON
with open("/Users/sanderpriston/Documents/Websites/Polling Ticker/data.json", "w") as f:
    json.dump(headlines, f)
