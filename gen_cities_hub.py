#!/usr/bin/env python3
"""Génère cities.html — hub listant TOUTES les villes ADU (répare le 404 du sitemap)."""
import json, datetime, re

BASE = "https://aducheatsheet.com"
OUT = "/root/aducheatsheet/cities.html"


def slug(s):
    return s.lower().replace(" ", "-").replace("'", "").replace(".", "")


def main():
    data = json.load(open("/root/aducheatsheet/cities-data.json"))
    cities = [c for c in data if c.get("published", True)]

    groups = {}
    for c in cities:
        key = (c["state"], c["state_abbr"])
        groups.setdefault(key, []).append(c)

    ordered = sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0][0]))
    n_cities, n_states = len(cities), len(ordered)

    nav = " &middot; ".join(
        f'<a href="#{slug(st)}">{abbr}</a>' for (st, abbr), _ in ordered
    )

    sections = []
    for (state, abbr), cs in ordered:
        cs = sorted(cs, key=lambda c: c["city"])
        items = "\n".join(
            f'      <li><a href="cities/{slug(c["city"])}-{c["state_abbr"].lower()}.html">'
            f'{c["city"]} ADU rules</a></li>'
            for c in cs
        )
        sections.append(
            f'  <section id="{slug(state)}" style="margin:26px 0;">\n'
            f'    <h2>{state} <span style="font-size:0.85rem;color:var(--text-light);">'
            f'({abbr} &middot; {len(cs)} cities)</span></h2>\n'
            f'    <ul style="columns:2;column-gap:28px;line-height:1.9;margin-top:8px;">\n'
            f'{items}\n'
            f'    </ul>\n'
            f'  </section>'
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>All {n_cities} ADU City Guides — ADU Zoning by City &amp; State | ADUCheatSheet</title>
  <meta name="description" content="Browse ADU zoning guides for {n_cities} US cities across {n_states} states. Maximum size, setbacks, parking and owner-occupancy rules — simplified, city by city.">
  <link rel="canonical" href="{BASE}/cities.html">
  <link rel="stylesheet" href="styles.css">
</head>
<body>

<header>
  <div class="container">
    <p><a href="/" style="color:white;opacity:0.8;text-decoration:none;">&larr; ADUCheatSheet.com</a></p>
    <h1>All ADU City Guides</h1>
    <p>{n_cities} cities across {n_states} states. Jump to your state: {nav}</p>
  </div>
</header>

<main class="container">

  <p style="color:var(--text-light);margin-top:20px;">Every city below has its own ADU cheat sheet: maximum size, setbacks, parking, owner-occupancy and permit steps — with the numbers your local planning department actually uses.</p>

{chr(10).join(sections)}

  <section style="margin-top:34px;padding:20px;background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);">
    <h2 style="margin-top:0;">Building ADUs for clients?</h2>
    <p style="color:var(--text-light);">Get the professional packs — multi-state master database and client-ready guides.</p>
    <p><a href="/pro/" style="font-weight:700;">See professional packs &rarr;</a></p>
  </section>

</main>

<footer style="margin-top:40px;padding:24px 0;background:var(--card-bg);border-top:1px solid var(--border);">
  <div class="container">
    <p style="font-size:0.85rem;color:var(--text-light);">
      <a href="/">Home</a> &middot;
      <a href="/cities.html">All cities</a> &middot;
      <a href="/privacy-policy.html">Privacy</a> &middot;
      <a href="/terms-of-service.html">Terms</a> &middot;
      <a href="/legal-disclaimer.html">Disclaimer</a>
    </p>
    <p style="font-size:0.8rem;color:var(--text-light);">&copy; {datetime.date.today().year} ADUCheatSheet.com</p>
  </div>
</footer>

</body>
</html>
"""
    open(OUT, "w").write(html)
    print(f"✅ cities.html généré : {n_cities} villes, {n_states} états → {OUT}")


if __name__ == "__main__":
    main()
