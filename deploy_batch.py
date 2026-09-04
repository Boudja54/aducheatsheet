#!/usr/bin/env python3
"""
DRIP PUBLISHING AUTO-DEPLOYER
Exécuté par le workflow GitHub Actions tous les 15 jours.

Logique :
1. Charge cities-data.json
2. Prend les N prochaines villes non publiées (flag "published")
3. Pour chaque nouvelle ville : crée Produit Stripe + Prix + Payment Link (si pas déjà fait)
4. Marque "published": true
5. Génère les fichiers HTML pour TOUTES les villes publiées
6. Régénère index.html avec toutes les villes publiées
7. Sauvegarde cities-data.json
"""

import stripe, json, os, sys

# ============================================================
# CONFIG
# ============================================================
DATA_FILE = "cities-data.json"
TEMPLATE_FILE = "template-city.html"
CITIES_DIR = "cities"
PRICES = {"CA": 1200, "WA": 1400, "CO": 1400, "OR": 1200, "TX": 1400, "AZ": 1400}

stripe.api_key = os.environ.get("STRIPE_KEY", "")
if not stripe.api_key:
    print("⚠️  STRIPE_KEY absente — les nouveaux liens Stripe ne seront PAS créés (les villes garderont leur lien existant)")
    STRIPE_ACTIVE = False
else:
    STRIPE_ACTIVE = True

# Nombre de villes à publier ce cycle (défaut 50, paramétrable)
batch_size = int(os.environ.get("BATCH_SIZE", "50"))
print(f"🚀 Batch de déploiement : {batch_size} villes")

# ============================================================
# 1. CHARGER LES DONNÉES
# ============================================================
with open(DATA_FILE) as f:
    cities = json.load(f)

with open(TEMPLATE_FILE) as f:
    template = f.read()

published = [c for c in cities if c.get("published", False)]
pending = [c for c in cities if not c.get("published", False)]
print(f"📊 Déjà publiées : {len(published)} | En attente : {len(pending)}")

# ============================================================
# 2. SÉLECTIONNER LE LOT
# ============================================================
to_publish = pending[:batch_size]
if not to_publish:
    print("✅ Aucune nouvelle ville à publier ce cycle — rien à faire.")
    sys.exit(0)

print(f"🎯 Publication de {len(to_publish)} villes : {[c['city'] for c in to_publish]}")

# ============================================================
# 3. CRÉER LES PRODUITS STRIPE (Payment Links permanents)
# ============================================================
for c in to_publish:
    city, state = c["city"], c["state_abbr"]
    if c.get("stripe_checkout_url"):
        print(f"  ⏭️  {city} a déjà un lien Stripe, skip")
        continue
    if not STRIPE_ACTIVE:
        print(f"  ⚠️  {city} — pas de lien Stripe (clé absente), HTML généré sans CTA")
        continue
    price_cents = PRICES.get(state, 1200)
    try:
        prod = stripe.Product.create(
            name=f"The Ultimate {city} ADU Permit Cheat Sheet",
            description=f"ADU guide for {city}, {state}"
        )
        price = stripe.Price.create(product=prod.id, unit_amount=price_cents, currency="usd")
        link = stripe.PaymentLink.create(
            line_items=[{"price": price.id, "quantity": 1}],
            after_completion={"type": "redirect", "redirect": {"url": "https://aducheatsheet.com/"}},
        )
        c["stripe_checkout_url"] = link.url
        c["stripe_product_id"] = prod.id
        c["stripe_price_id"] = price.id
        print(f"  ✅ {city} → {link.url[:50]}...")
    except Exception as e:
        print(f"  ❌ {city} → {str(e)[:80]}")
        # On continue sans lien Stripe (page générée sans CTA)

# ============================================================
# 4. MARQUER COMME PUBLIÉ
# ============================================================
for c in to_publish:
    c["published"] = True

# ============================================================
# 5. GÉNÉRER LES HTML (toutes les villes publiées)
# ============================================================
def slug(city):
    return city.lower().replace(" ", "-").replace("'", "")

def city_filename(city, state):
    return f'{slug(city)}-{state.lower()}.html'

all_published = [c for c in cities if c.get("published", False)]
print(f"\n📄 Génération de {len(all_published)} pages HTML...")

os.makedirs(CITIES_DIR, exist_ok=True)

