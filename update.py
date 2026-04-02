import requests
import csv
import json
from io import StringIO

url = "https://raw.githubusercontent.com/simonw/fivethirtyeight-polls/main/president_polls.csv"

headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"Error fetching data: {e}")
    exit(1)

# Read CSV into a list of dictionaries
csv_data = StringIO(response.text)
reader = list(csv.DictReader(csv_data))

# Sort polls by enddate (newest first)
reader.sort(key=lambda x: x.get('enddate', ''), reverse=True)

# Take the latest 5 polls
latest_polls = reader[:5]

# Short codes for pollsters
pollster_codes = {
    "YouGov": "YGVG",
    "The New York Times/Siena College": "NYTS",
    "ABC News/The Washington Post": "ABCW",
    "Marquette University Law School": "MARQ",
    "Monmouth University Polling Institute": "MONU",
    "SurveyUSA": "SVYU",
    "Trafalgar Group": "TRAF",
    "Emerson College Polling": "EMRC",
    "Quinnipiac University": "QUIN",
    "Ipsos": "IPSOS",
    "Rasmussen Reports": "RASM",
    "NBC News/Wall Street Journal": "NBCW",
    "CNN/ORC": "CNN",
    "Gallup": "GALL",
    "Pew Research Center": "PEWR",
    "Economist/YouGov": "ECNY",
    "JL Partners": "JLP"
}

polls_structured = []
for poll in latest_polls:
    try:
        candidate = poll.get('answer', 'Unknown')
        pct = float(poll.get('pct', 0))
        state = poll.get('state') or "US"
        pollster_name = poll.get('pollster', 'Unknown')
        # Map to code, or first 4 letters if unknown
        pollster_code = pollster_codes.get(pollster_name, pollster_name[:4].upper())
        polls_structured.append({
            "candidate": candidate,
            "pct": pct,
            "state": state,
            "pollster": pollster_code
        })
    except (ValueError, TypeError):
        continue

# Save to JSON
output_file = "/Users/sanderpriston/Documents/Websites/Polling Ticker/data.json"
with open(output_file, "w") as f:
    json.dump(polls_structured, f, indent=2)

print(f"Successfully updated {output_file}")
