# AQI Tower Phase 15 — Bill of Materials and Procurement Table

**PHASE 15 — PROCUREMENT PLANNING ONLY**
**STATUS: SPECIFICATION DOCUMENT — NO PURCHASE MADE**
**Date: 2026-09-06**

All items are classified by procurement status:
- **VERIFIED PRODUCT** — confirmed to exist with cited evidence and example price
- **CANDIDATE PRODUCT** — believed to be available; price indicative, not a quote
- **GENERIC REQUIREMENT** — functional specification only; specific product not selected
- **REQUIRES QUOTE** — specification is clear but current India price/availability not confirmed
- **UNKNOWN** — availability and price both require investigation

India prices where stated are observed single-distributor listings on the stated date; they are not procurement commitments and do not include GST, shipping, or import duty unless noted. Prices marked as volatile or observed may have changed.

---

## Category 1 — Column and Pressure Hardware

| # | Item | Specification | Example product / vendor | Evidence | Qty | Priority | Est. cost | Status |
|---|---|---|---|---|---|---|---|---|
| 1.1 | Test column body | SS316 tube, 75 mm ID, ≥ 200 mm length, flanged ends; or equivalent borosilicate glass chromatography column | Custom SS fabrication (local workshop) or Sigma-Aldrich chromatography column 65 mm–75 mm ID | GENERIC REQUIREMENT | 1 | MUST BUY | REQUIRES QUOTE | GENERIC REQUIREMENT |
| 1.2 | Flanged end caps (pair) | SS316, 75 mm bore, flat or dished; drilled for 1/8" NPT sample port + pressure tap | Local SS fabrication | GENERIC REQUIREMENT | 2 | MUST BUY | REQUIRES QUOTE | GENERIC REQUIREMENT |
| 1.3 | SS316 retaining screens | 2.0 mm opening woven wire mesh, 75 mm diameter discs | Scientific mesh suppliers India (IndiaMART: woven wire mesh discs) | CANDIDATE PRODUCT | 6 | MUST BUY | REQUIRES QUOTE | CANDIDATE PRODUCT |
| 1.4 | Inlet distributor / perforated plate | SS316 perforated plate ≥ 30% open area, 75 mm disc, or sintered SS disc | Local fabrication or SS perforated sheet cut to disc | GENERIC REQUIREMENT | 2 | MUST BUY | REQUIRES QUOTE | GENERIC REQUIREMENT |
| 1.5 | PTFE sheet gaskets | 1–2 mm flat PTFE for flange seals | Standard industrial PTFE sheet, cut to flange size | CANDIDATE PRODUCT | 1 sheet | MUST BUY | ~₹500–1,000 | CANDIDATE PRODUCT |
| 1.6 | Differential pressure sensor | 0–500 Pa range, ≤1 Pa resolution, I²C or 4–20 mA output, SS or PTFE wetted parts | Sensirion SDP510 (+500 Pa, I²C) — CANDIDATE; or Honeywell HSC series — CANDIDATE | Sensirion product page; RS Components | 1 (2 preferred) | MUST BUY | REQUIRES QUOTE | CANDIDATE PRODUCT |
| 1.7 | DP sensor reference / check manometer | Inclined water manometer or calibrated digital reference, 0–500 Pa | Laboratory equipment supplier | GENERIC REQUIREMENT | 1 | MUST BUY | REQUIRES QUOTE | GENERIC REQUIREMENT |
| 1.8 | Pressure tap tubing | 3 mm OD SS or PTFE, 500 mm lengths | Standard SS/PTFE tubing, India suppliers | CANDIDATE PRODUCT | 2 lengths | MUST BUY | ~₹200–500 | CANDIDATE PRODUCT |
| 1.9 | Column stand / clamp | Lab retort stand + column clamps, vertical mounting | Standard lab equipment | GENERIC REQUIREMENT | 1 set | MUST BUY | ~₹500–1,500 | GENERIC REQUIREMENT |

**Fabrication note:** For the minimum viable tier, a transparent acrylic column body (ID = 75 mm) can be fabricated from acrylic tube stock by a local plastics supplier. Acrylic has known HCHO adsorption at low ppb; acceptable for pressure-drop (clean air) tests but must NOT be used for breakthrough tests with HCHO unless a blank test confirms negligible uptake under the test conditions. For breakthrough tests, SS316 or borosilicate glass is required.

---

