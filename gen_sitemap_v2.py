#!/usr/bin/env python3
"""Génère le sitemap.xml complet (73 villes + pages principales)."""
import json, os, datetime

BASE = "https://aducheatsheet.com"
OUT = "/root/aducheatsheet/sitemap.xml"

def slug(s):
    return s.lower().replace(" ", "-").replace("'", "").replace(".", "")

def main():
    data = json.load(open("/root/aducheatsheet/cities-data.json"))
    cities = data if isinstance(data, list) else data.get("cities", [])
    today = datetime.date.today().isoformat()

    urls = [
        {"loc": BASE + "/", "priority": "1.0"},
        {"loc": BASE + "/cities.html", "priority": "0.9"},
    ]
    for c in cities:
        if c.get("published", True):
            fname = f"{slug(c['city'])}-{c['state_abbr'].lower()}.html"
            urls.append({"loc": f"{BASE}/cities/{fname}", "priority": "0.8"})

    with open(OUT, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in urls:
            f.write(f"  <url>\n    <loc>{u['loc']}</loc>\n    <lastmod>{today}</lastmod>\n    <priority>{u['priority']}</priority>\n  </url>\n")
        f.write("</urlset>\n")

    print(f"✅ Sitemap généré: {len(urls)} URLs → {OUT}")

if __name__ == "__main__":
    main()
