#!/usr/bin/env python3
"""
ADU — Outreach B2B (Resend) pour la Master Database $197.
Cible : agents immobiliers et investisseurs très actifs dans les zones couvertes.
Usage : python3 outreach_b2b.py --dry-run | --send
"""
import csv, os, sys, time, json, urllib.request

RESEND_KEY = os.environ.get("RESEND_API_KEY", "")
FROM = "ADUCheatSheet <contact@aducheatsheet.com>"

SUBJECT = "The ADU zoning database your clients ask about"

BODY_TEMPLATE = """Hi {first_name},

I put together the exact ADU zoning database for {state} — every city's rules in one filterable file: max size, setbacks, parking, height.

Investors use it to instantly spot high-potential properties. Realtors use it to prove to buyers that a lot is ADU-eligible — and close faster.

It covers {city_count} cities across the states we track, with free updates for a year.

Full access: $197 (one-time) → https://aducheatsheet.com/pro/

Want to see a preview first? Happy to share a sample of the data.

Best,
ADUCheatSheet
"""

def send_email(to, first_name, state, city_count):
    body = BODY_TEMPLATE.format(first_name=first_name, state=state, city_count=city_count)
    payload = json.dumps({
        "from": FROM,
        "to": [to],
        "subject": SUBJECT,
        "html": body.replace("\n", "<br>"),
        "text": body,
    }).encode()
    req = urllib.request.Request("https://api.resend.com/emails", data=payload,
        headers={"Authorization": f"Bearer {RESEND_KEY}", "Content-Type": "application/json"})
    try:
        r = urllib.request.urlopen(req, timeout=30)
        d = json.loads(r.read())
        return True, d.get("id", "")
    except urllib.error.HTTPError as e:
        return False, e.read().decode()[:150]

def main():
    dry = "--dry-run" in sys.argv
    if not RESEND_KEY and not dry:
        print("❌ RESEND_API_KEY manquante")
        return

    # Prospecting list: agents/investors in covered states
    prospects = []
    if os.path.exists("/root/aducheatsheet/data/prospects.csv"):
        with open("/root/aducheatsheet/data/prospects.csv") as f:
            for row in csv.DictReader(f):
                prospects.append(row)
    else:
        # Fallback: create the file with the structure
        print("ℹ️ data/prospects.csv n'existe pas encore — créez-le avec: first_name,email,state")
        with open("/root/aducheatsheet/data/prospects.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["first_name", "email", "state"])
        return

    print(f"{'🔍 DRY-RUN' if dry else '📤 ENVOI'} : {len(prospects)} prospects")
    sent = 0
    for p in prospects[:25]:  # max 25/jour
        ok, info = (True, "dry") if dry else send_email(p["email"], p["first_name"], p["state"], "38")
        print(f"  {'✅' if ok else '❌'} {p['email']} ({p['state']}) {info[:40]}")
        if ok and not dry:
            sent += 1
            time.sleep(2)  # anti-spam
    print(f"✅ {sent} envoyés (max 25/jour)")

if __name__ == "__main__":
    main()