## Category 2 — Flow Measurement and Control

| # | Item | Specification | Example product / vendor | Evidence | Qty | Priority | Est. cost | Status |
|---|---|---|---|---|---|---|---|---|
| 2.1 | Rotameter, 0–100 L/min air | Acrylic float, scale in L/min, needle valve at inlet, ±3% FS accuracy | Shree Aashapura Instrument, Mumbai, IndiaMART | IndiaMART listing observed ₹1,950 | 1 | MUST BUY | ~₹1,950 | CANDIDATE PRODUCT |
| 2.2 | Rotameter, 0–300 L/min air | Acrylic or SS float, for U_s = 0.52–1.05 m/s at 75 mm column | IndiaMART vendors; Deluxe Gases Pune | IndiaMART listings | 1 | MUST BUY | REQUIRES QUOTE | CANDIDATE PRODUCT |
| 2.3 | Needle valves (SS) | 1/4" or 3/8" NPT SS, fine adjustment; one per rotameter | Industrial valves, IndiaMART | CANDIDATE PRODUCT | 2 | MUST BUY | ~₹300–800 each | CANDIDATE PRODUCT |
| 2.4 | MFC, zero air, 0–80 L/min | Thermal mass flow controller, air, calibrated ±1% FS, for breakthrough tests | Alicat MC-50SLPM or 100SLPM, Bronkhorst EL-FLOW | International; India distributor UNKNOWN | 1 | RECOMMENDED | REQUIRES QUOTE | REQUIRES QUOTE |
| 2.5 | MFC, standard gas, 0–2 L/min | Thermal MFC, N₂ or air, calibrated ±1% FS, for HCHO cylinder dilution | Alicat MC-2SLPM, Bronkhorst | International; India distributor UNKNOWN | 1 | RECOMMENDED | REQUIRES QUOTE | REQUIRES QUOTE |
| 2.6 | Air compressor or lab bench supply | Oil-free compressor, ≥ 300 L/min at 2 bar; or lab building compressed air line | Local supplier; facility | GENERIC REQUIREMENT | 1 | MUST BUY or BORROW | Facility dependent | GENERIC REQUIREMENT |
| 2.7 | Air treatment (for zero air) | Activated carbon trap + molecular sieve (4A) + particulate filter, inline; verify HCHO blank < 5 µg/m³ | Gas filtration components, scientific supplier | GENERIC REQUIREMENT | 1 set | MUST BUY | REQUIRES QUOTE | GENERIC REQUIREMENT |

---

## Category 3 — HCHO Sensing

| # | Item | Specification | Example product / vendor | Evidence | Qty | Priority | Est. cost | Status |
|---|---|---|---|---|---|---|---|---|
| 3.1 | Sensirion SFA30-D-T module | 0–1000 ppb HCHO, I²C/UART, integrated T/RH, 3.3 V | E Control Devices India | ₹7,099 observed (one distributor, 2026-09-06) | 3 (2 active + 1 spare) | MUST BUY | ~₹21,300 | CANDIDATE PRODUCT |
| 3.2 | SFA30 breakout board / adapter | ZIF connector breakout for 7-pin SFA30 connector; or use SparkFun SEN-17228 | SparkFun (international) or custom PCB | SparkFun product page | 2 | MUST BUY | ~$10–15 USD each + import | CANDIDATE PRODUCT |
| 3.3 | 3.3 V power supply | Regulated 3.3 V, ≥ 200 mA; USB or linear regulator module | Standard electronics component | CANDIDATE PRODUCT | 2 | MUST BUY | ~₹50–200 each | CANDIDATE PRODUCT |
| 3.4 | I²C interface wiring | 100 mm–500 mm shielded cables; PTFE-insulated preferred | Standard electronics component | GENERIC REQUIREMENT | 1 set | MUST BUY | ~₹200 | GENERIC REQUIREMENT |

---

## Category 4 — HCHO Reference Analysis (DNPH / HPLC)

