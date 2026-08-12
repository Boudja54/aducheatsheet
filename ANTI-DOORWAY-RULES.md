# ⚠️ RÈGLES ANTI-DOORWAY — ADUCheatSheet (apprises le 12/08/2026)

## Audit réalisé sur les 38 pages
- ✅ Intros : toutes UNIQUES (0 doublon) — garder cette règle
- ✅ Données de zonage : réelles et différentes par ville — garder
- ⚠️ FAQ génériques répétées sur 38/38 pages :
  - "Simple attached ADU conversions may be processed faster than new detached construction."
  - "Junior ADUs (JADUs) are limited to 500 square feet where permitted."
  - "Plan review in [CITY] typically takes 4 to 8 weeks..."
- ⚠️ Mentions de loi d'état (AB 68, HB 1337...) identiques PAR ÉTAT (12 CA, 11 WA, 10 CO)

## Règles pour les PROCHAINES pages (Phase 3 et +)
1. **FAQ UNIQUES par ville** : varier les délais de permis (ex: "4 to 6 weeks" vs "6 to 10 weeks" selon la ville réelle), varier les phrases JADU selon la politique locale
2. **Loi d'état** : garder la référence légale mais ajouter une phrase locale sur COMMENT la ville applique (ex: "Bakersfield processes simple conversions faster")
3. **Contenu local renforcé** : 1-2 phrases par ville sur la demande réelle (démographie, coût du logement, quartiers en développement ADU)
4. **Toujours vérifier** : après génération, comparer 2 pages au hasard — les intros, FAQ et sections locales doivent différer
5. Le script `check_duplicates.py` à la racine du repo fait la vérification automatique

## Template actuel
- `template-city.html` lignes 63-72 : FAQ avec [CITY], [MAX_SIZE], [FAQ_1]
- Le champ `faq1` dans cities-data.json alimente la première FAQ — les 2 autres sont codées en dur dans le template → à rendre dynamiques par ville
