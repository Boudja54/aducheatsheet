#!/usr/bin/env python3
"""Régénère sitemap.xml avec toutes les villes publiées (38 actuelles, plus à chaque batch).
Usage: python3 gen_sitemap.py
Appelé automatiquement par deploy_batch.py après chaque génération de batch.
"""
import json, os, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "cities-data.json")
OUT = os.path.join(ROOT, "sitemap.xml")

SITE = "https://aducheatsheet.com"
TODAY = datetime.date.today().isoformat()

STATIC_PAGES = [
    ("/", "weekly", "1.0"),
    ("/privacy-policy.html", "monthly", "0.3"),
    ("/terms-of-service.html", "monthly", "0.3"),
    ("/legal-disclaimer.html", "monthly", "0.3"),
    ("/legal-notice.html", "monthly", "0.3"),
]

def slug(city):
    return city.lower().replace(" ", "-").replace("'", "")

def main():
    with open(DATA, encoding="utf-8") as f:
        cities = json.load(f)

    published = [c for c in cities if c.get("published", False)]

    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for path, freq, prio in STATIC_PAGES:
        lines.append("  <url>")
        lines.append(f"    <loc>{SITE}{path}</loc>")
        lines.append(f"    <lastmod>{TODAY}</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{prio}</priority>")
        lines.append("  </url>")

    for c in published:
        fname = f"cities/{slug(c['city'])}-{c['state_abbr'].lower()}.html"
        lines.append("  <url>")
        lines.append(f"    <loc>{SITE}/{fname}</loc>")
        lines.append(f"    <lastmod>{TODAY}</lastmod>")
        lines.append("    <changefreq>monthly</changefreq>")
        lines.append("    <priority>0.8</priority>")
        lines.append("  </url>")

    lines.append("</urlset>")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"✅ sitemap.xml — {len(published)} villes + {len(STATIC_PAGES)} pages statiques = {len(published) + len(STATIC_PAGES)} URLs")

if __name__ == "__main__":
    main()