| # | Item | Specification | Example product / vendor | Evidence | Qty | Priority | Est. cost | Status |
|---|---|---|---|---|---|---|---|---|
| 4.1 | DNPH sampling cartridges | DNPH-coated silica, Sep-Pak type or Supelco LpDNPH S10; store refrigerated, protected from light | Waters, Sigma-Aldrich India, HiMedia | Sigma-Aldrich US listed; India UNKNOWN | 20 minimum per campaign | MUST BUY | REQUIRES QUOTE | CANDIDATE PRODUCT |
| 4.2 | Sampling pump (personal air) | Constant-flow pump 0.5–2 L/min, ±2% calibrated; compatible with HCHO environment | SKC Pocket Pump, Gillian BDX-II, or equivalent | CANDIDATE PRODUCT | 2 | MUST BUY | REQUIRES QUOTE | CANDIDATE PRODUCT |
| 4.3 | Rotameter for DNPH pump calibration | Calibrated bubble/electronic soap-film flowmeter or calibration rotameter | DryCal or similar | CANDIDATE PRODUCT | 1 | MUST BUY | REQUIRES QUOTE | CANDIDATE PRODUCT |
| 4.4 | Sample vials (amber glass) | 2 mL amber HPLC vials + caps; PTFE-lined caps | Standard laboratory supply, HiMedia India | CANDIDATE PRODUCT | 50 per campaign | MUST BUY | ~₹5–15 each | CANDIDATE PRODUCT |
| 4.5 | External HPLC analysis service | ISO/IEC 17025 accredited carbonyl analysis; formaldehyde-DNPH by HPLC/UV; report µg/m³ + expanded uncertainty | NABL-accredited lab; e.g., Bureau Veritas India, CSIR-NEERI collaboration | REQUIRES QUOTE; institutional collaboration preferred | Per campaign | BORROW / OUTSOURCE | REQUIRES QUOTE | REQUIRES QUOTE |

---

## Category 5 — T/RH Measurement

| # | Item | Specification | Example product / vendor | Evidence | Qty | Priority | Est. cost | Status |
|---|---|---|---|---|---|---|---|---|
| 5.1 | SFA30 integrated T/RH | Provided by the SFA30 module (see Category 3) | — | Sensirion DS v1.3 | — | INCLUDED | See Cat. 3 | VERIFIED PRODUCT |
| 5.2 | Reference T/RH probe (stress tests only) | Calibrated probe ±0.5°C / ±2% RH; e.g., E+E EE33, Vaisala HMP series | E+E Elektronik India Private Limited | India presence confirmed (IndiaMART) | 1 | RECOMMENDED | REQUIRES QUOTE | CANDIDATE PRODUCT |

---

## Category 6 — HCHO Generation System

| # | Item | Specification | Example product / vendor | Evidence | Qty | Priority | Est. cost | Status |
|---|---|---|---|---|---|---|---|---|
| 6.1 | HCHO certified gas cylinder | 5–50 ppm HCHO in zero air or N₂; NIST/NPL-traceable; ±2% certified | BOC India, Linde India, NCL Pune | REQUIRES QUOTE | 1 | MUST BUY (for breakthrough) | REQUIRES QUOTE | REQUIRES QUOTE |
| 6.2 | Cylinder regulator (SS diaphragm) | SS two-stage regulator for HCHO gas; PTFE seat; 0–2 bar outlet | Matheson or equivalent | GENERIC REQUIREMENT | 1 | MUST BUY (for breakthrough) | REQUIRES QUOTE | GENERIC REQUIREMENT |
| 6.3 | MFCs | See Category 2, items 2.4 and 2.5 | — | — | — | RECOMMENDED | REQUIRES QUOTE | REQUIRES QUOTE |
| 6.4 | Static mixer | 150 mm SS or PTFE tube with turbulence inserts | Lab fabrication or inline mixer supplier | GENERIC REQUIREMENT | 1 | MUST BUY | REQUIRES QUOTE | GENERIC REQUIREMENT |
| 6.5 | Humidifier | Nafion membrane humidifier or SS bubbler; delivers controlled RH to carrier air | Perma Pure Nafion or equivalent; India availability UNKNOWN | CANDIDATE PRODUCT | 1 | MUST BUY (for breakthrough) | REQUIRES QUOTE | REQUIRES QUOTE |
| 6.6 | HCHO exhaust scrubber | Carbon scrubber or KMnO₄ scrubber rated for HCHO; or routed to institution fume-hood exhaust | Institutional facility (preferred) or Purafil CC media | GENERIC REQUIREMENT | 1 | MUST BUY | Facility dependent | GENERIC REQUIREMENT |
| 6.7 | Area HCHO safety monitor | Independent calibrated HCHO monitor; alarm ≤ 0.05 ppm; not the SFA30 | Dräger Pac 7000, RAE Systems, or equivalent | CANDIDATE PRODUCT | 1 | MUST BUY | REQUIRES QUOTE | CANDIDATE PRODUCT |

