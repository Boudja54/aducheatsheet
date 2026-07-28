#!/usr/bin/env python3
"""Stripe products creator - reads key from external file"""
import sys, json

# Read key from parts file
with open("/tmp/stripe_key_part.txt") as f:
    key = f.read().strip()

import stripe
stripe.api_key = key

with open("/root/aducheatsheet/cities-data.json") as f:
    cities = json.load(f)

prices = {"CA": 1200, "WA": 1400, "CO": 1400}

for i, c in enumerate(cities):
    city = c["city"]
    state = c["state_abbr"]
    title = f"The Ultimate {city} ADU Permit Cheat Sheet"
    slug = city.lower().replace(" ", "-")
    
    prod = stripe.Product.create(name=title, description=f"ADU guide for {city}, {state}")
    price = stripe.Price.create(product=prod.id, unit_amount=prices[state], currency="usd")
    
    sess = stripe.checkout.Session.create(
        mode="payment",
        line_items=[{"price": price.id, "quantity": 1}],
        success_url="https://aducheatsheet.com/",
        cancel_url=f"https://aducheatsheet.com/cities/{slug}-{state.lower()}.html"
    )
    
    c["stripe_checkout_url"] = sess.url
    c["stripe_product_id"] = prod.id
    c["stripe_price_id"] = price.id
    print(f"[{i+1}/18] {city} - ${prices[state]//100}")

with open("/root/aducheatsheet/cities-data.json", "w") as f:
    json.dump(cities, f, indent=2)

print(f"\nDone: {len(cities)} products")
