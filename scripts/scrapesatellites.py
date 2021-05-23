import os
import json
import wikipedia
import pandas as pd

"""
Scrape satellite data from Wikipedia to match PRNs to a satellite description.
"""

url = wikipedia.page("List of GPS satellites").url
df = pd.read_html(url, header=0)[0]

names = df["Satellite"].to_list()
prns = df["PRN"].to_list()
statuses = df["Status"].to_list()

valid = {}
for idx, status in enumerate(statuses):
    if isinstance(status, str) and "operational" in status.lower():
        try:
            # throw out non-numbered PRNs
            int(prns[idx])
        except:
            continue
        # trim footnote markers
        valid[prns[idx]] = names[idx]

path = "satellites.json"
if os.path.exists(path):
    os.remove(path)
with open(path, "w") as f:
    json.dump(valid, f, indent=4)
