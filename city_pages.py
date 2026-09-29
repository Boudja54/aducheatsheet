#!/usr/bin/env python3
"""Construction des pages villes d'ADUCheatSheet — logique PARTAGEE.

Appele par generate.py (local, genere aussi les PDF) ET deploy_batch.py (CI GitHub
Actions). Regle du repo : les deux generateurs doivent rester IDENTIQUES — un correctif
applique a un seul des deux disparait au prochain passage du workflow automatique.

Ce module gere :
  * la lecture des donnees par ville (champs optionnels inclus) ;
  * la FAQ : les 3 FAQ historiques (faq1..faq3, qui contiennent leur propre question)
    plus des FAQ libres (champ "faqs") ; question/reponse separees proprement, plus de
    question affichee deux fois ;
  * le JSON-LD construit avec json.dumps (jamais a la main : les guillemets et sauts de
    ligne cassaient le schema) ;
  * le maillage interne : meme comte d'abord, puis meme etat, plus le hub /cities.html.
"""

import json
import re
from datetime import date

# Ancre du hub /cities.html (cities.html utilise le nom d'etat en minuscules en id)
STATE_ANCHOR = {
    "California": "california",
    "Washington": "washington",
    "Colorado": "colorado",
    "Oregon": "oregon",
    "Texas": "texas",
    "Arizona": "arizona",
}

DEFAULT_QUESTIONS = [
    "Can I build an ADU in {city}?",
    "How big can my ADU be in {city}?",
    "What about setbacks and other requirements in {city}?",
]

MAX_STATE_LINKS = 8


def slug(city: str) -> str:
    return city.lower().replace(" ", "-").replace("'", "")


def city_filename(city: str, state_abbr: str) -> str:
    return f"{slug(city)}-{state_abbr.lower()}.html"


def _qa(texte: str, defaut: str):
    """« Question ? Reponse » -> (question, reponse).

    Les donnees stockent la question en tete de la reponse : si on la garde telle
    quelle, la page affiche « <h4>Question ?</h4><p>Question ? Reponse ... ».
    """
    texte = (texte or "").strip()
    if not texte:
        return None
    if "?" in texte:
        q, a = texte.split("?", 1)
        q, a = q.strip(), a.strip()
        if q and a:
            return (q + "?", a)
    return (defaut, texte)


def faq_pairs(c: dict):
    """[(question, reponse)] : les 3 FAQ historiques puis les FAQ additionnelles."""
    paires = []
    for i, cle in enumerate(("faq1", "faq2", "faq3")):
        paire = _qa(c.get(cle, ""), DEFAULT_QUESTIONS[i].format(city=c["city"]))
        if paire:
            paires.append(paire)
    for extra in c.get("faqs", []) or []:
        q = (extra.get("q") or "").strip()
        a = (extra.get("a") or "").strip()
        if q and a:
            paires.append((q if q.endswith("?") else q + "?", a))
    return paires


def faq_html(c: dict) -> str:
    blocs = []
    for q, a in faq_pairs(c):
        blocs.append(f"  <h4>{q}</h4>\n  <p>{a}</p>")
    return "\n\n".join(blocs)


def faq_jsonld(c: dict):
    return [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        }
        for q, a in faq_pairs(c)
    ]


def sources_html(c: dict) -> str:
    """Sources officielles citees : credibilite (Google) + verifiabilite (lecteur)."""
    lignes = []
    for s in c.get("sources", []) or []:
        label = s.get("label", "")
        url = s.get("url", "")
        if label and url:
            lignes.append(f'      <li><a href="{url}" rel="nofollow noopener">{label}</a></li>')
    return "\n".join(lignes)


def related_html(c: dict, toutes) -> str:
    """Maillage interne : meme comte, puis meme etat, puis le hub complet."""
    morceaux = []

    comte = (c.get("county") or "").split("/")[0].strip()
    meme_comte = [
        x
        for x in toutes
        if x["city"] != c["city"]
        and comte
        and comte.lower() in (x.get("county") or "").lower()
    ]
    if meme_comte:
        liens = "\n".join(
            f'      <li><a href="/cities/{city_filename(x["city"], x["state_abbr"])}">'
            f'{x["city"]} ADU rules</a></li>'
            for x in sorted(meme_comte, key=lambda x: x["city"])[:12]
        )
        morceaux.append(
            f'    <h4 style="margin-bottom:6px;">More ADU guides in {comte}</h4>\n'
            f"    <ul>\n{liens}\n    </ul>"
        )

    meme_etat = [
        x
        for x in toutes
        if x["state_abbr"] == c["state_abbr"] and x["city"] != c["city"]
    ]
    deja = {x["city"] for x in meme_comte}
    reste = [x for x in sorted(meme_etat, key=lambda x: x["city"]) if x["city"] not in deja]
    if reste:
        liens = "\n".join(
            f'      <li><a href="/cities/{city_filename(x["city"], x["state_abbr"])}">'
            f'{x["city"]} ADU rules</a></li>'
            for x in reste[:MAX_STATE_LINKS]
        )
        morceaux.append(
            f"    <h4 style=\"margin-bottom:6px;\">More {c['state']} ADU city guides</h4>\n"
            f"    <ul>\n{liens}\n    </ul>"
        )

    total_etat = sum(1 for x in toutes if x["state_abbr"] == c["state_abbr"])
    ancre = STATE_ANCHOR.get(c["state"], c["state"].lower())
    morceaux.append(
        f'    <p><a href="/cities.html#{ancre}">See all {total_etat} {c["state"]} '
        f'ADU city guides</a> &middot; <a href="/cities.html">all {len(toutes)} cities, '
        f"6 states</a></p>"
    )
    return "\n".join(morceaux)