---

## Category 7 — Tubing and Fittings

| # | Item | Specification | Example product / vendor | Evidence | Qty | Priority | Est. cost | Status |
|---|---|---|---|---|---|---|---|---|
| 7.1 | PTFE tubing | 6 mm OD × 4 mm ID PTFE; all wetted lines downstream of HCHO injection | SS/PTFE supplier IndiaMART, Pune | CANDIDATE PRODUCT | 5 m | MUST BUY | ~₹200–500/m | CANDIDATE PRODUCT |
| 7.2 | SS316 tubing (upstream) | 6 mm OD SS316 for lines that may contact HCHO | Industrial tube supplier | CANDIDATE PRODUCT | 2 m | MUST BUY | REQUIRES QUOTE | CANDIDATE PRODUCT |
| 7.3 | PTFE or SS compression fittings | 6 mm Swagelok-type or Parker A-Lok, SS316 | Swagelok India (Mumbai, Pune offices) | CANDIDATE PRODUCT | 20 | MUST BUY | REQUIRES QUOTE | CANDIDATE PRODUCT |
| 7.4 | T-fittings (PTFE or SS) | 6 mm three-way T for sample-port branches | Swagelok India or equivalent | CANDIDATE PRODUCT | 4 | MUST BUY | REQUIRES QUOTE | CANDIDATE PRODUCT |
| 7.5 | Ball valves (SS, PTFE seat) | 1/4" SS ball valve with PTFE seat for bypass / isolation | Industrial valve supplier, IndiaMART | CANDIDATE PRODUCT | 4 | MUST BUY | ~₹300–600 each | CANDIDATE PRODUCT |

---

## Category 8 — Data Acquisition and Logging

| # | Item | Specification | Example product / vendor | Evidence | Qty | Priority | Est. cost | Status |
|---|---|---|---|---|---|---|---|---|
| 8.1 | Raspberry Pi 4B (or equivalent) | Linux SBC, I²C + UART capable, USB; runs Python logging script | Raspberry Pi Foundation; available at Robu.in, Evelta India | CANDIDATE PRODUCT | 1 | MUST BUY | ~₹5,000–7,000 | CANDIDATE PRODUCT |
| 8.2 | I²C multiplexer (TCA9548A) | Allows two SFA30s on same I²C bus (different addresses possible; check SFA30 address config) | Adafruit, Robu.in | CANDIDATE PRODUCT | 1 | MUST BUY | ~₹200–400 | CANDIDATE PRODUCT |
| 8.3 | Analog-to-digital converter (for DP sensor) | 16-bit ADC if DP sensor has analog output (4–20 mA → voltage divider) | ADS1115 or similar, Robu.in | CANDIDATE PRODUCT | 1 | MUST BUY | ~₹150–400 | CANDIDATE PRODUCT |
| 8.4 | Real-time clock module | Battery-backed RTC (DS3231) for accurate timestamping | Robu.in, Amazon.in | CANDIDATE PRODUCT | 1 | MUST BUY | ~₹100–300 | CANDIDATE PRODUCT |
| 8.5 | SD card for local logging | 32 GB microSD, class 10 | Standard | CANDIDATE PRODUCT | 2 | MUST BUY | ~₹300–500 | CANDIDATE PRODUCT |
| 8.6 | USB keyboard and monitor | For Raspberry Pi setup; not required for headless operation | Standard | GENERIC REQUIREMENT | — | CAN BORROW | — | GENERIC REQUIREMENT |
| 8.7 | Enclosure (IP54 or better) | Protects DAQ electronics from laboratory humidity | ABS enclosure, IndiaMART | CANDIDATE PRODUCT | 1 | RECOMMENDED | ~₹300–800 | CANDIDATE PRODUCT |

---

## Category 9 — Activated Carbon Media

