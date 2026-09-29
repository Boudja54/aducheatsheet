#!/usr/bin/env python3
"""Injecte le contenu VERIFIE (recherche 2026-09-29) dans cities-data.json.

Sources : codes municipaux officiels (Bellevue LUC, Vallejo Ord. 1890, Modesto
MMC Title 10), lois d'Etat (RCW 36.70A.681, Gov. Code 66310 et suivants), pages
officielles des villes et HCD. Chiffres cites avec leur source.

Usage : python3 apply_rich.py            (ecrit cities-data.json)
"""
import json
import re

FICHIER = "cities-data.json"


def table(entetes, lignes):
    h = "".join(f"<th>{c}</th>" for c in entetes)
    corps = "".join(
        "<tr>" + "".join(f"<td>{v}</td>" for v in ligne) + "</tr>" for ligne in lignes
    )
    return (
        f'<table class="data-table"><thead><tr>{h}</tr></thead>'
        f"<tbody>{corps}</tbody></table>"
    )


def section(titre, html):
    return f"<h2>{titre}</h2>\n{html}\n"


def liste(puces):
    return "<ul>\n" + "\n".join(f"  <li>{p}</li>" for p in puces) + "\n</ul>"


BELLEVUE = {
    "h1": "Bellevue ADU Rules (2026): Size, Setbacks, Parking &amp; DADU Guide",
    "seo_title": "Bellevue ADU Rules 2026: Size, Setbacks, Parking & DADU Permits",
    "seo_desc": (
        "Bellevue ADU and DADU requirements checked against the city's Land Use Code: "
        "1,200 sq ft maximum, 24 ft height, 10/15/5 ft setbacks, parking, owner "
        "occupancy and the building permit you actually need."
    ),
    "county": "King County",
    "state_law": (
        "the Bellevue Land Use Code (LUC 20.20.120, with dimensional standards in LUC "
        "20.20.538) and Washington's statewide ADU law, RCW 36.70A.680 and 36.70A.681"
    ),
    "intro": (
        "Detached ADUs only became legal in Bellevue on 1 July 2025, when the city's "
        "Middle Housing amendments (Ordinance 6851) took effect. Bellevue had already "
        "reformed its ADU rules in 2023 (Ordinance 6746). Together those two ordinances "
        "deleted most of the restrictions that older guides still repeat."
    ),
    "max_size": (
        "1,200 sq ft of floor area (up to 300 sq ft used for parking or unheated storage "
        "does not count toward the limit)"
    ),
    "setbacks": (
        "New detached ADUs: 10 ft front / 15 ft rear / 5 ft side in the SR-1 and SR-2 "
        "zones, per LUC 20.20.538 &mdash; a detached ADU may sit on the lot line that "
        "abuts an alley. Attached ADUs match the main house. A structure converted into "
        "an ADU does not have to meet today's setback or lot coverage rules at all."
    ),
    "parking": (
        "No space required for an ADU under 1,000 sq ft of floor area, or for any ADU "
        "within 1/2 mile of a major transit stop. Otherwise 1 space per ADU"
    ),
    "occupancy": (
        "Not required &mdash; Bellevue repealed owner occupancy in 2023 (Ordinance 6746) "
        "and Washington law bars cities from imposing it"
    ),
    "additional": liste([
        "Up to <strong>2 ADUs per lot</strong> in any zone where a single-family home is allowed &mdash; two attached, one attached plus one detached, or two detached units",
        "Detached ADU height limit: <strong>24 ft</strong>, or <strong>28 ft</strong> when built as an addition over an existing accessory structure",
        "No design review and no ADU registry: additional design controls and the registration/noticing requirements were removed in 2023",
        "Converting a detached garage, studio or other existing structure is allowed <strong>even if that structure does not meet current setback or lot coverage rules</strong>",
        "Impact fees are capped at <strong>50%</strong> of what the main house would be charged (RCW 36.70A.681)",
        "An ADU may now be <strong>sold separately</strong> from the main house; the old condominium prohibition was lifted",
        "A property cannot have both an ADU and a home-occupation business, and new ADUs are not allowed on unit lots created by unit-lot or short subdivision",
        "Short-term rentals may still be regulated by the city &mdash; check before counting on nightly-rental income",
    ]),
    "long_content": (
        section(
            "Bellevue ADU rules changed twice in three years",
            "<p>Two ordinances explain why so much Bellevue ADU information online is out of "
            "date:</p>"
            + liste([
                "<strong>Ordinance 6746 (2023) &mdash; the ADU reform package.</strong> Bellevue repealed the owner-occupancy requirement, removed ADU design controls, dropped the registration and noticing process, and lifted the ban on selling an ADU separately from the main house.",
                "<strong>Ordinance 6851 (adopted 24 June 2025, effective 1 July 2025) &mdash; Middle Housing.</strong> This is the change that matters most: before it, detached ADUs were <em>not allowed in Bellevue at all</em>. The middle housing amendments legalised them and allow up to two ADUs per lot, implementing Washington's HB 1110 and HB 1337.",
            ])
            + "<p>Practical consequence: if an article tells you Bellevue requires the owner to "
            "live on site, caps an ADU at 1,000 sq ft, or that you cannot build a detached unit, "
            "it was written before mid-2025 and is describing rules that no longer exist.</p>",
        )
        + section(
            "What you can build in Bellevue: the 2026 limits",
            table(
                ["Item", "Bellevue limit"],
                [
                    ["Maximum ADU floor area", "1,200 sq ft (up to 300 sq ft of parking or unheated storage excluded)"],
                    ["Detached ADU height", "24 ft &mdash; 28 ft when added over an existing accessory structure"],
                    ["Attached ADU height", "The same limit that applies to the main house"],
                    ["Setbacks, new detached ADU", "10 ft front / 15 ft rear / 5 ft side (SR-1 and SR-2, LUC 20.20.538)"],
                    ["Setbacks, attached ADU", "Same as the main house"],
                    ["Converted existing structure", "Allowed regardless of current setback or lot coverage compliance"],
                    ["Units per lot", "Up to 2 ADUs"],
                    ["Units counted for permit type", "ADUs count as regular dwelling units"],
                    ["Parking", "0 spaces under 1,000 sq ft or within 1/2 mile of a major transit stop; otherwise 1"],
                    ["Owner occupancy", "Not required"],
                    ["Impact fees", "Capped at 50% of the principal unit's fees"],
                ],
            )
            + "<p>Two narrow limits are worth knowing early: a site cannot contain both an ADU "
            "and a home-occupation business, and no new ADU can be built on a unit lot created "
            "through a unit-lot or short subdivision.</p>",
        )
        + section(
            "Can I add an ADU to my existing Bellevue house?",
            "<p>Yes, and this is the cheapest route. An <strong>attached</strong> ADU (basement, "
            "converted garage, upper-floor addition) follows the main house's height and setback "
            "limits, and its floor area is <em>not</em> counted against the site's single-family "
            "floor-area allowance &mdash; so a big addition does not eat your FAR.</p>"
            "<p>Conversions are the hidden advantage in Bellevue: the code lets you convert an "
            "existing structure into an ADU <em>regardless of whether that structure currently "
            "meets the applicable setback and lot coverage dimensional requirements</em>, and "
            "doing so does not make the property legally non-conforming. In most cities, a "
            "garage that sits too close to the property line is the reason a conversion fails. "
            "In Bellevue it is not a blocker.</p>",
        )
        + section(
            "Can I build a DADU (detached ADU) in Bellevue?",
            "<p>Since 1 July 2025, yes. Detached units are limited to <strong>24 ft</strong> in "
            "height, or <strong>28 ft</strong> when proposed as an addition over an existing "
            "accessory structure, and they follow the middle-housing dimensional table in LUC "
            "20.20.538 (10 ft front, 15 ft rear, 5 ft side in the single-family zones). A "
            "detached ADU may be sited on the lot line that abuts an alley, which is how "
            "narrow lots usually make the numbers work.</p>"
            "<p>Watch for one confusion that catches even experienced designers: the old "
            "detached <em>accessory structure</em> rules (LUC 20.20.125 &mdash; 5 ft rear "
            "setback, 15 ft height, 10% lot coverage) do <strong>not</strong> apply to detached "
            "ADUs. Mixing the two produces the wrong setback and the wrong height limit, which "
            "is exactly the mistake this page used to contain.</p>",
        )
        + section(
            "Parking, owner occupancy and design review: three rules people get wrong",
            liste([
                "<strong>Parking is not simply waived.</strong> Bellevue requires no off-street space for an ADU under 1,000 sq ft, or for one within 1/2 mile of a major transit stop. Outside those cases, one space per ADU is required. State law also caps what a city may ask: no parking within a 1/2-mile walk of a major transit stop, at most 1 space on lots under 6,000 sq ft, at most 2 on larger lots.",
                "<strong>Owner occupancy is gone.</strong> The city repealed it in 2023 and RCW 36.70A.681 independently forbids cities from requiring the owner to live in the ADU or the main house.",
                "<strong>Design review is gone.</strong> An ADU cannot face design or aesthetic requirements stricter than those applied to a single-family house, and Bellevue removed its extra design controls in 2023.",
            ]),
        )
        + section(
            "Which Bellevue building permit you need, and how the process runs",
            liste([
                "<strong>1 or 2 units on the lot:</strong> a standard one- and two-family residence building permit.",
                "<strong>3 to 6 units in a single structure:</strong> the Middle Housing permit process.",
                "<strong>More than 6 units:</strong> the commercial multifamily process.",
                "ADUs count as dwelling units for this test, so adding a second ADU can push a project into the middle housing path.",
                "One building permit is issued per building; a multi-building project may also need a separate clearing and grading site permit.",
                "There is no ADU registry and no noticing requirement &mdash; that step was removed in 2023.",
            ])
            + "<p>Start with a pre-application conversation with Bellevue's Development Services "
            "before you pay for drawings. Ask two questions that change projects: whether the lot "
            "carries a home-occupation business, and whether it was created by a unit-lot or "
            "short subdivision &mdash; either one can rule out a new ADU.</p>",
        )
        + section(
            "One amendment to watch",
            "<p>Ordinance 6931, passed on 28 July 2026, amends the units-per-lot provisions in "
            "LUC 20.20.120(C)(1) and 20.20.538(C)(1). It was pending codification at the time "
            "this page was written. If your project depends on the exact number of units you "
            "can build, confirm the current count with the city rather than relying on any "
            "guide, including this one.</p>",
        )
    ),
    "faq1": (
        "Can I build an ADU in Bellevue? Yes. Bellevue allows up to two ADUs on any lot zoned "
        "for a single-family home, and since Ordinance 6851 took effect on 1 July 2025 that "
        "includes detached ADUs (DADUs). No owner occupancy is required and no design review "
        "is applied."
    ),
    "faq2": (
        "How big can an ADU be in Bellevue? The standard maximum floor area is 1,200 sq ft. Up "
        "to 300 sq ft used for parking or unheated storage is excluded from the count, an ADU "
        "converted from a previously permitted guest cottage is exempt from the cap, and the "
        "Director may approve more than 1,200 sq ft where the unit sits entirely on one floor "
        "or is added to an existing detached structure. An attached ADU's floor area does not "
        "count against the site's single-family floor-area allowance."
    ),
    "faq3": (
        "What are the setback requirements for an ADU in Bellevue? An attached ADU follows the "
        "main house's setbacks. A new detached ADU follows the middle-housing table in LUC "
        "20.20.538, which is 10 ft front, 15 ft rear and 5 ft side in the SR-1 and SR-2 zones, "
        "although a detached ADU may be sited on the lot line that abuts an alley. If you "
        "convert an existing structure, today's setback and lot coverage rules do not block the "
        "project."
    ),
    "faqs": [
        {
            "q": "Can I build a DADU in Bellevue?",
            "a": "Yes, but only since 1 July 2025. Detached ADUs were not allowed in Bellevue before Ordinance 6851 (the Middle Housing amendments) took effect. Detached units are limited to 24 ft in height, or 28 ft when built as an addition over an existing accessory structure, and they follow the dimensional table in LUC 20.20.538.",
        },
        {
            "q": "How many ADUs can I build in Bellevue?",
            "a": "Up to two ADUs on a lot where a single-family dwelling is allowed: two attached, one attached plus one detached, or two detached. Note that Ordinance 6931, passed on 28 July 2026, amends the units-per-lot provisions and was still pending codification when this page was written, so confirm the current count with Bellevue before you commit.",
        },
        {
            "q": "Do I have to live in my Bellevue house to rent out the ADU?",
            "a": "No. Bellevue removed its owner-occupancy requirement in 2023 and Washington law bars cities from requiring the owner to live in the ADU or the main house. Rentals of 30 consecutive days or more are allowed; short-term rentals may still be restricted by the city.",
        },
        {
            "q": "Do I need design review for an ADU in Bellevue?",
            "a": "No. Bellevue removed ADU design controls in 2023, and state law bars aesthetic requirements or design review for ADUs that are stricter than those applied to the principal unit.",
        },
        {
            "q": "What does a Bellevue ADU cost in impact fees?",
            "a": "Impact fees for an ADU are capped at 50% of what the same unit would be charged as a principal dwelling under RCW 36.70A.681. That cap is one of the biggest cost differences between Bellevue and California cities, where impact fees often apply in full above a size threshold.",
        },
    ],
    "sources": [
        {"label": "Bellevue Land Use Code 20.20.120 &mdash; Accessory dwelling units", "url": "https://bellevue.municipal.codes/LUC/20.20.120"},
        {"label": "Bellevue Land Use Code 20.20.538 &mdash; Middle housing dimensional standards", "url": "https://bellevue.municipal.codes/LUC/20.20.538"},
        {"label": "City of Bellevue &mdash; ADU reform (Ordinance 6746, 2023)", "url": "https://bellevuewa.gov/ADU-reform"},
        {"label": "City of Bellevue &mdash; Middle Housing code amendments (Ordinance 6851, effective 1 July 2025)", "url": "https://bellevuewa.gov/code-amendments/recent-code-amendments/middle-housing-code-amendments"},
        {"label": "City of Bellevue &mdash; Middle housing building permits", "url": "https://bellevuewa.gov/city-government/departments/development/permits/middle-housing-building"},
        {"label": "Washington RCW 36.70A.681 &mdash; ADU standards a city may not impose", "url": "https://app.leg.wa.gov/RCW/default.aspx?cite=36.70A.681"},
        {"label": "Bellevue Planning Commission staff report &mdash; middle housing dimensional table (March 2025)", "url": "https://bellevuewa.gov/sites/default/files/media/pdf_document/2025/dsd-03212025-middle-housing-pc-staff-report-luca-and-attachment-a.pdf"},
    ],
}

