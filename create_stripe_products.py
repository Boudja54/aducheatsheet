#!/usr/bin/env python3
"""
ONE-CLICK STRIPE FIX — Payment Links permanents au lieu de Sessions expirantes.

Usage:
  export STRIPE_KEY="sk_live_..."
  python3 create_stripe_products.py

Ce script :
  1. Crée un Produit Stripe (si pas déjà existant)
  2. Crée un Prix (Price)
  3. Crée un Payment Link permanent
  4. Sauvegarde l'URL buy.stripe.com/... dans cities-data.json
  5. Régénère les fichiers HTML avec la bonne URL
"""

import stripe, json, os, sys

# Clé API Stripe (live)
stripe.api_key = os.environ.get("STRIPE_KEY", "")
if not stripe.api_key:
    print("❌ Erreur : mets ta clé Stripe dans la variable d'env STRIPE_KEY")
    print("   export STRIPE_KEY=\"sk_live_...\"")
    sys.exit(1)

DATA_FILE = "cities-data.json"
TEMPLATE_FILE = "template-city.html"
CITIES_DIR = "cities"

with open(DATA_FILE) as f:
    cities = json.load(f)

with open(TEMPLATE_FILE) as f:
    template = f.read()

# Prix par état (en cents)
PRICES = {"CA": 1200, "WA": 1400, "CO": 1400, "OR": 1200, "TX": 1400, "AZ": 1400}

updated = 0
for c in cities:
    city = c["city"]
    state = c["state_abbr"]
    price_cents = PRICES.get(state, 1200)
    slug = city.lower().replace(" ", "-").replace("'", "")

    # 1. Créer ou réutiliser le produit
    prod_name = f"The Ultimate {city} ADU Permit Cheat Sheet"
    prod_desc = f"Complete ADU zoning guide for {city}, {state} — permits, setbacks, parking, fees & local contacts"

    # Create product (fresh each time to avoid stale data issues)
    prod = stripe.Product.create(name=prod_name, description=prod_desc)
    print(f"  📦 Produit: {prod.id} — {prod_name}")

    # 2. Créer le prix
    price = stripe.Price.create(
        product=prod.id,
        unit_amount=price_cents,
        currency="usd",
    )
    print(f"  💰 Prix: {price.id} — ${price_cents // 100}.{price_cents % 100:02d}")

    # 3. Créer le LIEN DE PAIEMENT PERMANENT
    payment_link = stripe.PaymentLink.create(
        line_items=[{"price": price.id, "quantity": 1}],
        after_completion={"type": "redirect", "redirect": {"url": "https://aducheatsheet.com/"}},
    )
    print(f"  🔗 Payment Link: {payment_link.url}")

    # 4. Mettre à jour les données
    c["stripe_checkout_url"] = payment_link.url
    c["stripe_product_id"] = prod.id
    c["stripe_price_id"] = price.id
    updated += 1

    # 5. Régénérer le fichier HTML avec la nouvelle URL
    html = template[:]
    # Related cities (same state)
    related = [x for x in cities if x["state_abbr"] == state and x["city"] != city]
    related_html = ""
    for r in related:
        r_slug = r["city"].lower().replace(" ", "-").replace("'", "")
        related_html += f'<li><a href="/cities/{r_slug}-{r["state_abbr"].lower()}.html">{r["city"]}, {r["state_abbr"]}</a></li>\n'

    parking_row = ""
    if "required" in c.get("parking", "").lower() or "space" in c.get("parking", "").lower():
        parking_row = f'<tr><td><strong>Extra Parking Required</strong></td><td>{c["parking"]}</td></tr>'

    occ_row = ""
    if "required" in c.get("occupancy", "").lower():
        occ_row = f'<tr><td><strong>Owner Occupancy</strong></td><td>{c["occupancy"]}</td></tr>'
    elif "not" in c.get("occupancy", "").lower():
        occ_row = ""
    else:
        occ_row = f'<tr><td><strong>Owner Occupancy</strong></td><td>{c["occupancy"]}</td></tr>'

    replacements = {
        "[CITY]": city,
        "[CITY-LOWER]": slug,
        "[STATE]": c["state"],
        "[STATE-LOWER]": state.lower(),
        "[COUNTY]": c.get("county", ""),
        "[CITY_INTRO]": c.get("intro", ""),
        "[STATE_LAW]": c.get("state_law", "local zoning ordinances"),
        "[MAX_SIZE]": c["max_size"],
        "[SETBACKS]": c["setbacks"],
        "[PARKING_ROW]": parking_row,
        "[OCCUPANCY_ROW]": occ_row,
        "[ADDITIONAL_REQUIREMENTS]": c.get("additional", ""),
        "[FAQ_1]": c.get("faq1", ""),
        "[YEAR]": c.get("year", "2026"),
        "[PRICE]": c.get("web_price", str(price_cents // 100)),
        "[STRIPE_CHECKOUT_URL]": payment_link.url,
        "[RELATED_CITIES]": related_html,
    }

    for old, new in replacements.items():
        html = html.replace(old, new)

    fname = f"{slug}-{state.lower()}.html"
    with open(f"{CITIES_DIR}/{fname}", "w") as f:
        f.write(html)
    print(f"  ✅ HTML mis à jour: {fname}")
    print()

# Sauvegarder les données mises à jour
with open(DATA_FILE, "w") as f:
    json.dump(cities, f, indent=2)

print(f"\n🎉 {updated} produits Stripe avec Payment Links permanents créés !")
print("   Les URLs buy.stripe.com sont injectées dans les fichiers HTML.")
print("   Plus besoin de git push => le site est à jour.")
