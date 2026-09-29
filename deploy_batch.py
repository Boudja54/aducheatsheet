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

import city_pages  # rendu des pages villes — logique partagee avec generate.py (local)

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
    return city_pages.slug(city)

def city_filename(city, state):
    return city_pages.city_filename(city, state)

all_published = [c for c in cities if c.get("published", False)]
print(f"\n📄 Génération de {len(all_published)} pages HTML...")

os.makedirs(CITIES_DIR, exist_ok=True)

for c in all_published:
    html = city_pages.build_page(c, all_published, template)
    with open(os.path.join(CITIES_DIR, city_filename(c["city"], c["state_abbr"])), "w", encoding="utf-8") as f:
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