VALLEJO = {
    "h1": "Vallejo ADU Rules (Solano County): Size, Setbacks, Parking &amp; Permits",
    "seo_title": "Vallejo ADU Rules 2026: Size, Setbacks, Parking & Permits",
    "seo_desc": (
        "Vallejo ADU requirements under the new Ordinance 1890 and California state law: "
        "1,200 sq ft detached, 4 ft setbacks, parking exemptions, JADU rules, fees and the "
        "60-day approval deadline."
    ),
    "county": "Solano County",
    "state_law": (
        "California Government Code sections 66310 to 66342 (the ADU statutes, renumbered by "
        "SB 477 in 2024) layered on the Vallejo Municipal Code Chapter 16.303, which was "
        "rewritten by Ordinance No. 1890 N.C.(2d), effective 8 October 2026"
    ),
    "intro": (
        "Vallejo replaced its entire ADU chapter in 2026. Ordinance No. 1890 N.C.(2d) was "
        "adopted on 8 September 2026 and takes effect on 8 October 2026, turning a six-section "
        "chapter into a new fifteen-section Chapter 16.303. The figures below are correct under "
        "both the outgoing and the incoming chapter, with two exceptions: the minimum unit size "
        "rises from 150 to 190 sq ft, and JADU owner occupancy narrows to shared-sanitation "
        "cases only."
    ),
    "max_size": (
        "1,200 sq ft for a detached ADU; an attached ADU is capped at the lesser of 50% of the "
        "main home's floor area or 1,200 sq ft; garage and interior conversions have no size "
        "limit"
    ),
    "setbacks": (
        "4 ft side and 4 ft rear for new units; no setback at all for a conversion or a JADU; "
        "the front setback follows the underlying zoning district (the city's summary sheet "
        "lists 15 ft)"
    ),
    "parking": (
        "1 off-street space per ADU (tandem counts) unless an exemption applies &mdash; no "
        "space is required for an ADU of 500 sq ft or less, within 1/2 mile of transit, in a "
        "historic district, inside the main or accessory structure, on a permit-only street "
        "where no permit is offered to the ADU occupant, or where a car-share vehicle sits "
        "within one block"
    ),
    "occupancy": (
        "Not required for an ADU. A JADU requires owner occupancy today; from 8 October 2026 "
        "only where it shares sanitation facilities with the main home"
    ),
    "additional": liste([
        "Up to <strong>3 units</strong> on a single-family lot: 1 JADU, plus one attached or conversion ADU, plus one detached ADU",
        "On a lot with an existing multifamily building: up to <strong>8 detached ADUs</strong>, capped at the number of existing units; ADUs created inside existing non-livable space can be at least 1 and up to 25% of the existing units",
        "Detached ADU height: <strong>16 ft</strong>, rising to <strong>18 ft</strong> (plus a 2 ft roof-pitch allowance) within 1/2 mile of a major transit stop; attached ADUs may reach <strong>25 ft</strong>",
        "<strong>No replacement parking</strong> is required when a garage or carport is demolished or converted for an ADU",
        "Impact fees apply only to new ADUs of <strong>750 sq ft or more</strong>, and must be charged proportionally to the main home's fees; conversions and JADUs pay no new utility connection fees",
        "New detached ADUs need solar panels under the California Energy Code (exempt below 500 sq ft or 1.8 kW)",
        "Fire sprinklers cannot be required in an ADU unless the main home already requires them",
        "Rentals must run <strong>30 consecutive days or longer</strong>; the ADU cannot be sold separately, and the deed restriction is recorded with the Solano County Assessor/Recorder",
        "Approval is <strong>ministerial</strong> &mdash; no public hearing &mdash; and the city must decide within 60 days of a complete application or the permit is deemed approved",
        "An ADU built before 1 January 2020 without permits can be legalised, with enforcement on health and safety issues delayed to 1 January 2030",
    ]),
    "long_content": (
        section(
            "Vallejo's ADU ordinance changed in 2026 &mdash; what that means for you",
            "<p>Vallejo repealed and replaced Chapter 16.303 in its entirety. Ordinance No. 1890 "
            "N.C.(2d) was introduced on 4 August 2026, adopted on 8 September 2026, and became "
            "effective on <strong>8 October 2026</strong> after the standard 30-day period. "
            "Until that date the old six-section chapter still governs.</p>"
            "<p>There is a second layer to the story. On 8 October 2025 the state Department of "
            "Housing and Community Development wrote to Vallejo noting that the most recent ADU "
            "ordinance on file dated from 2018 and may not comply with state ADU law. Under "
            "Government Code section 66316, an ADU ordinance that fails to meet state law is "
            "<strong>null and void</strong> &mdash; and state standards apply instead. Ordinance "
            "1890 is the city's compliance response.</p>"
            "<p>The practical rule for a homeowner: if a local standard blocks your project, ask "
            "whether it is stricter than state law allows. Where the two conflict, state law "
            "wins (VMC section 16.303.15).</p>",
        )
        + section(
            "How many ADUs can I build on a Vallejo lot?",
            liste([
                "<strong>Single-family lot:</strong> three units in total &mdash; one JADU, one attached or conversion ADU, and one detached ADU.",
                "<strong>Lot with an existing multifamily building:</strong> up to 8 detached ADUs, capped at the number of existing units; conversion ADUs inside existing non-livable space are allowed at a minimum of one and up to 25% of the existing units.",
                "<strong>Lot with a proposed multifamily building:</strong> up to 2 detached ADUs.",
                "ADUs and JADUs do <strong>not</strong> count toward the site's allowable residential density.",
            ])
            + "<p>On top of these local limits, California requires every city to approve certain "
            "ADU types ministerially, including one ADU plus one JADU on a single-family lot and "
            "a detached new-construction ADU of up to 800 sq ft with 4 ft side and rear setbacks. "
            "Those by-right units cannot be refused for parking, or because the site has "
            "non-conforming conditions.</p>",
        )
        + section(
            "Vallejo ADU size, height and setback limits",
            table(
                ["Item", "Vallejo limit"],
                [
                    ["Detached ADU maximum", "1,200 sq ft"],
                    ["Attached ADU maximum", "Lesser of 50% of the main home's floor area or 1,200 sq ft"],
                    ["Conversion ADU (garage, interior)", "No minimum or maximum floor area"],
                    ["Minimum unit size", "190 sq ft from 8 October 2026 (150 sq ft before that)"],
                    ["JADU", "500 sq ft maximum, and it must sit within the walls of the house"],
                    ["Detached ADU height", "16 ft; 18 ft near major transit or on a multifamily multistory lot, plus 2 ft for an aligned roof pitch"],
                    ["Attached ADU height", "Up to 25 ft, or the main home's limit if lower"],
                    ["Side and rear setbacks", "4 ft for new units; none for conversions or JADUs"],
                    ["Front setback", "Follows the base zoning district (the city summary sheet lists 15 ft)"],
                    ["Parking", "1 space per ADU unless an exemption applies"],
                    ["Owner occupancy", "Not required for an ADU; required for a JADU in shared-sanitation cases"],
                    ["Rental term", "30 consecutive days or more"],
                ],
            ),
        )
        + section(
            "Parking: Vallejo does require a space, with a long list of exceptions",
            "<p>Most summaries of Vallejo's rules state that no parking is required. That is "
            "wrong. The city requires <strong>one off-street space per ADU</strong>, and tandem "
            "spaces count. A space cannot be required, however, in any of these cases:</p>"
            + liste([
                "the ADU is 500 sq ft or less;",
                "it sits within 1/2 mile walking distance of public transit;",
                "it is in a historic district;",
                "it is located entirely within the main dwelling or an accessory structure;",
                "the street is permit-parking only and the city does not offer a permit to the ADU occupant;",
                "a car-share vehicle is available within one block.",
            ])
            + "<p>Two further points save money. <strong>No replacement parking</strong> is "
            "required when you demolish or convert a garage or carport for the ADU, and the "
            "by-right units listed in Government Code section 66323 cannot be conditioned on "
            "parking at all.</p>",
        )
        + section(
            "Owner occupancy, renting and selling a Vallejo ADU",
            liste([
                "<strong>An ADU does not require owner occupancy.</strong> State law bars the requirement for ADUs.",
                "<strong>A JADU does</strong> under the current chapter; from 8 October 2026 the requirement applies only when the JADU shares sanitation facilities with the main home.",
                "<strong>Rentals must be 30 days or longer.</strong> Short-term and vacation rentals of an ADU are not allowed in Vallejo.",
                "<strong>The unit cannot be sold separately</strong> from the main house, and the deed restriction that records these limits is filed with the Solano County Assessor/Recorder &mdash; that is the county's only role inside the city, since Solano County's own zoning chapter governs unincorporated land only.",
            ]),
        )
        + section(
            "Permits, fees and the 60-day rule",
            liste([
                "<strong>Ministerial approval, no hearing.</strong> The city must approve or deny a complete application within 60 days; if it does nothing, the permit is <strong>deemed approved</strong>.",
                "<strong>The 800 sq ft by-right ADU.</strong> Vallejo must allow at least an 800 sq ft ADU with 4 ft side and rear setbacks, and site rules such as lot coverage, floor-area ratio, open space and front setbacks cannot be used to preclude it.",
                "<strong>Impact fees only above 750 sq ft</strong>, and only in proportion to what the main home would pay. Conversions and JADUs are not charged new utility connection or capacity fees.",
                "<strong>Design standards apply narrowly:</strong> objective design rules for newly built attached or detached ADUs over 800 sq ft must be met; they do not apply to by-right state units.",
                "<strong>Fire sprinklers and passageways cannot be imposed</strong> beyond what the main residence already requires.",
                "<strong>Unpermitted ADUs:</strong> a unit built before 1 January 2020 can be legalised, and enforcement is delayed to 1 January 2030 where there is no health or safety issue.",
            ])
            + "<p>Because the ordinance changed in October 2026, confirm the fee schedule and "
            "front setback for your specific zoning district with Vallejo Planning before you "
            "draw anything. The figures above come from the ordinance text, the city's own ADU "
            "summary sheet and California statute &mdash; all linked below.</p>",
        )
    ),
    "faq1": (
        "Are ADUs allowed in Vallejo? Yes. Vallejo allows ADUs and JADUs on residential lots "
        "that have a proposed or existing dwelling, and approval is ministerial with no public "
        "hearing. Chapter 16.303 was rewritten by Ordinance No. 1890 N.C.(2d), effective "
        "8 October 2026."
    ),
    "faq2": (
        "How big can an ADU be in Vallejo? A detached ADU can be up to 1,200 sq ft. An attached "
        "ADU is capped at the lesser of 50% of the main home's floor area or 1,200 sq ft. Garage "
        "and interior conversions have no size limit. The minimum unit size becomes 190 sq ft on "
        "8 October 2026, up from 150 sq ft."
    ),
    "faq3": (
        "What are the setback and parking requirements for an ADU in Vallejo? New units need "
        "4 ft side and 4 ft rear setbacks; conversions and JADUs need none. One off-street "
        "parking space per ADU is required unless an exemption applies &mdash; an ADU of 500 sq "
        "ft or less, within 1/2 mile of transit, in a historic district, inside the main or "
        "accessory structure, on a permit-only street where no permit is offered to the ADU "
        "occupant, or within one block of a car-share vehicle. No replacement parking is needed "
        "for a garage conversion."
    ),
    "faqs": [
        {
            "q": "How many ADUs can I build in Vallejo?",
            "a": "On a single-family lot, three units in total: one JADU plus one attached or conversion ADU plus one detached ADU. A lot with an existing multifamily building can take up to 8 detached ADUs, capped at the number of existing units, and interior conversion ADUs can be at least one and up to 25% of the existing units.",
        },
        {
            "q": "Do I have to live in the property to rent out a Vallejo ADU?",
            "a": "No for an ADU \u2014 California law bars an owner-occupancy requirement for ADUs and Vallejo dropped it. A JADU does require owner occupancy today, and from 8 October 2026 it does so only where the JADU shares sanitation facilities with the main home. Rentals must be for 30 consecutive days or longer.",
        },
        {
            "q": "Can I convert my garage into an ADU in Vallejo?",
            "a": "Yes. A legally built garage, barn or studio can be converted, and Vallejo treats a converted garage as a conversion ADU: no setback requirement, no minimum or maximum floor area, and no replacement parking. Demolishing a detached garage can be permitted at the same time as the ADU.",
        },
        {
            "q": "How long does a Vallejo ADU permit take?",
            "a": "Vallejo must approve or deny a complete ADU application within 60 days, and the review is ministerial with no public hearing. If the city misses the deadline, the permit is deemed approved under state law.",
        },
        {
            "q": "Do Vallejo's rules or California's rules apply?",
            "a": "Both, and state law wins where they conflict. California's ADU statutes (Government Code sections 66310 to 66342) set the floor: they limit what a city can require on size, setbacks, parking, owner occupancy and fees. Vallejo's chapter 16.303 adds local standards, but section 66316 makes a non-compliant ordinance null and void \u2014 which is why the state sent Vallejo a technical assistance letter in October 2025.",
        },
    ],
    "sources": [
        {"label": "Vallejo Ordinance No. 1890 N.C.(2d) &mdash; full ordinance text (PDF)", "url": "https://www.cityofvallejo.net/common/pages/GetFile.ashx?key=anxGAdOC"},
        {"label": "City of Vallejo &mdash; ADU Ordinance Update project page", "url": "https://www.vallejo.gov/our_city/departments_divisions/planning_development_services/planning_division/long_range_projects/a_d_u_ordinance_update"},
        {"label": "Vallejo Municipal Code Chapter 16.303 &mdash; Accessory dwelling units (Municode)", "url": "https://library.municode.com/ca/vallejo/codes/municipal_code?nodeId=TIT16ZO_PTIIIUSST_CH16.303ACDWUN"},
        {"label": "City of Vallejo &mdash; ADU Mini-Guide and Summary Sheet (PDF)", "url": "https://www.cityofvallejo.net/common/pages/GetFile.ashx?key=0wc%2fARP5"},
        {"label": "California Government Code 66314 &mdash; development standards", "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=66314"},
        {"label": "California Government Code 66321 &mdash; size and height floors", "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=66321"},
        {"label": "California Government Code 66323 &mdash; by-right ministerial approvals", "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=66323"},
        {"label": "HCD &mdash; technical assistance letter to Vallejo (8 October 2025, PDF)", "url": "https://www.hcd.ca.gov/sites/default/files/docs/policy-and-research/ordinance-review-letters/vallejo-adu-ta-100825.pdf"},
        {"label": "HCD &mdash; ADU Handbook and ordinance review", "url": "https://www.hcd.ca.gov/building-standards/adu/handbook"},
        {"label": "Solano County &mdash; ADU information (unincorporated areas)", "url": "https://www.solanocounty.gov/government/resource-management/planning-services/accessory-dwelling-units-adus"},
    ],
}

