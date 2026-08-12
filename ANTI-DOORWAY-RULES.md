# ⚠️ RÈGLES ANTI-DOORWAY — ADUCheatSheet (mises à jour le 12/08/2026)

## ✅ CE QUI EST FAIT ET VALIDÉ

### FAQ uniques par ville (fait le 12/08)
- Champs `faq2` (taille max) et `faq3` (délais de permis) ajoutés aux 73 villes dans cities-data.json
- Générés par `enrich_faqs.py` : formulations variées choisies par hash déterministe du slug + délais réalistes par état (CA 8-12 semaines, CO 4-8, WA 6-10, OR 5-9, TX 6-12, AZ 4-8)
- Le template utilise `[FAQ_2]` et `[FAQ_3]` (plus de texte codé en dur)
- generate.py ET deploy_batch.py contiennent les remplacements (fallback si champ absent)

### Sitemap auto (fait le 12/08)
- `gen_sitemap.py` génère sitemap.xml avec TOUTES les villes publiées + 5 pages statiques
- Appelé automatiquement par deploy_batch.py après chaque batch
- Vérif : `python3 gen_sitemap.py` → doit afficher "38 villes + 5 pages = 43 URLs"

### Vérification anti-duplicate
- `check_duplicates.py` à la racine : vérifie intros, similarité entre paires, phrases répétées
- Résultat actuel : intros 0 doublon, FAQ 0 doublon, phrases répétées = uniquement lois d'état (normal, par état)

## 🚨 RÈGLES STRICTES POUR LES PROCHAINES PHASES

1. **NE JAMAIS lancer deploy_batch.py sans STRIPE_KEY en test** — il marque les villes `published=true` et les publie !
   - Le 12/08, un test a publié les 35 villes Phase 3 par erreur → corrigé (remises à published=false)
   - Pour tester : utiliser generate.py ou vérifier avec `--dry-run` mental (lire le code avant)
2. **TOUJOURS vérifier après génération** :
   - `python3 check_duplicates.py` → 0 doublon d'intro, 0 doublon de FAQ
   - `grep -c "cities/" index.html` → doit égaler le nombre de villes publiées (38)
   - `python3 gen_sitemap.py` → 43 URLs (38 villes + 5 statiques)
3. **Le flag `published` est le seul contrôle de publication** — un fichier HTML dans le repo SANS `published=true` n'est PAS exposé (pas lié dans l'index ni le sitemap)
4. **FAQ 3 (délais de permis)** : si une ville est ajoutée, lancer `enrich_faqs.py` pour régénérer les faq2/faq3
5. **Les pages Phase 3 (35 villes) sont dans le repo mais en attente** — elles se publieront via le workflow GitHub Actions le 16/08 (batch 50, Stripe Payment Links créés automatiquement)

## Template actuel
- `template-city.html` : FAQ avec [FAQ_1], [FAQ_2], [FAQ_3] — tous alimentés par cities-data.json
- Le disclaimer est EN BAS de page (avant les liens related cities) depuis le 12/08 — ne pas le remonter
