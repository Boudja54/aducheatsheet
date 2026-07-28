#!/usr/bin/env python3
"""
ADUCheatSheet.com — Programmatic HTML Generator
Reads cities-data.json and generates city HTML pages + index.html
"""

import json, os, re

DATA_FILE = "cities-data.json"
TEMPLATE_FILE = "template-city.html"
CITIES_DIR = "cities"
INDEX_FILE = "index.html"

with open(DATA_FILE) as f:
    cities = json.load(f)

with open(TEMPLATE_FILE) as f:
    template = f.read()

def slug(city):
    return city.lower().replace(" ", "-").replace("'", "")

os.makedirs(CITIES_DIR, exist_ok=True)

for c in cities:
    html = template[:]
    
    replacements = {
        "[CITY]": c["city"],
        "[CITY-LOWER]": slug(c["city"]),
        "[STATE]": c["state"],
        "[STATE-LOWER]": c["state_abbr"].lower(),
        "[MAX_SIZE]": c["max_size"],
        "[SETBACKS]": c["setbacks"],
        "[PARKING]": c["parking"],
        "[OCCUPANCY]": c["occupancy"],
        "[ADDITIONAL_REQUIREMENTS]": c["additional"],
        "[FAQ_1]": c["faq1"],
        "[YEAR]": c.get("year", "2026"),
        "[PRICE]": c.get("price", "12"),
        "[PAYHIP_LINK_CITY]": c["payhip_link"],
    }
    
    for old, new in replacements.items():
        html = html.replace(old, new)
    
    # Generate related cities list (same state)
    related = [x for x in cities if x["state_abbr"] == c["state_abbr"] and x["city"] != c["city"]]
    related_html = ""
    for r in related:
        related_html += f'<li><a href="/cities/{slug(r["city"])}-{r["state_abbr"].lower()}.html">{r["city"]}, {r["state_abbr"]}</a></li>\n'
    html = html.replace("[RELATED_CITIES]", related_html)
    
    filename = f'{CITIES_DIR}/{slug(c["city"])}-{c["state_abbr"].lower()}.html'
    with open(filename, "w") as f:
        f.write(html)
    print(f"✅ Generated: {filename}")

print(f"\n🎉 {len(cities)} city pages generated!")
