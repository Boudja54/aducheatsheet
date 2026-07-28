#!/usr/bin/env python3
"""Update cities-data.json with premium (Niveau 2) data fields."""

import json

with open("cities-data.json") as f:
    cities = json.load(f)

# Standard premium data templates by state
premium_data = {
    "CA": {
        "dept_name": "Planning & Building Department",
        "dept_name_short": "Building & Safety",
        "links": {
            "permit_form": "https://www.bakersfieldcity.us/426/Building-Permits-Inspections",
            "zoning_map": "https://www.bakersfieldcity.us/609/Zoning-Maps",
            "city_website": "https://www.bakersfieldcity.us"
        },
        "fees": {
            "permit_fee": "500-1,500",
            "impact_fee": "2,000-5,000",
            "plan_check": "200-800"
        }
    },
    "WA": {
        "dept_name": "Planning & Community Development",
        "dept_name_short": "Permit Center",
        "fees": {"permit_fee": "600-2,000", "impact_fee": "1,500-4,000", "plan_check": "300-900"},
        "links": {
            "permit_form": "https://www.spokanecity.org/services/permits/",
            "zoning_map": "https://www.spokanecity.org/services/maps/",
            "city_website": "https://www.spokanecity.org"
        }
    },
    "CO": {
        "dept_name": "Planning & Development Services",
        "dept_name_short": "Permit Center",
        "fees": {"permit_fee": "400-1,800", "impact_fee": "1,000-3,500", "plan_check": "250-750"},
        "links": {
            "permit_form": "https://www.fcgov.com/development/",
            "zoning_map": "https://www.fcgov.com/gis/",
            "city_website": "https://www.fcgov.com"
        }
    }
}