MODESTO = {
    "h1": "Modesto ADU Rules &amp; Land Use Law: Size, Setbacks, Parking &amp; Permits",
    "seo_title": "Modesto ADU Rules 2026: Land Use Law, Size, Fees & Permits",
    "seo_desc": (
        "Modesto ADU requirements from the city's own land use code (Title 10, Article 5): "
        "1,200 sq ft detached, 4 ft setbacks, parking limits, the $2,429 flat permit fee, no "
        "minimum size and ADU Express same-day review."
    ),
    "county": "Stanislaus County",
    "state_law": (
        "the Modesto Municipal Code Title 10, Chapter 4, Article 5, sections 10-4.501 to "
        "10-4.512, which implements California Government Code section 66310 et seq."
    ),
    "intro": (
        "Modesto's ADU rules sit in the city's own land use code &mdash; Title 10, Chapter 4, "
        "Article 5 of the Modesto Municipal Code, added by Ordinance 3762-C.S. and amended in "
        "2025. Modesto is an incorporated charter city, so Stanislaus County's ADU chapter "
        "(21.74) does not apply inside the city limits; the county's rules govern "
        "unincorporated land only, although its free ADU plan sets are accepted in Modesto."
    ),
    "max_size": (
        "1,200 sq ft for a detached ADU, which also cannot exceed the main home's floor area; "
        "an attached ADU is capped at 50% of the main home but never below 800 sq ft; a JADU "
        "is limited to 500 sq ft"
    ),
    "setbacks": (
        "At least 4 ft side and 4 ft rear for a new detached ADU; a converted structure only "
        "needs enough clearance for fire and safety; lot coverage limits do not apply to an ADU "
        "of 800 sq ft or less"
    ),
    "parking": (
        "No more than 1 off-street space may be required, and zero in six cases &mdash; within "
        "1/2 mile of transit, in a historic or architecturally significant district, inside the "
        "main or accessory structure, on-street permits required but not offered to the ADU "
        "occupant, a car-share vehicle within one block, or an ADU filed with a new dwelling "
        "permit on the same lot"
    ),
    "occupancy": (
        "Not required for an ADU. A JADU requires a recorded deed restriction that the owner "
        "live in the JADU or the remaining part of the main home"
    ),
    "additional": liste([
        "Up to <strong>2 additional units</strong> on a single-family lot &mdash; any combination of attached, detached or converted ADU plus one JADU; three homes counting the main house",
        "ADUs are allowed in single-family, multifamily and mixed-use zones; JADUs only in single-family zones where a house exists or is proposed",
        "Detached ADU height: <strong>16 ft</strong>, or 18 ft within 1/2 mile of a major transit stop, plus 2 ft for an aligned roof pitch; attached ADUs up to <strong>25 ft</strong> and two storeys",
        "Approval is <strong>ministerial</strong> with no public hearing, and the city must decide within 60 days or the ADU is deemed approved",
        "<strong>No impact fee</strong> on an ADU under 750 sq ft; larger ADUs are charged proportionally to the main home",
        "Building permit fee: <strong>$2,429 per permit</strong> for ADUs and small dwellings up to 1,200 sq ft under the FY 2026-27 fee schedule, including mechanical, plumbing and electrical",
        "Photovoltaic (solar) plans are required for new-construction detached ADUs under the California Energy Code",
        "Fire sprinklers cannot be required in the ADU unless the main home needs them, and no passageway may be required",
        "Rentals must be for 30 days or more, and the JADU cannot be sold separately from the main house",
        "The City Council may designate areas where ADUs are not allowed because of water or sewer infrastructure constraints",
    ]),
    "long_content": (
        section(
            "Which law applies to a Modesto ADU: city, county or state?",
            "<p>All three, in this order. Modesto's own code governs first: the city is "
            "incorporated, so the rules that count inside the city limits are Title 10, Chapter "
            "4, Article 5 of the Modesto Municipal Code (sections 10-4.501 to 10-4.512), not "
            "Stanislaus County's Chapter 21.74. Where a local standard conflicts with California "
            "Government Code section 66310 et seq., state law applies &mdash; section 10-4.512 "
            "says so directly.</p>"
            "<p>One practical consequence: the county publishes <strong>free ADU plan sets</strong> "
            "(405 sq ft, 744 sq ft and 1,192 sq ft, drawn to the 2025 California Building Code) "
            "that can be used in Modesto as well as in the unincorporated county. For a "
            "new-construction detached ADU, those drawings can remove most of the design cost "
            "before you ever speak to a plan reviewer.</p>",
        )
        + section(
            "How many ADUs can I build in Modesto?",
            liste([
                "<strong>Single-family lot:</strong> up to two additional units &mdash; any combination of attached, detached or converted ADU, plus one JADU.",
                "<strong>Multifamily building:</strong> ADUs inside existing non-livable space can be at least one and up to 25% of the existing units; up to 8 detached ADUs on a lot with an existing multifamily building, and up to 2 detached ADUs where the multifamily building is proposed.",
                "<strong>Places of worship:</strong> up to two detached ADUs of no more than 1,200 sq ft each, with 4 ft interior side and rear setbacks and no extra parking where one existing space is reserved per ADU.",
            ])
            + "<p>California also requires Modesto to approve certain ADU types ministerially, "
            "and the city's code says so explicitly in section 10-4.511. Those units cannot be "
            "refused because the property has non-conforming zoning conditions, and correcting "
            "those conditions cannot be made a condition of approval.</p>",
        )
        + section(
            "Modesto ADU size, height and setback limits",
            table(
                ["Item", "Modesto limit"],
                [
                    ["Detached ADU maximum", "1,200 sq ft, and never more than the main home's floor area"],
                    ["Attached ADU maximum", "50% of the main home's floor area, but the city cannot refuse an attached ADU of up to 800 sq ft"],
                    ["JADU maximum", "500 sq ft, inside the walls of the house"],
                    ["Minimum ADU size", "None in the code &mdash; state law bars a minimum that would exclude an efficiency unit"],
                    ["Expansion of a converted ADU", "Up to 150 sq ft beyond the existing structure, for ingress and egress only"],
                    ["Detached ADU height", "16 ft; 18 ft within 1/2 mile of a major transit stop; plus 2 ft for an aligned roof pitch"],
                    ["Attached ADU height", "25 ft or the zone limit for the main home, whichever is lower; two storeys maximum"],
                    ["Setbacks, new detached", "4 ft side and 4 ft rear minimum"],
                    ["Setbacks, converted structure", "Sufficient for fire and safety only"],
                    ["Lot coverage", "Limits do not apply to an ADU of 800 sq ft or less"],
                    ["Parking", "1 space maximum, zero in six cases"],
                    ["Owner occupancy", "Not required for an ADU; required for a JADU"],
                ],
            ),
        )
        + section(
            "Parking in Modesto: one space maximum, none in six cases",
            "<p>Modesto cannot require more than one off-street space for an ADU, and a tandem "
            "space in an existing driveway counts. Uncovered spaces may sit in the required front "
            "setback where a driveway already exists, or in the rear setback where the lot has "
            "alley access. No space at all may be required in these six situations:</p>"
            + liste([
                "the ADU is within 1/2 mile walking distance of public transit;",
                "it is in an architecturally or historically significant district;",
                "it is part of the main residence or an existing accessory structure;",
                "the street requires permits but no permit is offered to the ADU occupant;",
                "a car-share vehicle is available within one block;",
                "the ADU permit is filed together with a new single-family or multifamily dwelling permit on the same lot.",
            ])
            + "<p>Parking that disappears when a garage or carport is demolished or converted "
            "does <strong>not</strong> have to be replaced.</p>",
        )
        + section(
            "Modesto's ADU Express program: same-day plan review",
            "<p>Modesto runs an appointment-based <strong>ADU Express</strong> service that "
            "coordinates Building Safety, Fire, Planning and Engineering in one review session "
            "for ADU and JADU projects that qualify for ministerial approval. Same-day approval "
            "requires plans prepared by a professional designer, licensed architect or engineer. "
            "Appointments are booked through Building Safety at 209-577-5232, extension 0; the "
            "program's flyer lists Tuesday sessions from 10:00 to 11:00 a.m.</p>"
            "<p>The city describes an eight-step path: create a plan, get planning advice, "
            "prepare the submittal package, apply through the eTRAKiT portal, hire licensed "
            "professionals, go through staff plan review, receive the permit, then build and "
            "inspect. Housing questions go to the Community Development Division at "
            "housing@modestogov.com or 209-577-5211; planning questions to 209-577-5267.</p>",
        )
        + section(
            "What a Modesto ADU costs: $2,429 per permit",
            "<p>The FY 2026-27 Building Safety fee schedule charges <strong>$2,429 per permit</strong> "
            "for accessory dwelling units and small dwellings up to 1,200 sq ft, covering "
            "mechanical, plumbing and electrical work, payable at application. On top of that, "
            "<strong>no impact fee applies to an ADU under 750 sq ft</strong>, and above that "
            "threshold fees must be charged in proportion to the main dwelling's square footage "
            "&mdash; not at the full rate for a new house.</p>"
            "<p>Financial help exists: CalHFA's ADU grant programme has offered up to $40,000, "
            "and local options include the Valley First Credit Union Expand.Enhance.Empower loan "
            "programme and Stanislaus Equity Partners. Beware of older guides quoting Modesto's "
            "\"ADU Development Fees 2022-2023\" document &mdash; that link is dead and the "
            "numbers are obsolete.</p>",
        )
        + section(
            "Conversions, as-built drawings and unpermitted space",
            "<p>If you are converting a garage, a workshop or an unpermitted living area, Modesto "
            "does not require a setback beyond what fire and safety need, allows expansion of up "
            "to 150 sq ft of the existing structure for ingress and egress, waives lot coverage "
            "limits for units of 800 sq ft or less, and prohibits the city from requiring you to "
            "correct non-conforming zoning conditions as a condition of approval.</p>"
            "<p>What reviewers will still need is a clear picture of how the structure actually "
            "exists today &mdash; that is what a conversion set of drawings has to document. "
            "California law also prevents the city from denying a permit because of building-code "
            "violations or unpermitted structures, as long as the ADU itself is built to code.</p>",
        )
    ),
    "faq1": (
        "Are ADUs allowed in Modesto? Yes. Modesto allows ADUs in any zone that permits "
        "single-family, multifamily or mixed-use development, and JADUs in single-family zones "
        "where a house exists or is proposed. Approval is ministerial with no public hearing, "
        "and the city must decide within 60 days of a complete application or the permit is "
        "deemed approved."
    ),
    "faq2": (
        "What is the maximum ADU size in Modesto? A detached ADU can be up to 1,200 sq ft and "
        "can never exceed the floor area of the main home. An attached ADU is capped at 50% of "
        "the main home's floor area, but the code states that cap cannot be used to refuse an "
        "attached ADU of up to 800 sq ft. A JADU is limited to 500 sq ft inside the walls of "
        "the house."
    ),
    "faq3": (
        "What are Modesto's ADU setback and parking requirements? A new detached ADU needs a "
        "minimum 4 ft side and 4 ft rear setback; a structure converted into an ADU only needs "
        "enough clearance for fire and safety. Parking is capped at one off-street space per "
        "ADU, and no space may be required when the unit is within 1/2 mile of transit, in a "
        "historic district, inside the main or accessory structure, on a permit-only street "
        "where the ADU occupant cannot get a permit, within a block of a car-share vehicle, or "
        "built together with a new dwelling permit on the same lot."
    ),
    "faqs": [
        {
            "q": "What does Modesto land use law say about ADUs?",
            "a": "ADUs are governed by the Modesto Municipal Code Title 10, Chapter 4, Article 5, sections 10-4.501 to 10-4.512. That article sets where ADUs are allowed, the size and height limits, setbacks, parking, the JADU owner-occupancy deed restriction and the fee rules, and it says that where a local standard conflicts with California Government Code section 66310 et seq., state law applies. It is a city code, not a county one: Stanislaus County's Chapter 21.74 has no force inside Modesto's city limits.",
        },
        {
            "q": "Does Modesto require a minimum ADU size?",
            "a": "No. Modesto's code sets no minimum floor area for an ADU, and California law forbids a minimum that would prevent an efficiency unit. Guides quoting a 150 sq ft minimum for Modesto are not supported by the current code.",
        },
        {
            "q": "How much does a Modesto ADU permit cost?",
            "a": "$2,429 per permit for an ADU or small dwelling up to 1,200 sq ft under the FY 2026-27 fee schedule, including mechanical, plumbing and electrical, payable when you apply. Separately, no impact fee applies to an ADU under 750 sq ft, and larger units are charged proportionally to the main home rather than at full new-house rates.",
        },
        {
            "q": "Can I convert my garage into an ADU in Modesto?",
            "a": "Yes. A conversion inside or replacing an existing structure needs only enough setback for fire and safety, may expand the structure by up to 150 sq ft for ingress and egress, is exempt from lot coverage limits up to 800 sq ft, and the lost parking does not have to be replaced.",
        },
        {
            "q": "Do I have to live in the property to rent out a Modesto ADU?",
            "a": "No for an ADU \u2014 Modesto does not require owner occupancy for ADUs, and state law bars the requirement. A JADU is different: before final inspection the owner must record a deed restriction agreeing to live in the JADU or the rest of the house at all times, unless the owner is a government agency, land trust or housing organisation. Rentals must run 30 days or longer.",
        },
        {
            "q": "How long does a Modesto ADU permit take?",
            "a": "Ministerial review must be completed within 60 days of a complete application, and if the city takes no action the ADU is deemed approved. Modesto also runs ADU Express, an appointment-based session that reviews an eligible ADU with Building Safety, Fire, Planning and Engineering at once and can approve it the same day when the plans are prepared by a licensed professional.",
        },
    ],
    "sources": [
        {"label": "Modesto Municipal Code Title 10, Ch. 4, Art. 5 &mdash; Accessory Dwelling Units (Municode)", "url": "https://library.municode.com/ca/modesto/codes/code_of_ordinances?nodeId=TIT10ZORE_CH4DEST_ART5ACDWUN"},
        {"label": "City of Modesto &mdash; Accessory Dwelling Units program page", "url": "https://www.modestogov.com/2845/Accessory-Dwelling-Units"},
        {"label": "City of Modesto &mdash; ADU Express flyer (PDF)", "url": "https://www.modestogov.com/DocumentCenter/View/26117"},
        {"label": "City of Modesto &mdash; Building Safety fees (FY 2026-27)", "url": "https://www.modestogov.com/3308/Building-Safety-Fees"},
        {"label": "California Government Code Chapter 13 &mdash; Accessory Dwelling Units (sections 66310 to 66342)", "url": "https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?lawCode=GOV&division=1.&title=7.&part=&chapter=13.&article="},
        {"label": "HCD &mdash; ADU Handbook (January 2025)", "url": "https://www.hcd.ca.gov/sites/default/files/docs/policy-and-research/adu-handbook-update.pdf"},
        {"label": "Stanislaus County &mdash; ADUs and free plan sets (unincorporated areas; plan sets usable in Modesto)", "url": "https://www.stancounty.com/planning/ADUs/"},
    ],
}

