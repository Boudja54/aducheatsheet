#!/usr/bin/env python3
"""
ADUCheatSheet.com — Full Generator v2 (Anti-Penalty Google)
1. Reads cities-data.json
2. Generates HTML city pages (unique content per city, conditional rows)
3. Generates PDF cheat sheets (3 pages: cover, premium data, checklist)
4. Updates index.html
"""

import json, os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

DATA_FILE = "cities-data.json"
TEMPLATE_FILE = "template-city.html"
CITIES_DIR = "cities"
PDF_DIR = "pdfs"

with open(DATA_FILE) as f:
    cities = json.load(f)

with open(TEMPLATE_FILE) as f:
    template = f.read()

def slug(city):
    return city.lower().replace(" ", "-").replace("'", "")

def city_filename(city, state):
    return f'{slug(city)}-{state.lower()}.html'

os.makedirs(CITIES_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

# ============================================================
# 1. GENERATE HTML PAGES (Anti-Penalty: unique content per city)
# ============================================================
for c in cities:
    html = template[:]
    
    # Related cities (same state)
    related = [x for x in cities if x["state_abbr"] == c["state_abbr"] and x["city"] != c["city"]]
    related_html = ""
    for r in related:
        related_html += f'<li><a href="/cities/{city_filename(r["city"], r["state_abbr"])}">{r["city"]}, {r["state_abbr"]}</a></li>\n'
    
    # Conditional rows: hide if "Not required" / "Not applicable"
    parking_row = ""
    if "required" in c.get("parking", "").lower() or "space" in c.get("parking", "").lower():
        parking_row = f'<tr><td><strong>Extra Parking Required</strong></td><td>{c["parking"]}</td></tr>'
    
    occ_row = ""
    if "required" in c.get("occupancy", "").lower():
        occ_row = f'<tr><td><strong>Owner Occupancy</strong></td><td>{c["occupancy"]}</td></tr>'
    elif "not" in c.get("occupancy", "").lower():
        occ_row = ""  # Hide row completely — no "Not required" text
    else:
        occ_row = f'<tr><td><strong>Owner Occupancy</strong></td><td>{c["occupancy"]}</td></tr>'
    
    replacements = {
        "[CITY]": c["city"],
        "[CITY-LOWER]": slug(c["city"]),
        "[STATE]": c["state"],
        "[STATE-LOWER]": c["state_abbr"].lower(),
        "[COUNTY]": c.get("county", ""),
        "[CITY_INTRO]": c.get("intro", ""),
        "[STATE_LAW]": c.get("state_law", "local zoning ordinances"),
        "[MAX_SIZE]": c["max_size"],
        "[SETBACKS]": c["setbacks"],
        "[PARKING_ROW]": parking_row,
        "[OCCUPANCY_ROW]": occ_row,
        "[ADDITIONAL_REQUIREMENTS]": c.get("additional", ""),
        "[FAQ_1]": c.get("faq1", ""),
        "[FAQ_2]": c.get("faq2", ""),
        "[FAQ_3]": c.get("faq3", ""),
        "[YEAR]": c.get("year", "2026"),
        "[PRICE]": c.get("web_price", "12"),
        "[STRIPE_CHECKOUT_URL]": c.get("stripe_checkout_url", ""),
        "[RELATED_CITIES]": related_html,
    }
    
    for old, new in replacements.items():
        html = html.replace(old, new)
    
    # SCHEMA.ORG JSON-LD (SEO : extraits enrichis Google)
    faq_items = ""
    for q in [c.get("faq1", ""), c.get("faq2", ""), c.get("faq3", "")]:
        if q and len(q) > 30:
            q_clean = q[:300].replace('"', "'")
            q_name = q.split("?")[0][:90].strip()
            if q_name:
                faq_items += f'{{"@type":"Question","name":"{q_name}?","acceptedAnswer":{{"@type":"Answer","text":"{q_clean}"}}}},'
    schema_json = f'''<script type="application/ld+json">
{{"@context":"https://schema.org",
"@graph":[
{{"@type":"FAQPage","mainEntity":[{faq_items.rstrip(",")}]}},
{{"@type":"LocalBusiness","name":"ADUCheatSheet - {c["city"]} ADU Guide",
"description":"{c["city"]} ADU requirements and zoning laws for {c["state"]}",
"areaServed":"{c["city"]}, {c["state_abbr"]}",
"url":"https://aducheatsheet.com/cities/{city_filename(c["city"], c["state_abbr"])}",
"address":{{"@type":"PostalAddress","addressLocality":"{c["city"]}","addressRegion":"{c["state_abbr"]}","addressCountry":"US"}}}}
]}}
</script>'''
    html = html.replace("</head>", schema_json + "\n</head>")
    
    fname = city_filename(c["city"], c["state_abbr"])
    with open(os.path.join(CITIES_DIR, fname), "w") as f:
        f.write(html)
    print(f"✅ HTML: {fname}")

# ============================================================
# 2. GENERATE PDF CHEAT SHEETS (3 pages)
# ============================================================
styles = getSampleStyleSheet()
title_style = ParagraphStyle("CustomTitle", parent=styles["Title"], fontSize=22, spaceAfter=12, alignment=TA_CENTER, textColor=colors.HexColor("#1a5f3a"))
subtitle_style = ParagraphStyle("Subtitle", parent=styles["Normal"], fontSize=11, spaceAfter=6, alignment=TA_CENTER, textColor=colors.HexColor("#555555"))
heading_style = ParagraphStyle("Heading2", parent=styles["Heading2"], fontSize=14, spaceAfter=8, textColor=colors.HexColor("#1a5f3a"))
normal_style = ParagraphStyle("Normal2", parent=styles["Normal"], fontSize=10, spaceAfter=4, leading=14)
disclaimer_style = ParagraphStyle("Disclaimer", parent=styles["Normal"], fontSize=8, spaceAfter=6, textColor=colors.HexColor("#856404"))
bullet_style = ParagraphStyle("Bullet", parent=styles["Normal"], fontSize=10, spaceAfter=3, leftIndent=20, leading=14)
table_header_style = ParagraphStyle("TableHeader", parent=styles["Normal"], fontSize=10, textColor=colors.white)
table_cell_style = ParagraphStyle("TableCell", parent=styles["Normal"], fontSize=10)

for c in cities:
    pdf_path = os.path.join(PDF_DIR, f"{slug(c['city'])}-{c['state_abbr'].lower()}-adu-cheatsheet.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                            topMargin=0.8*inch, bottomMargin=0.8*inch,
                            leftMargin=0.8*inch, rightMargin=0.8*inch)
    
    elements = []
    
    # PAGE 1: COVER + DISCLAIMER
    elements.append(Spacer(1, 1.5*inch))
    elements.append(Paragraph(f"The Ultimate<br/>{c['city']} ADU<br/>Permit Cheat Sheet", title_style))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph(f"{c['city']}, {c.get('county', '')} — {c.get('year', '2026')}", subtitle_style))
    elements.append(Spacer(1, 1.5*inch))
    
    disclaimer_text = (
        "<b>For Informational Purposes Only:</b><br/>"
        "The information provided is strictly for educational purposes and does not constitute "
        "legal, architectural, or professional urban planning advice. Always consult the "
        "official city planning department before making any decisions or starting any construction project."
    )
    elements.append(Paragraph(disclaimer_text, disclaimer_style))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "By using this guide, you agree that the publisher is not liable for any errors, omissions, or damages. "
        "Zoning laws change frequently — verify all information with local officials.",
        disclaimer_style
    ))
    
    elements.append(PageBreak())
    
    # PAGE 2: PREMIUM DATA & CONTACTS
    elements.append(Paragraph(f"🏡 {c['city']} ADU — Key Regulations &amp; Local Contacts", heading_style))
    elements.append(Spacer(1, 0.15*inch))
    
    # Basic rules table
    elements.append(Paragraph("<b>Zoning Rules Overview</b>", normal_style))
    rules_data = [
        [Paragraph("Regulation", table_header_style), Paragraph("Requirement", table_header_style)],
        [Paragraph("Maximum Size", table_cell_style), Paragraph(c["max_size"] + " sq ft", table_cell_style)],
        [Paragraph("Property Setbacks", table_cell_style), Paragraph(c["setbacks"], table_cell_style)],
    ]
    if "Required" in c.get("parking", ""):
        rules_data.append([Paragraph("Extra Parking", table_cell_style), Paragraph(c["parking"], table_cell_style)])
    if "Required" in c.get("occupancy", ""):
        rules_data.append([Paragraph("Owner Occupancy", table_cell_style), Paragraph(c["occupancy"], table_cell_style)])
    
    rule_table = Table(rules_data, colWidths=[2.2*inch, 3.5*inch])
    rule_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1a5f3a")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(rule_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Premium contacts
    contacts = c.get("premium", {})
    elements.append(Paragraph("<b>📍 Local Planning Department</b>", normal_style))
    elements.append(Spacer(1, 0.1*inch))
    
    contact_lines = [
        f"<b>Department:</b> {contacts.get('dept_name', 'Planning Department')}",
        f"<b>Phone:</b> {contacts.get('phone', 'Check city website')}",
        f"<b>Email:</b> {contacts.get('email', 'Check city website')}",
        f"<b>Address:</b> {contacts.get('address', 'Check city website')}",
        f"<b>Hours:</b> {contacts.get('hours', 'Check website')}",
    ]
    if contacts.get('notes'):
        contact_lines.append(f"<b>Note:</b> {contacts['notes']}")
    for line in contact_lines:
        elements.append(Paragraph(line, normal_style))
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph("<b>🔗 Key Online Resources</b>", normal_style))
    links = contacts.get('links', {})
    link_lines = [
        f"• <b>ADU Information:</b> <font color='blue'><u>{links.get('city_website', 'N/A')}</u></font>",
        f"• <b>Zoning Map:</b> <font color='blue'><u>{links.get('zoning_map', 'N/A')}</u></font>",
        f"• <b>Permit Portal:</b> <font color='blue'><u>{links.get('permit_form', 'N/A')}</u></font>",
    ]
    for line in link_lines:
        elements.append(Paragraph(line, normal_style))
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph("<b>💰 Maximum Estimated Permit Fees</b>", normal_style))
    fees = contacts.get('fees', {})
    fee_lines = [
        f"• Building permit fee: {fees.get('permit_fee', 'TBD')}",
        f"• Impact / development fees: {fees.get('impact_fee', 'TBD')}",
        f"• Plan check fee: {fees.get('plan_check', 'TBD')}",
    ]
    for line in fee_lines:
        elements.append(Paragraph(line, normal_style))
    
    elements.append(PageBreak())
    
    # PAGE 3: PROJECT CHECKLIST
    elements.append(Paragraph(f"✅ {c['city']} ADU — Step-by-Step Project Checklist", heading_style))
    elements.append(Spacer(1, 0.2*inch))
    
    permit_form_name = contacts.get('links', {}).get('permit_form', 'the application')
    checklist_items = [
        "☐ Verify zoning compliance — confirm your lot is zoned for ADU use",
        f"☐ Check the official zoning map at: <font color='blue'><u>{contacts.get('links', {}).get('zoning_map', 'city GIS portal')}</u></font>",
        "☐ Measure lot size, setbacks, and height limits against your design",
        "☐ Prepare a preliminary site plan (property lines, building locations, setbacks)",
        "☐ Draft floor plan showing ADU layout (bedroom, kitchen, bathroom)",
        f"☐ Complete the building permit application — available at: {permit_form_name}",
        "☐ Gather required documents: site plan, floor plan, elevations, proof of ownership",
        "☐ Submit complete application package to the Planning Department in person or online",
        "☐ Pay plan check fee and building permit fee",
        "☐ Wait for plan review (typically 4-8 weeks — respond to correction notices promptly)",
        "☐ Schedule required inspections: foundation, framing, electrical, plumbing, final",
        "☐ Obtain Certificate of Occupancy once all inspections pass",
    ]
    for item in checklist_items:
        elements.append(Paragraph(item, bullet_style))
        elements.append(Spacer(1, 0.03*inch))
    
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph(
        f"<i>💡 Tip: Schedule a pre-application meeting with the {c['city']} Planning Department "
        f"early in your process — they can identify issues before you spend time and money on detailed plans.</i>",
        normal_style
    ))
    
    doc.build(elements)
    print(f"✅ PDF: {os.path.basename(pdf_path)}")

print(f"\n🎉 Done! {len(cities)} HTML pages + {len(cities)} PDFs — all with unique content and conditional rows.")
