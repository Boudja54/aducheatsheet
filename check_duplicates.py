#!/usr/bin/env python3
"""Vérification anti-doorway sur ADUCheatSheet : compare le contenu des 38 pages villes."""
import re, urllib.request, json

BASE = "https://aducheatsheet.com/cities/"

# Liste des slugs depuis le repo local
with open("/tmp/adu/cities-data.json") as f:
    cities = json.load(f)

published = [c for c in cities if c.get("published", False)]
print(f"📊 {len(published)} pages publiées à vérifier\n")

def get_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req, timeout=20).read().decode()
    text = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
    text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    return re.sub(r'\s+', ' ', text)

pages = {}
for c in published:
    slug = c["city"].lower().replace(" ", "-").replace("'", "")
    fname = f"{slug}-{c['state_abbr'].lower()}.html"
    try:
        pages[c["city"]] = get_text(BASE + fname)
    except Exception as e:
        pages[c["city"]] = f"ERROR: {e}"

# 1. Vérifier les intros (premier paragraphe après le H2)
print("=== 1. INTROS UNIQUES ? ===")
intros = {}
for city, text in pages.items():
    if text.startswith("ERROR"):
        print(f"  ❌ {city}: {text}")
        continue
    # Trouver le premier paragraphe après "ADU Regulations in"
    m = re.search(r'ADU Regulations in [^,]+, \w+ ([^A-Z]{0,10}?)Located', text)
    # Extraction plus robuste : le paragraphe après le h2
    idx = text.find("ADU Regulations in")
    if idx >= 0:
        # Chercher le premier point final après le début du paragraphe suivant
        par = text[idx+len("ADU Regulations in X, Y"):]
        # prendre environ 200 chars du début de l'intro
        start = text.find("Located", idx)
        if start >= 0:
            intros[city] = text[start:start+150]

dup_intros = {}
for city, intro in intros.items():
    for other, other_intro in intros.items():
        if city != other and intro[:80] == other_intro[:80]:
            dup_intros.setdefault(city, []).append(other)

if dup_intros:
    print(f"  ⚠️ {len(dup_intros)} intros dupliquées:")
    for city, dups in list(dup_intros.items())[:8]:
        print(f"    {city} ≈ {', '.join(dups)}")
else:
    print("  ✅ Toutes les intros sont uniques")

# 2. Comparaison globale par paires (pourcentage de similarité)
print("\n=== 2. SIMILARITÉ GLOBALE ENTRE PAGES ===")
high_sim = []
texts = [(city, t) for city, t in pages.items() if not t.startswith("ERROR")]
for i in range(len(texts)):
    for j in range(i+1, len(texts)):
        c1, t1 = texts[i]
        c2, t2 = texts[j]
        # Similarité simple : chevauchement de phrases
        s1 = set(re.findall(r'[^.]{30,}\.', t1))
        s2 = set(re.findall(r'[^.]{30,}\.', t2))
        if not s1 or not s2:
            continue
        common = len(s1 & s2)
        sim = common / min(len(s1), len(s2))
        if sim > 0.3:
            high_sim.append((c1, c2, round(sim*100)))

high_sim.sort(key=lambda x: -x[2])
if high_sim:
    print(f"  ⚠️ {len(high_sim)} paires avec >30% de phrases communes:")
    for c1, c2, sim in high_sim[:12]:
        print(f"    {c1} ~ {c2} : {sim}%")
else:
    print("  ✅ Aucune paire au-dessus de 30%")

# 3. Phrases template répétées (présentes dans beaucoup de pages)
print("\n=== 3. PHRASES RÉPÉTÉES DANS BEAUCOUP DE PAGES ===")
phrase_count = {}
for city, text in texts:
    for phrase in set(re.findall(r'[A-Z][^.]{60,200}\.', text)):
        phrase_count[phrase] = phrase_count.get(phrase, 0) + 1

suspicious = [(p, n) for p, n in phrase_count.items() if n >= 6]
suspicious.sort(key=lambda x: -x[1])
if suspicious:
    print(f"  ⚠️ {len(suspicious)} phrases présentes dans ≥6 pages:")
    for p, n in suspicious[:8]:
        print(f"    [{n}/38] {p[:100]}")
else:
    print("  ✅ Aucune phrase suspecte répétée")

print("\n=== RÉSUMÉ ===")
print(f"Pages analysées: {len(texts)}/{len(published)}")
print(f"Intros dupliquées: {len(dup_intros)}")
print(f"Paires >30% similaires: {len(high_sim)}")
print(f"Phrases répétées ≥6 pages: {len(suspicious)}")
