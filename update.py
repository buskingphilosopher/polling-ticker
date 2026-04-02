import requests
from bs4 import BeautifulSoup
import json

url = "https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_United_Kingdom_general_election"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Find the first polling table
table = soup.find("table", {"class": "wikitable"})

rows = table.find_all("tr")[1:6]  # latest 5 rows (top of table)

polls = []

for row in rows:
    cells = row.find_all(["td", "th"])
    try:
        pollster = cells[1].text.strip()
        lab = cells[2].text.strip()
        con = cells[3].text.strip()
        ld = cells[4].text.strip()

        polls.append({
            "pollster": pollster[:4].upper(),
            "candidate": f"LAB {lab} / CON {con} / LD {ld}",
            "pct": 0,
            "state": "UK"
        })

    except:
        continue

# Save to JSON
with open("data.json", "w") as f:
    json.dump(polls, f, indent=2)

print("Updated UK polling data")