# City-specific contact info
city_contacts = {
    "Bakersfield": {"phone": "(661) 326-3711", "email": "planning@bakersfieldcity.us", "address": "1715 Chester Ave, Bakersfield, CA 93301", "links": {"permit_form": "https://www.bakersfieldcity.us/426/Building-Permits-Inspections", "zoning_map": "https://www.bakersfieldcity.us/609/Zoning-Maps", "city_website": "https://www.bakersfieldcity.us"}},
    "Fresno": {"phone": "(559) 621-8000", "email": "planning@fresno.gov", "address": "2600 Fresno St, Fresno, CA 93721", "links": {"permit_form": "https://www.fresno.gov/darm/building-permits/", "zoning_map": "https://www.fresno.gov/planning/zoning-map/", "city_website": "https://www.fresno.gov"}},
    "Modesto": {"phone": "(209) 577-5200", "email": "planning@modestogov.com", "address": "1010 10th St, Modesto, CA 95354", "links": {"permit_form": "https://www.modestogov.com/272/Building-Permits", "zoning_map": "https://www.modestogov.com/145/Zoning", "city_website": "https://www.modestogov.com"}},
    "Stockton": {"phone": "(209) 937-8270", "email": "planning@stocktonca.gov", "address": "425 N El Dorado St, Stockton, CA 95202", "links": {"permit_form": "https://www.stocktonca.gov/348/Permits", "zoning_map": "https://www.stocktonca.gov/636/Zoning", "city_website": "https://www.stocktonca.gov"}},
    "Santa Rosa": {"phone": "(707) 543-3200", "email": "planning@srcity.org", "address": "100 Santa Rosa Ave, Santa Rosa, CA 95404", "links": {"permit_form": "https://srcity.org/269/Permit-Center", "zoning_map": "https://srcity.org/271/Zoning-Information", "city_website": "https://srcity.org"}},
    "Oceanside": {"phone": "(760) 435-3500", "email": "planning@oceansideca.org", "address": "300 N Coast Hwy, Oceanside, CA 92054", "links": {"permit_form": "https://www.oceansideca.org/planning", "zoning_map": "https://www.oceansideca.org/gis", "city_website": "https://www.oceansideca.org"}},
    "Vallejo": {"phone": "(707) 648-4321", "email": "planning@cityofvallejo.net", "address": "555 Santa Clara St, Vallejo, CA 94590", "links": {"permit_form": "https://www.cityofvallejo.net/building", "zoning_map": "https://www.cityofvallejo.net/planning", "city_website": "https://www.cityofvallejo.net"}},
    "Spokane": {"phone": "(509) 625-6300", "email": "planning@spokanecity.org", "address": "808 W Spokane Falls Blvd, Spokane, WA 99201", "links": {"permit_form": "https://my.spokanecity.org/permits/", "zoning_map": "https://my.spokanecity.org/gis/", "city_website": "https://my.spokanecity.org"}},
    "Tacoma": {"phone": "(253) 591-5000", "email": "planning@cityoftacoma.org", "address": "747 Market St, Tacoma, WA 98402", "links": {"permit_form": "https://www.cityoftacoma.org/permits", "zoning_map": "https://www.cityoftacoma.org/gis", "city_website": "https://www.cityoftacoma.org"}},
    "Vancouver": {"phone": "(360) 487-8000", "email": "planning@cityofvancouver.us", "address": "415 W 6th St, Vancouver, WA 98660", "links": {"permit_form": "https://www.cityofvancouver.us/permits", "zoning_map": "https://www.cityofvancouver.us/gis", "city_website": "https://www.cityofvancouver.us"}},
    "Bellevue": {"phone": "(425) 452-6800", "email": "planning@bellevuewa.gov", "address": "450 110th Ave NE, Bellevue, WA 98004", "links": {"permit_form": "https://permits.bellevuewa.gov/", "zoning_map": "https://bellevuewa.gov/gis", "city_website": "https://bellevuewa.gov"}},
    "Everett": {"phone": "(425) 257-8700", "email": "planning@everettwa.gov", "address": "2930 Wetmore Ave, Everett, WA 98201", "links": {"permit_form": "https://www.everettwa.gov/permits", "zoning_map": "https://www.everettwa.gov/gis", "city_website": "https://www.everettwa.gov"}},
    "Yakima": {"phone": "(509) 575-6000", "email": "planning@yakimawa.gov", "address": "129 N 2nd St, Yakima, WA 98901", "links": {"permit_form": "https://www.yakimawa.gov/permits", "zoning_map": "https://www.yakimawa.gov/gis", "city_website": "https://www.yakimawa.gov"}},
    "Fort Collins": {"phone": "(970) 221-6500", "email": "planning@fcgov.com", "address": "281 N College Ave, Fort Collins, CO 80524", "links": {"permit_form": "https://www.fcgov.com/permits", "zoning_map": "https://www.fcgov.com/gis-maps", "city_website": "https://www.fcgov.com"}},
    "Greeley": {"phone": "(970) 350-9800", "email": "planning@greeleygov.com", "address": "1000 10th St, Greeley, CO 80631", "links": {"permit_form": "https://greeleygov.com/permits", "zoning_map": "https://greeleygov.com/gis", "city_website": "https://greeleygov.com"}},
    "Pueblo": {"phone": "(719) 553-2200", "email": "planning@pueblo.us", "address": "211 E D St, Pueblo, CO 81003", "links": {"permit_form": "https://www.pueblo.us/permits", "zoning_map": "https://www.pueblo.us/gis", "city_website": "https://www.pueblo.us"}},
    "Boulder": {"phone": "(303) 441-1880", "email": "planning@bouldercolorado.gov", "address": "1739 Broadway, Boulder, CO 80302", "links": {"permit_form": "https://bouldercolorado.gov/permits", "zoning_map": "https://bouldercolorado.gov/gis", "city_website": "https://bouldercolorado.gov"}},
    "Grand Junction": {"phone": "(970) 244-3000", "email": "planning@gjcity.org", "address": "250 N 5th St, Grand Junction, CO 81501", "links": {"permit_form": "https://www.gjcity.org/permits", "zoning_map": "https://www.gjcity.org/gis", "city_website": "https://www.gjcity.org"}},
}

# Add premium data to each city
for c in cities:
    state = c["state_abbr"]
    base = premium_data.get(state, {})
    contact = city_contacts.get(c["city"], {})
    
    links = dict(base.get("links", {}))
    links.update(contact.get("links", {}))
    
    c["premium"] = {
        "dept_name": base.get("dept_name", "Planning Department"),
        "phone": contact.get("phone", "Check city website"),
        "email": contact.get("email", "Check city website"),
        "address": contact.get("address", "Check city website"),
        "links": links,
        "fees": base.get("fees", {"permit_fee": "TBD", "impact_fee": "TBD", "plan_check": "TBD"})
    }

with open("cities-data.json", "w") as f:
    json.dump(cities, f, indent=2)

print(f"✅ Updated {len(cities)} cities with premium (Niveau 2) data")