| # | Item | Specification | Example product / vendor | Evidence | Qty | Priority | Est. cost | Status |
|---|---|---|---|---|---|---|---|---|
| 9.1 | Calgon Carbon OVC 4×8 | Steam-activated coconut-shell GAC; 4×8 US mesh; min. CTC activity 60; lot certificate and SDS required | Kuraray/Calgon Carbon India (Calgon Carbon India LLP) | Kuraray India presence confirmed; exact OVC 4×8 availability in India UNKNOWN | 1–2 kg | MUST BUY | REQUIRES QUOTE | REQUIRES QUOTE |
| 9.2 | Calgon Carbon FORMASORB | HCHO-specific impregnated coconut-shell GAC; 4×8 or 6×12 mesh; lot certificate and SDS required | Kuraray/Calgon Carbon India | Availability in India UNKNOWN | 0.5–1 kg | MUST BUY (for comparison) | REQUIRES QUOTE | REQUIRES QUOTE |

**Procurement note:** Contact Kuraray India (`www.kuraray.com/in-en/`) and Calgon Carbon India for OVC 4×8 and FORMASORB stock, MOQ, SDS, and pricing. If Calgon/Kuraray cannot supply in India at acceptable MOQ, request samples through a global order. Do not substitute with unverified e-commerce activated charcoal.

---

## Category 10 — Safety Equipment

| # | Item | Specification | Example product / vendor | Evidence | Qty | Priority | Est. cost | Status |
|---|---|---|---|---|---|---|---|---|
| 10.1 | Half-face respirator with HCHO cartridge | NIOSH-approved or EN 140 equivalent; A1 or OV cartridge rated for formaldehyde | 3M 6502QL + 3M 6001 (OV/HCHO) or equivalent | CANDIDATE PRODUCT | 2 sets | MUST BUY | ~₹1,000–3,000/set | CANDIDATE PRODUCT |
| 10.2 | Chemical splash goggles | Indirect-vent, EN 166 or ANSI Z87.1 | Standard safety supplier | CANDIDATE PRODUCT | 2 pair | MUST BUY | ~₹200–500/pair | CANDIDATE PRODUCT |
| 10.3 | Chemical-resistant gloves | Nitrile ≥ 0.2 mm; or Viton for extended contact | Standard lab supply | CANDIDATE PRODUCT | 1 box | MUST BUY | ~₹300–600 | CANDIDATE PRODUCT |
| 10.4 | Lab coat (chemical resistant) | Cotton or Nomex; minimum requirement per institutional policy | Standard lab supply | GENERIC REQUIREMENT | 2 | MUST BUY | ~₹500–1,500 | GENERIC REQUIREMENT |
| 10.5 | Spill kit | Absorbent pads; sodium bisulfite solution neutralizes HCHO spills | Standard lab safety kit | GENERIC REQUIREMENT | 1 | MUST BUY | ~₹500–2,000 | GENERIC REQUIREMENT |

---

## Procurement Classification Summary

| Category | Must buy | Can fabricate | Borrow / outsource |
|---|---|---|---|
| Column and pressure hardware | Items 1.4–1.9 | Items 1.1–1.3 (custom fabrication) | 1.7 (reference manometer — may borrow) |
| Flow measurement | 2.1, 2.3; 2.4–2.5 (recommended) | 2.7 (air treatment, can assemble) | 2.6 (air supply — facility) |
| HCHO sensing | 3.1–3.4 | — | — |
| DNPH reference | 4.1–4.4 | — | 4.5 (HPLC service — outsource) |
| T/RH | Included in SFA30 | — | 5.2 (borrow from lab if possible) |
| HCHO generation | 6.1–6.7 | 6.4 (static mixer) | 6.6 (exhaust — facility); full system (institutional lab) |
| Tubing and fittings | 7.1–7.5 | — | — |
| DAQ | 8.1–8.7 | — | 8.6 (monitor/keyboard — borrow) |
| Media | 9.1–9.2 | — | — |
| Safety | 10.1–10.5 | — | — |

---

## Cost Tiers

### Minimum Viable — lowest-cost scientifically defensible setup

Assumes: pressure-drop tests only (no HCHO); no MFC; acrylic column; rotameter flow control; Raspberry Pi DAQ; SFA30 for T/RH only; institutional laboratory for HCHO work when ready.

