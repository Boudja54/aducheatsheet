#!/usr/bin/env python3
"""
ADU — Enrichit chaque ville avec faq2 + faq3 générées depuis SES données réelles.
Les questions sont personnalisées par ville (max_size, setbacks, parking, etc.)
"""
import json

DATA = "/root/aducheatsheet/cities-data.json"

def slug(s):
    return s.lower().replace(" ", "-").replace("'", "").replace(".", "")

def build_faqs(c):
    city = c["city"]
    faqs = {}
    
    # FAQ 2 : taille / surface (donnée réelle)
    max_size = c.get("max_size", "1,200")
    faqs["faq2"] = (
        f"What is the maximum ADU size allowed in {city}? "
        f"ADUs in {city} can be up to {max_size} square feet, "
        f"subject to the property's zoning and lot coverage limits. "
        f"Always confirm the exact allowed size with the {city} planning department before designing your project."
    )
    
    # FAQ 3 : setbacks ou parking selon ce qui existe
    setbacks = c.get("setbacks", "")
    parking = c.get("parking", "")
    if setbacks and "ft" in setbacks.lower():
        faqs["faq3"] = (
            f"What are the setback requirements for an ADU in {city}? "
            f"ADUs in {city} generally require setbacks of {setbacks}. "
            f"California state law (AB 68) limits local setback requirements to 4 feet "
            f"for existing structures, but always verify with local zoning."
        )
    elif parking and "not required" not in parking.lower():
        faqs["faq3"] = (
            f"Are ADUs in {city} required to include parking? "
            f"{parking.capitalize()}. Check with the {city} planning department for "
            f"the specific parking requirements that apply to your ADU project."
        )
    else:
        faqs["faq3"] = (
            f"How long does it take to get an ADU permit in {city}? "
            f"Permit timelines in {city} vary depending on the project complexity, "
            f"but California state law requires ministerial approval within 60 days "
            f"for qualifying ADUs. Contact the local building department for current processing times."
        )
    
    return faqs

def main():
    data = json.load(open(DATA))
    cities = data if isinstance(data, list) else data.get("cities", [])
    
    updated = 0
    for c in cities:
        faqs = build_faqs(c)
        for k, v in faqs.items():
            if not c.get(k) or len(c.get(k, "")) < 30:
                c[k] = v
                updated += 1
    
    # Sauvegarder
    with open(DATA, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ {updated} FAQ ajoutées/mises à jour sur {len(cities)} villes")

if __name__ == "__main__":
    main()