def build_page(c: dict, toutes, template: str, jour: str = "") -> str:
    """Rend la page HTML complete d'une ville."""
    jour = jour or date.today().strftime("%B %-d, %Y")

    parking = (c.get("parking") or "").lower()
    parking_row = ""
    if "required" in parking or "space" in parking:
        parking_row = (
            f'<tr><td><strong>Extra Parking Required</strong></td>'
            f'<td>{c["parking"]}</td></tr>'
        )

    occ = (c.get("occupancy") or "").strip()
    occ_row = ""
    if occ:
        occ_row = (
            f'<tr><td><strong>Owner Occupancy</strong></td>'
            f"<td>{occ}</td></tr>"
        )

    html = template[:]
    remplacements = {
        "[CITY]": c["city"],
        "[CITY-LOWER]": slug(c["city"]),
        "[STATE]": c["state"],
        "[STATE-LOWER]": c["state_abbr"].lower(),
        "[COUNTY]": c.get("county", ""),
        "[CITY_INTRO]": c.get("intro", ""),
        "[STATE_LAW]": c.get("state_law", "local zoning ordinances"),
        "[MAX_SIZE]": c.get("max_size", ""),
        "[SETBACKS]": c.get("setbacks", ""),
        "[PARKING_ROW]": parking_row,
        "[OCCUPANCY_ROW]": occ_row,
        "[ADDITIONAL_REQUIREMENTS]": c.get("additional", ""),
        "[LONG_CONTENT]": c.get("long_content", ""),
        "[FAQ_BLOCK]": faq_html(c),
        "[SOURCES_BLOCK]": sources_html(c),
        "[SOURCES_SECTION]": (
            "  <h3>Sources</h3>\n  <ul class=\"sources\">\n"
            + sources_html(c)
            + "\n  </ul>"
            if sources_html(c)
            else ""
        ),
        "[YEAR]": str(c.get("year", "2026")),
        "[H1]": c.get("h1") or f'{c["city"]} ADU Zoning Rules & Permit Guide',
        "[PRICE]": str(c.get("price", c.get("web_price", "12"))),
        "[STRIPE_CHECKOUT_URL]": c.get("stripe_checkout_url", ""),
        "[RELATED_CITIES]": related_html(c, toutes),
        "[LAST_UPDATED]": jour,
        "[STATE_ANCHOR]": STATE_ANCHOR.get(c["state"], c["state"].lower()),
        "[SEO_TITLE]": c.get("seo_title")
        or f'{c["city"]} ADU Requirements and Zoning Laws — {c["state"]} | ADUCheatSheet',
        "[SEO_DESC]": c.get("seo_desc")
        or (
            f'Complete {c["city"]} ADU zoning guide. Maximum size, setbacks, parking '
            f'rules, owner occupancy requirements in {c.get("county", "")}, {c["state"]}. '
            f"Download your city-specific PDF cheat sheet."
        ),
    }
    for cle, valeur in remplacements.items():
        html = html.replace(cle, valeur)

    seo_title = remplacements["[SEO_TITLE]"]
    seo_desc = remplacements["[SEO_DESC]"]
    geo = {
        "@type": "WebPage",
        "name": seo_title,
        "description": seo_desc,
        "url": f'https://aducheatsheet.com/cities/{city_filename(c["city"], c["state_abbr"])}',
        "isPartOf": {"@type": "WebSite", "name": "ADUCheatSheet", "url": "https://aducheatsheet.com"},
        "about": {
            "@type": "Thing",
            "name": f'Accessory dwelling unit rules in {c["city"]}, {c["state_abbr"]}',
        },
    }
    graph = [
        {"@type": "FAQPage", "mainEntity": faq_jsonld(c)},
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://aducheatsheet.com/"},
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": f'ADU guides by city',
                    "item": "https://aducheatsheet.com/cities.html",
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": f'{c["city"]}, {c["state_abbr"]}',
                    "item": f'https://aducheatsheet.com/cities/'
                    f'{city_filename(c["city"], c["state_abbr"])}',
                },
            ],
        },
        geo,
    ]
    schema = {
        "@context": "https://schema.org",
        "@graph": graph,
    }
    bloc = (
        '<script type="application/ld+json">\n'
        + json.dumps(schema, ensure_ascii=False, indent=None)
        + "\n</script>"
    )
    html = html.replace("</head>", bloc + "\n</head>", 1)
    reste = re.findall(r"\[[A-Z_]{3,}\]", html)
    if reste:
        print(f"  ⚠️  placeholders non remplaces dans {c['city']}: {sorted(set(reste))}")
    return html