PAR_VILLE = {"bellevue": BELLEVUE, "vallejo": VALLEJO, "modesto": MODESTO}


def main():
    villes = json.load(open(FICHIER, encoding="utf-8"))
    par_nom = {c["city"].lower(): c for c in villes}

    # 1. max_size : les valeurs stockees sont des nombres nus ("1,200") alors que le
    #    gabarit n'ajoute plus "sq ft" -> on ajoute l'unite.
    normalisees = 0
    for c in villes:
        v = (c.get("max_size") or "").strip()
        if v and not re.search(r"(sq|square)\s*ft", v, re.I):
            c["max_size"] = f"{v} sq ft"
            normalisees += 1

    # 2. contenu verifie
    for cle, donnees in PAR_VILLE.items():
        c = par_nom.get(cle)
        if c is None:
            print(f"⚠️  ville absente: {cle}")
            continue
        c.update(donnees)

    json.dump(villes, open(FICHIER, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"max_size normalisees: {normalisees} villes")
    for cle in PAR_VILLE:
        c = par_nom[cle]
        mots = len(re.sub(r"<[^>]+>", " ", c.get("long_content", "")).split())
        print(
            f"  {c['city']}: {len(c.get('faqs', [])) + 3} FAQ, "
            f"{len(c.get('sources', []))} sources, ~{mots} mots de contenu long"
        )


if __name__ == "__main__":
    main()
