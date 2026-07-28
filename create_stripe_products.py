#!/usr/bin/env python3
"""
ONE-CLICK STRIPE SETUP
Copie-colle ceci dans le terminal :
python3 /root/aducheatsheet/create_stripe_products.py
"""
import stripe, json, os

# Ton API Key Stripe
stripe.api_key = os.environ.get("STRIPE_KEY", "")

with open("/root/aducheatsheet/cities-data.json") as f:
    cities = json.load(f)

prices = {"CA": 1200, "WA": 1400, "CO": 1400}

for i, c in enumerate(cities):
    city = c["city"]
    state = c["state_abbr"]
    slug = city.lower().replace(" ", "-")
    
    prod = stripe.Product.create(name=f"The Ultimate {city} ADU Permit Cheat Sheet", description=f"ADU guide for {city}, {state}")
    price = stripe.Price.create(product=prod.id, unit_amount=prices[state], currency="usd")
    sess = stripe.checkout.Session.create(
        mode="payment", line_items=[{"price": price.id, "quantity": 1}],
        success_url="https://aducheatsheet.com/",
        cancel_url=f"https://aducheatsheet.com/cities/{slug}-{state.lower()}.html"
    )
    c["stripe_checkout_url"] = sess.url
    c["stripe_product_id"] = prod.id
    c["stripe_price_id"] = price.id
    print(f"✅ {city} - ${prices[state]//100}")

with open("/root/aducheatsheet/cities-data.json", "w") as f:
    json.dump(cities, f, indent=2)

print(f"\n🎉 {len(cities)} produits Stripe crees !")
