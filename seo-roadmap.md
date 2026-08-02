# ADUCheatSheet.com — SEO Deployment Roadmap 🗺️

**Domaine :** aducheatsheet.com  
**Déploiement :** GitHub Pages (auto via push)  
**Stratégie :** Drip publishing progressif (anti-pénalité Google)

---

## 📏 RÈGLE STRICTE DE FRÉQUENCE (Drip Publishing)

- **Rythme :** 1 déploiement tous les **15 jours maximum**
- **Volume :** 50 villes par lot (après la Phase 3)
- **Objectif :** laisser Google indexer naturellement entre chaque phase, sans déclencher d'alerte anti-spam
- **Automatisation :** workflow GitHub Actions (1er et 16 de chaque mois à 06:00 UTC)

---

## PHASE 1 ✅ Déployé (28 Juillet 2026)

| Région | Villes | Nb |
|--------|--------|:--:|
| Californie | Bakersfield, Fresno, Modesto, Oceanside, Santa Rosa, Stockton, Vallejo | 7 |
| Colorado | Boulder, Fort Collins, Grand Junction, Greeley, Pueblo | 5 |
| Washington | Bellevue, Everett, Spokane, Tacoma, Vancouver, Yakima | 6 |
| **Total** | | **18** |

**Statut :** ✅ En ligne + indexée (Google Search Console)

---

## PHASE 2 ✅ Déployée (30 Juillet 2026 — en avance via script Stripe)

| Région | Villes | Nb |
|--------|--------|:--:|
| Californie | Riverside, San Bernardino, Santa Clarita, Oxnard, Glendale | 5 |
| Colorado | Aurora, Lakewood, Thornton, Arvada, Westminster | 5 |
| Washington | Kent, Renton, Federal Way, Kirkland, Redmond | 5 |
| Oregon | Eugene, Salem, Gresham, Hillsboro, Beaverton | 5 |
| **Total** | | **20** |

**Statut :** ✅ En ligne — **38 pages cumulées**

---

## 📅 PLAN 6 MOIS (Août 2026 — Janvier 2027)

### MOIS 1 — Août 2026 (→ ~120 pages)

| Phase | Date | Volume | Cibles | Cumul |
|:--:|----------|:--:|--------|:--:|
| **3** | Mi-août (16/08) | 35 | Texas (10) + Arizona (10) + CA/CO/WA/OR (15) | 73 |
| **4** | Fin août (01/09) | 50 | Villes 100k-300k hab., états pro-ADU | 123 |

### MOIS 2 — Septembre 2026 (→ ~220 pages)

| Phase | Date | Volume | Cibles | Cumul |
|:--:|----------|:--:|--------|:--:|
| **5** | 16/09 | 50 | Villes 50k-100k hab. (CA, WA, CO, OR, TX, AZ) | 173 |
| **6** | 01/10 | 50 | Villes 50k-100k hab. (CA, WA, CO, OR, TX, AZ) | 223 |

### MOIS 3 — Octobre 2026 (→ ~320 pages)

| Phase | Date | Volume | Cibles | Cumul |
|:--:|----------|:--:|--------|:--:|
| **7** | 16/10 | 50 | **Floride** + Caroline du Nord + Géorgie | 273 |
| **8** | 01/11 | 50 | Floride + NC + Géorgie (suite) | 323 |

### MOIS 4 — Novembre 2026 (→ ~420 pages)

| Phase | Date | Volume | Cibles | Cumul |
|:--:|----------|:--:|--------|:--:|
| **9** | 16/11 | 50 | Saturation États du Sud pro-ADU | 373 |
| **10** | 01/12 | 50 | Côte Est pro-ADU | 423 |

### MOIS 5 — Décembre 2026 (→ ~520 pages)

| Phase | Date | Volume | Cibles | Cumul |
|:--:|----------|:--:|--------|:--:|
| **11** | 16/12 | 50 | Marchés secondaires émergents | 473 |
| **12** | 01/01/2027 | 50 | Marchés secondaires (suite) | 523 |

### MOIS 6 — Janvier 2027 (→ 600+ pages)

| Phase | Date | Volume | Cibles | Cumul |
|:--:|----------|:--:|--------|:--:|
| **13** | 16/01/2027 | 50 | Complément couverture nationale | 573 |
| **14** | 01/02/2027 | 50 | **Seuil critique 600+ pages actives** | 623 |

---

## 📊 Projection

| Période | Pages cumulées |
|:-------|:--:|
| Fin Août 2026 | ~120 |
| Fin Septembre | ~220 |
| Fin Octobre | ~320 |
| Fin Novembre | ~420 |
| Fin Décembre | ~520 |
| Janvier 2027 | **600+** |

---

## ⚙️ AUTOMATISATION (workflow GitHub Actions)

- **Fichier :** `.github/workflows/drip-publish.yml`
- **Déclencheurs :**
  - Cron : 1er et 16 de chaque mois à 06:00 UTC
  - Manuel : `workflow_dispatch` (bouton « Run workflow » sur GitHub)
- **Actions automatiques :**
  1. Installe Python + dépendances (stripe, reportlab)
  2. Marque les N prochaines villes comme « à publier »
  3. Crée produits Stripe + Payment Links (pour les villes sans lien)
  4. Génère les fichiers HTML des villes publiées
  5. Régénère `index.html`
  6. Commit + push → **GitHub Pages déploie automatiquement**
- **Secret requis :** `STRIPE_KEY` (clé secrète Stripe live) dans Settings → Secrets du repo