| Sub-category | Approximate total |
|---|---|
| Acrylic column body + fabrication | REQUIRES QUOTE (est. ~₹3,000–8,000 custom) |
| Retaining screens + fittings | ~₹2,000–5,000 |
| Differential pressure sensor (Sensirion SDP type) | REQUIRES QUOTE (est. ~₹2,000–5,000) |
| Rotameter 0–100 L/min | ~₹1,950 |
| Rotameter 0–300 L/min | REQUIRES QUOTE |
| Raspberry Pi 4B + accessories | ~₹6,000–8,000 |
| SFA30 × 2 (T/RH + orientation check; not HCHO for breakthrough) | ~₹14,200 (₹7,099 × 2) |
| SFA30 breakout boards | ~₹1,500–3,000 |
| PTFE tubing + fittings | ~₹3,000–6,000 |
| Media samples (OVC 4×8) | REQUIRES QUOTE |
| Safety (PPE only) | ~₹3,000–6,000 |
| **Estimated subtotal (India-sourced items only)** | **~₹37,000–53,000 + multiple REQUIRES QUOTE items** |

**HCHO breakthrough testing is NOT included in minimum viable.** It requires institutional laboratory access, MFCs, certified gas cylinder, and DNPH analysis — all in the recommended or reference tier.

### Recommended — best balance of accuracy and cost

Adds: SS316 column body, calibrated MFCs for breakthrough testing, certified HCHO cylinder, DNPH cartridges, external HPLC service, one reference T/RH probe, better DP sensor.

| Additional items vs. minimum viable | Approximate additional cost |
|---|---|
| SS316 column + flanged end caps (fabrication) | REQUIRES QUOTE (est. ~₹8,000–20,000) |
| Differential pressure sensor upgrade (calibrated industrial) | REQUIRES QUOTE |
| MFCs × 2 (zero air + standard gas) | REQUIRES QUOTE (est. US$500–1,500 each; India import) |
| HCHO certified cylinder + regulator | REQUIRES QUOTE (BOC/Linde India) |
| DNPH cartridges × 20 + vials | REQUIRES QUOTE |
| HPLC analysis (external lab, 1 campaign) | REQUIRES QUOTE |
| Area HCHO safety monitor | REQUIRES QUOTE (est. ₹30,000–80,000 for industrial monitor) |
| Humidifier for RH conditioning | REQUIRES QUOTE |
| Reference T/RH probe | REQUIRES QUOTE |
| **Additional estimated total** | **REQUIRES QUOTE — most items need supplier quotes** |

### Reference-grade — higher-confidence laboratory setup

Adds: HPLC instrument access (institutional; not purchased); calibrated optical HCHO analyzer (e.g., Picarro cavity ring-down if available as a loan); three-point DP sensor calibration; NIST-traceable cylinder with independent analytical verification before first test; professional fabricated SS column with integrated pressure taps.

**All items in this tier are REQUIRES QUOTE or BORROW/OUTSOURCE.**

The reference tier is the appropriate level for a peer-reviewed publication; the recommended tier is appropriate for a well-documented student project with institutional laboratory support.

---

## Critical Procurement Blockers

These items must be resolved before any breakthrough testing can begin:

1. **Institutional safety approval** — no purchase of HCHO cylinder until written institutional approval exists
2. **OVC 4×8 and FORMASORB availability and MOQ in India** — contact Kuraray/Calgon Carbon India; if unavailable, all breakthrough planning depends on international procurement
3. **Certified HCHO gas cylinder** (BOC/Linde India) — REQUIRES QUOTE; lead time unknown; import may be required
4. **MFCs** — no current India price found; likely imported; lead time 4–12 weeks
5. **External HPLC laboratory** — identify and confirm an external laboratory before buying DNPH cartridges; laboratory must confirm they can perform ISO 16000-3 or TO-11A carbonyl analysis
6. **Column fabrication** — need a local SS/glass fabricator who can produce a 75 mm ID leak-tight column at an acceptable price

---

## Procurement Priority Order

For a student project starting from scratch, the following sequence is recommended:

1. **Immediately:** contact Kuraray/Calgon Carbon India for OVC 4×8 and FORMASORB samples; contact BOC/Linde India for HCHO cylinder options; identify institutional HPLC laboratory
2. **Next:** buy Raspberry Pi, SFA30 modules, rotameters, PTFE tubing, and basic fittings — these are available now at known prices and needed for rig assembly and clean-air pressure-drop tests
3. **After rig assembly:** buy differential pressure sensor; fabricate or buy column body; perform clean-air pressure-drop tests with OVC media
4. **After institutional safety approval:** order HCHO cylinder, MFCs, DNPH cartridges, scrubber media, and area safety monitor; book external HPLC service
5. **Last:** perform breakthrough tests under institutional supervision

---

*References: all Phase 14, 13 documents and Phase 15 engineering spec; individual item sources cited inline.*