for c in all_published:
    html = template[:]
    related = [x for x in all_published if x["state_abbr"] == c["state_abbr"] and x["city"] != c["city"]]
    related_html = ""
    for r in related:
        related_html += f'<li><a href="/cities/{city_filename(r["city"], r["state_abbr"])}">{r["city"]}, {r["state_abbr"]}</a></li>\n'

    parking_row = ""
    if "required" in c.get("parking", "").lower() or "space" in c.get("parking", "").lower():
        parking_row = f'<tr><td><strong>Extra Parking Required</strong></td><td>{c["parking"]}</td></tr>'

    occ_row = ""
    if "required" in c.get("occupancy", "").lower():
        occ_row = f'<tr><td><strong>Owner Occupancy</strong></td><td>{c["occupancy"]}</td></tr>'
    elif "not" in c.get("occupancy", "").lower():
        occ_row = ""

    replacements = {
        "[CITY]": c["city"],
        "[CITY-LOWER]": slug(c["city"]),
        "[STATE]": c["state"],
        "[STATE-LOWER]": c["state_abbr"].lower(),
        "[COUNTY]": c.get("county", ""),
        "[CITY_INTRO]": c.get("intro", ""),
        "[STATE_LAW]": c.get("state_law", "local zoning ordinances"),
        "[MAX_SIZE]": c["max_size"],
        "[SETBACKS]": c["setbacks"],
        "[PARKING_ROW]": parking_row,
        "[OCCUPANCY_ROW]": occ_row,
        "[ADDITIONAL_REQUIREMENTS]": c.get("additional", ""),
        "[FAQ_1]": c.get("faq1", ""),
        "[FAQ_2]": c.get("faq2", ""),
        "[FAQ_3]": c.get("faq3", ""),
        "[YEAR]": c.get("year", "2026"),
        "[PRICE]": c.get("web_price", "12"),
        "[STRIPE_CHECKOUT_URL]": c.get("stripe_checkout_url", ""),
        "[RELATED_CITIES]": related_html,
    }
    for old, new in replacements.items():
        html = html.replace(old, new)

    # SCHEMA.ORG JSON-LD (SEO : extraits enrichis Google) — même bloc que generate.py
    faq_items = ""
    for q in [c.get("faq1", ""), c.get("faq2", ""), c.get("faq3", "")]:
        if q and len(q) > 30:
            q_clean = q[:300].replace('"', "'")
            q_name = q.split("?")[0][:90].strip()
            if q_name:
                faq_items += f'{{"@type":"Question","name":"{q_name}?","acceptedAnswer":{{"@type":"Answer","text":"{q_clean}"}}}},'
    schema_json = f'''<script type="application/ld+json">
{{"@context":"https://schema.org",
"@graph":[
{{"@type":"FAQPage","mainEntity":[{faq_items.rstrip(",")}]}},
{{"@type":"LocalBusiness","name":"ADUCheatSheet - {c["city"]} ADU Guide",
"description":"{c["city"]} ADU requirements and zoning laws for {c["state"]}",
"areaServed":"{c["city"]}, {c["state_abbr"]}",
"url":"https://aducheatsheet.com/cities/{city_filename(c["city"], c["state_abbr"])}",
"address":{{"@type":"PostalAddress","addressLocality":"{c["city"]}","addressRegion":"{c["state_abbr"]}","addressCountry":"US"}}}}
]}}
</script>'''
    html = html.replace("</head>", schema_json + "\n</head>")

    with open(os.path.join(CITIES_DIR, city_filename(c["city"], c["state_abbr"])), "w") as f:
        f.write(html)
    print(f"  ✅ {city_filename(c['city'], c['state_abbr'])}")

# ============================================================
# 6. RÉGÉNÉRER INDEX.HTML (sections par état)
# ============================================================
print("\n🏠 Régénération de index.html...")
if os.path.exists("index.html"):
    with open("index.html") as f:
        index = f.read()

    # Grouper les villes par état
    states_order = []
    by_state = {}
    for c in all_published:
        abbr = c["state_abbr"]
        if abbr not in by_state:
            by_state[abbr] = []
            states_order.append(abbr)
        by_state[abbr].append(c)

    # Construire les sections par état
    sections = ""
    for abbr in states_order:
        state_name = by_state[abbr][0]["state"]
        sections += f'\n    <!-- ===== {state_name.upper()} ===== -->\n    <div class="state-section">\n      <h2>📍 {state_name}</h2>\n      <div class="city-grid">\n'
        for c in by_state[abbr]:
            sections += f'''        <a href="cities/{city_filename(c['city'], c['state_abbr'])}" class="city-card">
          <span class="state-badge">{abbr}</span>
          <h3>{c["city"]}</h3>
          <p>ADU rules, permits &amp; zoning</p>
        </a>
'''
        sections += '      </div>\n    </div>\n'

    # Remplacer le bloc entre les marqueurs
    if "<!-- STATES_START -->" in index and "<!-- STATES_END -->" in index:
        import re
        index = re.sub(r'<!-- STATES_START -->.*?<!-- STATES_END -->',
                       f'<!-- STATES_START -->{sections}    <!-- STATES_END -->',
                       index, flags=re.DOTALL)
        with open("index.html", "w") as f:
            f.write(index)
        print("  ✅ index.html mis à jour (bloc STATES_START/END)")
    else:
        print("  ⚠️  Marqueurs STATES_START/END absents — index.html non modifié (à vérifier manuellement)")

# ============================================================
# 7. SAUVEGARDER
# ============================================================
with open(DATA_FILE, "w") as f:
    json.dump(cities, f, indent=2)
print(f"\n🎉 Terminé ! {len(to_publish)} villes publiées ce cycle. Total en ligne : {len(all_published)}")
