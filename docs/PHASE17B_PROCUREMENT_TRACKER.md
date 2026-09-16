# AQI Tower Phase 17B — Procurement Tracker

**PHASE 17B — PROCUREMENT UNBLOCK**
**STATUS: RFQ READY — NO ITEMS ORDERED YET**
**Date: 2026-09-07**

---

## Legend

**Priority:**
- P0 — Blocking Phase 17A (Stage A empty-rig and Stage B 26 mm bed at baseline velocity)
- P1 — Required for full velocity matrix (Stages C, D; U_s ≥ 0.52 m/s)
- P2 — Useful verification; not strictly required for first results
- P3 — HCHO-only; do not purchase until Phase 17B+ approval

**Status:**
- NOT CONTACTED — no inquiry sent
- RFQ READY — letter drafted, not yet sent
- RFQ SENT — inquiry submitted; awaiting response
- QUOTE RECEIVED — price and availability confirmed
- ORDERED — purchase placed
- RECEIVED — item physically in hand
- BLOCKED — inquiry made; supplier unable to fulfil

**Category:**
- MUST HAVE — cannot run Phase 17A without this item
- CAN BORROW — available from institutional lab; request before ordering
- CAN FABRICATE — custom-made locally; requires drawing and workshop quote
- BUY LATER — not needed for clean-air Phase 17A
- OUTSOURCE — external service; not purchased directly

---

## Table 1 — P0 Blocking Items (all MUST HAVE before Phase 17A Stage A)

| ID | Item | Exact Model / Spec | Supplier | Price (India) | MOQ | Lead Time | Status | Category | Action |
|---|---|---|---|---:|---|---|---|---|---|
| M-01 | OVC 4×8 GAC media | Calgon Carbon OVC 4×8; coconut-shell; 4×8 US mesh (2.36–4.75 mm); steam-activated; non-impregnated; CTC ≥ 60 wt% | Kuraray India / Chemet India (+91 22 6680 2222, info@chemetindia.com) | REQUIRES QUOTE | ~500 g minimum for Phase 17A baseline | Unknown | NOT CONTACTED | MUST HAVE | **Send RFQ immediately** — use letter in PHASE17B_OVC4X8_RFQ.md Part A |
| M-02 | SDP810-500Pa DP sensor | Sensirion SDP810-500Pa; ±500 Pa differential; I²C; 2.7–5.5 V; tube connection | Tanotis India (tanotis.com) — confirmed listing | **₹4,748.73 incl. taxes** (confirmed Tanotis, 2026-09-07) | 1 unit | Not stated | NOT CONTACTED | MUST HAVE | Order from tanotis.com; add to cart confirmed; buy 1 unit (consider buying 2 for redundancy) |
| M-03 | Rotameter A — 0–100 L/min | Air rotameter; float-type; acrylic body; 0–100 LPM range; ±2% FS; 1/4" or 1/2" BSP screwed; air service | Shree Aashapura Instrument, Mumbai (IndiaMART listing confirmed) | **₹1,950** (confirmed IndiaMART, 2026-09-07) | 1 unit | Not stated | NOT CONTACTED | MUST HAVE | Contact Shree Aashapura via IndiaMART; confirm air-service calibration and connection thread; place order |
| M-04 | SS316 needle valve | 1/4" NPT or 6 mm compression; stainless steel; for flow adjustment paired with Rotameter A | IndiaMART (Alfa Valves Bhosari or similar) | ~₹600–1,200 (estimate) | 1 unit | — | NOT CONTACTED | MUST HAVE | Search IndiaMART; request quote from 2 suppliers |
| M-05 | Acrylic column tube | 75 mm ID clear acrylic tube; total length 300 mm; wall ≥ 3 mm; transparent; round; no seam | IndiaMART acrylic suppliers (request 75 mm ID specifically — standard 75 mm OD has ~69 mm ID; confirm ID not OD) | REQUIRES QUOTE (~₹600–1,500 estimated) | 300 mm cut | — | NOT CONTACTED | CAN FABRICATE | Contact ≥ 2 IndiaMART acrylic tube suppliers; specify 75 mm ID (not OD); see fabrication spec Section 4 below |
| M-06 | Acrylic end caps (×2) | Machined from 10 mm acrylic sheet; 75 mm bore; O-ring groove 70 mm ID × 5 mm; two 6 mm compression ports per cap | Local machine shop (contact via university workshop or IndiaMART fabrication services) | REQUIRES QUOTE (~₹1,000–3,000 estimated) | 2 caps | — | NOT CONTACTED | CAN FABRICATE | Prepare dimensioned drawing; get workshop quote; see Section 4 below for full spec |
| M-07 | Viton O-rings | 70 mm ID × 5 mm cross-section; for column-to-cap seal; Viton (FKM) material; qty 6 (2 active + 4 spares) | IndiaMART (Seals India, Hydrojet, or O-ring suppliers in Mumbai/Pune) | ~₹50–120 each → ~₹300–720 for 6 | 6-piece set | — | NOT CONTACTED | MUST HAVE | Search IndiaMART; specify Viton (FKM) not NBR; confirm 70 mm ID × 5 mm CS |
| M-08 | SS316 wire mesh screens | Woven SS316; ≤ 2 mm opening (equivalent to 10 mesh or finer); for cutting 75 mm discs; qty: 1 sheet 100 × 100 mm | IndiaMART metalware suppliers | ₹16–75/sq ft (estimate) | 1 sheet | — | NOT CONTACTED | MUST HAVE | Search IndiaMART; confirm SS316 (not SS304); confirm ≤ 2 mm opening; buy enough for 10+ discs |
| M-09 | SHT40 T/RH breakout board | Sensirion SHT40; ±0.2°C / ±1.8% RH; I²C; 3.3 V; 2.54 mm or 1.27 mm header; qty 2 | Robu.in; Evelta Electronics; Amazon.in India | ~₹400–800 per board (estimate — not confirmed in this search) | 2 boards | — | NOT CONTACTED | MUST HAVE | Check Robu.in and Evelta for current price; buy 2 |
| M-10 | PTFE tubing | 6 mm OD × 4 mm ID; quantity 3 m; for pressure taps and flow connections | IndiaMART (Sealco Pune or similar) | ~₹85/m → ~₹255 for 3 m (estimate) | Per metre | — | NOT CONTACTED | MUST HAVE | Search IndiaMART; confirm chemical-grade PTFE; buy ≥ 3 m |
| M-11 | Compression fittings — straight (×4) | 6 mm OD; push-in or compression; SS316 or polypropylene body; for tube-to-cap connections | SMC India; Festo India; IndiaMART | ~₹80–180 each (estimate) | 4 | — | NOT CONTACTED | MUST HAVE | Get prices from SMC India or Festo India; or IndiaMART |
| M-12 | Compression fittings — tee (×2) | 6 mm OD tee; for pressure-tap branches | Same vendors as M-11 | ~₹120–250 each (estimate) | 2 | — | NOT CONTACTED | MUST HAVE | Same vendor as M-11 |
| M-13 | Raspberry Pi 4B (2 GB) | Raspberry Pi 4 Model B, 2 GB RAM; for I²C DAQ logging (SDP810 + SHT40) | Robu.in; Evelta Electronics; Amazon.in India | ~₹5,500–7,500 (estimate — confirm current price) | 1 | — | NOT CONTACTED | MUST HAVE | Check Robu.in and Evelta current listing prices; note RPi supply can vary |
| M-14 | MicroSD card (32 GB) | Class 10 or better; for RPi OS and data logging | Amazon.in / local electronics | ~₹400–600 (estimate) | 1 | — | NOT CONTACTED | MUST HAVE | Buy with RPi from same order |
| M-15 | RPi USB-C power supply (5 V 3 A) | Official RPi PSU or certified 3 A USB-C; for RPi 4B | Robu.in; Amazon.in | ~₹400–600 (estimate) | 1 | — | NOT CONTACTED | MUST HAVE | Buy with RPi |
| M-16 | Dupont/I²C cables | 4-wire (GND, 3V3, SDA, SCL); female-female Dupont jumpers; 20 cm; for SDP810 + SHT40 to RPi GPIO | Robu.in; local electronics market | ~₹50–150 (estimate) | 1 set | — | NOT CONTACTED | MUST HAVE | Buy with RPi order |
| M-17 | PTFE sheet gaskets | 1 mm thick; cut to 75 mm disc; for screen-to-end-cap seating; qty 4 | IndiaMART (Bhosari Pune or PTFE sheet supplier) | ~₹100–300/sheet (estimate) | 1 sheet | — | NOT CONTACTED | MUST HAVE | Cut from PTFE sheet; confirm 1 mm thickness |

**P0 estimated minimum spend (confirmed prices only):**
- SDP810-500Pa: ₹4,748.73
- Rotameter A: ₹1,950
- **Subtotal confirmed:** ₹6,698.73
- Remaining P0 items: mostly REQUIRES QUOTE or estimated; see Section 3 for minimum viable total

---

## Table 2 — P1 Items (needed for full velocity matrix U_s ≥ 0.52 m/s)

| ID | Item | Exact Model / Spec | Supplier | Price (India) | MOQ | Lead Time | Status | Category | Action |
|---|---|---|---|---:|---|---|---|---|---|
| P1-01 | Rotameter B — 0–300 L/min | Air rotameter; 0–300 LPM; acrylic body; ±2% FS; air service | Shree Aashapura Instrument, Mumbai (same supplier as Rotameter A) | REQUIRES QUOTE | 1 unit | — | NOT CONTACTED | MUST HAVE (for Stage C/D) | Request quote simultaneously with Rotameter A order; list separately |
| P1-02 | Testo 510 digital manometer | Testo 510; 0–100 hPa (10,000 Pa); 1 Pa resolution; rubber pressure tubes | IndiaMART — multiple listings confirmed: ₹9,999 (Ghaziabad) and ₹12,197 (Ahmedabad) | **₹9,999–12,197** (confirmed IndiaMART, 2026-09-07) | 1 unit | — | NOT CONTACTED | CAN BORROW (check institutional lab first) | Borrow from physics/civil/HVAC lab before purchasing; if unavailable buy from IndiaMART listing |
| P1-03 | SS316 needle valve (second) | Same as M-04; for Rotameter B flow control | Same vendor as M-04 | ~₹600–1,200 (estimate) | 1 | — | NOT CONTACTED | MUST HAVE (for Stage C/D) | Order with M-04 |

---

## Table 3 — P2 Items (verification; useful but not blocking)

| ID | Item | Exact Model / Spec | Supplier | Price | MOQ | Lead Time | Status | Category | Action |
|---|---|---|---|---:|---|---|---|---|---|
| P2-01 | DS3231 RTC module | Battery-backed I²C RTC; for RPi timestamp if no network available | Robu.in; Amazon.in India | ~₹150–350 (estimate) | 1 | — | NOT CONTACTED | MUST HAVE (if no lab network) | Buy with RPi order if lab has no reliable network |
| P2-02 | Laboratory balance (0.01 g resolution) | 200–500 g capacity; 0.01 g readability | Chemistry lab (borrow) | ₹0 | — | — | NOT CONTACTED | CAN BORROW | Request from chemistry department; do NOT purchase unless borrow is refused |
| P2-03 | Digital caliper (0.01 mm) | 150 mm range; 0.01 mm readability | Mechanical lab (borrow) or IndiaMART | ₹0 or ~₹500–800 | — | — | NOT CONTACTED | CAN BORROW | Borrow from mechanical workshop; buy only if unavailable |
| P2-04 | Drying oven (105 °C) | For media drying at 105 °C | Chemistry or materials lab (borrow) | ₹0 | — | — | NOT CONTACTED | CAN BORROW | Request from chemistry/materials lab; cannot be improvised |
| P2-05 | Bubble / soap-film flowmeter | For rotameter calibration check at 50 L/min | Physics lab or DIY (graduated burette) | ₹0 or ₹200–400 DIY | — | — | NOT CONTACTED | CAN BORROW / FABRICATE | Improvise from burette if not available |
| P2-06 | Desiccator (for media storage) | Sealed; with silica gel or desiccant | Chemistry lab (borrow) | ₹0 | — | — | NOT CONTACTED | CAN BORROW | Request from chemistry lab |
| P2-07 | Nitrile gloves (box of 100) | For media handling; any disposable nitrile | Lab supply store | ~₹300–600 | 1 box | — | NOT CONTACTED | MUST HAVE | Buy locally |

---

## Table 4 — P3 Items (HCHO-only; BUY LATER)

**Do not purchase any P3 item until Phase 17B+ institutional safety approval is obtained.**

| ID | Item | Notes | Status |
|---|---|---|---|
| P3-01 | FORMASORB (4×8 mesh) | Quote via same routes as OVC 4×8; confirm formaldehyde-specific grade; do not order until safety approval | RFQ READY — see PHASE17B_OVC4X8_RFQ.md Part B |
| P3-02 | Sensirion SFA30-D-T HCHO sensor ×2 + 1 spare | ₹7,099/unit observed (E Control Devices India, Phase 15); verify stock before ordering | NOT CONTACTED |
| P3-03 | Certified HCHO gas cylinder (BOC India / Linde India) | Requires institutional safety approval, signed permit, cylinder SDS, storage | NOT CONTACTED — DO NOT ORDER |
| P3-04 | Mass Flow Controllers ×2 (Alicat / Brooks / Bronkhorst) | Imported; $200–600 USD each; long lead time | NOT CONTACTED |
| P3-05 | Static mixer / mixing tee | SS316; for HCHO + air blending | NOT CONTACTED |
| P3-06 | DNPH cartridge sampling pump ×2 | SKC or Supelco; for ISO 16000-3:2022 reference sampling | NOT CONTACTED |
| P3-07 | DNPH cartridges (case of 50) | Consumable; from NABL lab or import | NOT CONTACTED |
| P3-08 | SS316 custom column (75 mm ID) | For Phase 17B+ HCHO breakthrough; acrylic NOT approved for HCHO | NOT CONTACTED |

---

## Table 5 — Outsource Items

| ID | Item | Service type | Provider type | Estimated cost | Status |
|---|---|---|---|---:|---|
| OS-01 | Column end cap machining | Machine acrylic end caps to spec (see Section 4) | Local precision workshop via university machine shop or IndiaMART fabricators | ~₹1,000–3,000 | NOT CONTACTED |
| OS-02 | Acrylic tube supply and cut | 75 mm ID clear acrylic; 300 mm cut | Local plastics fabricator via IndiaMART (specify 75 mm ID, not OD) | ~₹600–1,500 | NOT CONTACTED |
| OS-03 | HPLC/DNPH analysis | ISO 16000-3:2022 HCHO quantification | NABL/17025-accredited external laboratory | ~₹1,500–5,000/set | NOT YET NEEDED — Phase 17B+ only |

---

## 3. Minimum Phase 17A Purchase Package

This is the smallest set of purchases required to execute Stage A (empty-rig) and Stage B (26 mm bed) at baseline velocities (U_s = 0.13 and 0.26 m/s = Q = 34.5 and 68.9 L/min), borrowing the balance, Testo 510, RPi, oven, and caliper from institutional labs.

### MUST BUY (cannot borrow or fabricate cheaply)

| Item | Confirmed or Estimated India Price |
|---:|---:|
| SDP810-500Pa — M-02 (Tanotis India) | **₹4,748.73** (confirmed) |
| Rotameter A 0–100 LPM — M-03 (Shree Aashapura) | **₹1,950** (confirmed) |
| SS316 needle valve — M-04 | ~₹800 (estimate) |
| OVC 4×8 media, 500 g — M-01 | REQUIRES QUOTE |
| Viton O-rings — M-07 | ~₹400 |
| SS316 mesh screens — M-08 | ~₹400 |
| PTFE tubing 3 m — M-10 | ~₹255 |
| Compression fittings ×6 — M-11/M-12 | ~₹800 |
| SHT40 breakout ×2 — M-09 | ~₹1,000 (estimate) |
| PTFE gaskets — M-17 | ~₹300 |
| Nitrile gloves — P2-07 | ~₹400 |
| I²C cables — M-16 | ~₹100 |
| **Subtotal (excluding media, column, machining, RPi)** | **~₹11,153 + media quote** |

### CAN BORROW (confirm before ordering)

- Raspberry Pi 4B + SD card + PSU (request from CS department)
- Laboratory balance 0.01 g (request from chemistry)
- Digital caliper 0.01 mm (request from mechanical workshop)
- Drying oven 105 °C (request from chemistry or materials lab)
- Testo 510 (request from physics, civil, or HVAC lab)
- Desiccator (request from chemistry)

### CAN FABRICATE / OUTSOURCE

- Acrylic column tube 75 mm ID × 300 mm: quote from local plastics supplier (~₹600–1,500)
- Acrylic end caps ×2: quote from local machine workshop (~₹1,000–3,000)

### Estimated minimum total (MUST BUY only, before media and column costs)

**~₹11,153** (confirmed prices: ₹6,699; estimates: ~₹4,454)

**Add media quote result + column/fabrication quote to get full P0 total.**

---

## Phase 19 — Pre-filter Tower Items

**Added: 2026-09-07 (Phase 19). These items are TOWER HARDWARE, not bench-rig items. They are independent of Phase 17A and can be procured in parallel.**

| ID | Item | Spec | Supplier | Price | MOQ | Status | Action |
|---|---|---|---|---:|---|---|---|
| T-01 | G4 washable pre-filter panel × 2 | 592 × 592 × 48 mm; G4 (EN 779:2012); synthetic fibre media; galvanised steel frame; washable ≥ 12 cycles; EN 779 or ISO 16890 test certificate required | **PREFERRED:** Freudenberg India (info@freudenberg-filter.com, +91 20 67633600) **BACKUP:** Camfil India (info.in@camfil.com) | REQUIRES QUOTE | 2 units min | NOT CONTACTED | **Send RFQ simultaneously to Freudenberg and Camfil using spec in PHASE19_PREFILTER_SPECIFICATION.md §11.5** |
| T-02 | Inlet cassette frame × 1 | Sheet metal frame; outer 620 × 620 mm; 592 × 592 mm clear opening; depth 30 mm; galvanised steel 0.8–1.2 mm; filter slide-in from one side; drainage slot at bottom | Local sheet-metal workshop (IndiaMART / university workshop) | REQUIRES QUOTE (~₹500–2,000 estimate) | 1 | NOT CONTACTED | Prepare dimensioned drawing; request quote from 2 workshops |
| T-03 | EPDM foam gasket tape | Closed-cell EPDM; 10 mm wide × 6 mm deep; self-adhesive backing; 2.5 m total (perimeter of one 592 mm filter) | IndiaMART (foam sealant / gasket tape category) | ~₹200–400 per roll | 1 roll | NOT CONTACTED | Search IndiaMART "closed cell EPDM foam tape 10mm" |
| T-04 | Tower DP sensor — pre-filter | Sensirion SDP810-500Pa (same part as M-02); for permanent pre-filter ΔP monitoring in tower (separate from bench rig unit) | Tanotis India (tanotis.com) — confirmed | **₹4,748.73** (confirmed, 2026-09-07) | 1 unit | NOT CONTACTED | Order with M-02 if ordering simultaneously; 2 units total |
| T-05 | Wire spring retention clip | SS or carbon steel; clips inside cassette frame to hold filter panel seated | Local hardware / IndiaMART | ~₹50–150 | 2 clips | NOT CONTACTED | Specify after frame fabrication geometry is confirmed |

**Phase 19 tower pre-filter estimated total:**
- T-01 (filter × 2): REQUIRES QUOTE (~₹1,400–4,000 estimate)
- T-02 (cassette frame): REQUIRES QUOTE (~₹500–2,000 estimate)
- T-03 (gasket tape): ~₹300
- T-04 (tower DP sensor): ₹4,748.73 (confirmed)
- **Estimated total: ~₹6,950–11,050** (excluding fabrication uncertainty)

**Pre-filter RFQ priority:** The G4 pre-filter RFQ (T-01) can be sent immediately by combining it with any existing Freudenberg communication about the H13 HEPA. Use the RFQ spec in `docs/PHASE19_PREFILTER_SPECIFICATION.md` §11.5.

---

## 4. Column Fabrication Specification

**FOR CLEAN-AIR PRESSURE-DROP TESTING (PHASE 17A) ONLY.**

**ACRYLIC IS NOT APPROVED FOR HCHO BREAKTHROUGH TESTING. A separate SS316 or borosilicate-glass column must be used for any phase that introduces formaldehyde gas.**

### 4.1 Column tube

| Parameter | Specification |
|---|---|
| Material | Clear cast acrylic (PMMA); transparent; no seam |
| Internal diameter (ID) | **75.0 mm ± 0.5 mm** — confirm this is the INTERNAL diameter with supplier; do not accept OD-specified tube without measuring ID |
| Wall thickness | ≥ 3 mm (to give OD ≈ 81 mm; any consistent wall ≥ 3 mm acceptable) |
| Total tube length | 300 mm |
| Usable internal length | ≥ 250 mm (end-cap recess and O-ring groove account for remaining ~25 mm per end) |
| Surface finish | Inner bore smooth; no ridges, burrs, or internal weld lines |
| Optical clarity | Transparent (for visual inspection of media bed and fines) |
| Temperature rating | ≥ 50 °C (for clean-air tests at laboratory ambient; not required for high-temperature service) |
| Pressure rating | ≥ 10 kPa gauge (operating pressure well below this) |
| Quantity | 2 (one active + one spare) |

**Supplier note:** Many Indian acrylic tube suppliers list 75 mm by OD. Specify clearly: "75 mm internal diameter (ID), clear acrylic tube, 300 mm length, wall ≥ 3 mm." If supplier cannot supply exactly 75 mm ID, request the next available ID and document the actual measured value for use in all area calculations (A = π × ID² / 4).

### 4.2 End caps (×2, machined)

Each end cap:

| Parameter | Specification |
|---|---|
| Material | Clear acrylic (PMMA), 10–15 mm plate/block |
| Outer diameter | Match tube OD (≈ 81 mm) |
| Central bore | 75 mm ID (same as column bore; no step or ledge inside the flow path) |
| O-ring groove | On the outer cylindrical surface or on the face that contacts the tube; 70 mm ID × 5 mm cross-section (to seat a 70 × 5 Viton O-ring); depth = 3.5 mm, width = 5.5 mm (standard groove for 5 mm CS O-ring with 10% stretch) |
| Pressure tap port | One side port per end cap; 6 mm compression or 1/8" NPT female thread; flush with inner bore (no protrusion into flow path); located 10–15 mm from the end face |
| Sample port | One additional side port per end cap; 6 mm compression or 1/8" NPT female thread; for future HCHO/DNPH sampling in later phases (can be plugged for Phase 17A) |
| Screen seat recess | A 75 mm ID × 1 mm deep recess just inside the tube bore on each end cap to locate the SS316 wire-mesh screen disc and prevent it shifting during flow |
| Fastening | 4× M4 or M5 screws through flanged collar or hose clamps around tube OD; or compression clamp; end cap must be removable without tools if possible |
| Bed-depth scale | Engrave or mark a ruler scale (mm) on the outside of the acrylic tube at 10 mm intervals (0–200 mm from the lower screen position) to read settled bed depth during packing |

### 4.3 Screen and gasket assembly (per end cap)

- 1× SS316 wire-mesh disc, 75 mm diameter, ≤ 2 mm opening (prevents OVC 4×8 from exiting; min mesh size 10 mesh / ~2 mm clear opening)
- 1× PTFE sheet gasket, 75 mm disc, 1 mm thick, between screen and end-cap face to prevent metal-on-acrylic contact and leakage path

### 4.4 Flow orientation

Vertical column, bottom-to-top airflow:
- Bottom end cap = inlet (air enters upward through bed)
- Top end cap = outlet (air exits)
- Rotameter and flow control downstream (on the outlet/top side)
- Pressure taps: bottom tap = upstream (high pressure); top tap = downstream (low pressure); SDP810 reads upstream − downstream = positive value for pressure drop

### 4.5 Support and stand

- Mount column vertically in a ring stand or custom acrylic/aluminium bracket
- Column must be stable with no rocking during tamping; add rubber feet to stand
- Do not weld or epoxy end caps to tube — must remain disassemblable

### 4.6 Acrylic limitation notice

This specification is for clean-air testing only. If formaldehyde gas is ever introduced to the rig in a future phase:
1. The acrylic column must be replaced with SS316 or borosilicate glass before gas testing.
2. A blank test of any replacement column must be run before interpreting HCHO measurements.
3. Do not sand, cut, or machine the acrylic column near HCHO or flame sources.

---

## 5. Procurement Priority Summary

| Priority | Item | Blocker? | First Action |
|---|---|---|---|
| **P0** | OVC 4×8 media — M-01 | YES | Send RFQ (PHASE17B_OVC4X8_RFQ.md Part A) to Routes 1, 2, 3 today |
| **P0** | SDP810-500Pa — M-02 | YES | Order from tanotis.com (₹4,748.73); do today |
| **P0** | Rotameter A 0–100 LPM — M-03 | YES | Contact Shree Aashapura via IndiaMART (₹1,950); confirm and order |
| **P0** | Acrylic column + machining — M-05, M-06 | YES | Get quotes from 2 acrylic suppliers + 1 machine workshop; use spec in Section 4 |
| **P0** | RPi 4B (borrow or buy) — M-13 | YES | Request from CS/ECE department first; if unavailable, buy from Robu.in |
| **P0** | SHT40 ×2 — M-09 | YES | Check Robu.in / Evelta; order with RPi |
| **P0** | O-rings, mesh, PTFE, fittings — M-07/08/10–12/17 | YES | Place one IndiaMART order combining all small hardware |
| **P1** | Testo 510 — P1-02 | Only for high-velocity or backup | Borrow first; if unavailable, buy at ₹9,999–12,197 from IndiaMART |
| **P1** | Rotameter B 0–300 LPM — P1-01 | Only for U_s ≥ 0.52 m/s | Quote from Shree Aashapura simultaneously |
| **P3** | FORMASORB — P3-01 | NO (deferred) | Send quote request now; do NOT order yet |

---

## 6. Evidence and Sources Used

All prices and contacts below were checked 2026-09-07. Prices are subject to change; re-confirm before ordering.

| Item | Evidence | URL |
|---|---|---|
| SDP810-500Pa India price | Tanotis.com product page; "Add to cart" available; price ₹4,748.73 incl. taxes | https://www.tanotis.com/products/sensirion-sdp810-500pa-pressure-sensor-differential-500-pa-500-pa-2-7-v-5-5-v-sip |
| Rotameter A 0–100 LPM price | IndiaMART listing; Shree Aashapura Instrument, Mumbai | https://www.indiamart.com/proddetail/air-rotameter-in-flow-range-0-100-lpm-18378270973.html |
| Testo 510 India price | IndiaMART (Ghaziabad listing ₹9,999; Ahmedabad listing ₹12,197) | https://www.indiamart.com/proddetail/testo-510-digital-manometer-2855716613255.html |
| Kuraray India contact | Kuraray India official contact page | https://www.kuraray.com/in-en/contact-us/ |
| Kuraray Environmental Solutions contact | Carbon solutions contact form | https://go.kuraray.com/en/contact/carbon-solutions/ |
| Chemet India (Calgon Carbon distributor) | Chemet India supplier page for Calgon Carbon | https://chemetindia.com/supplier/calgon-carbon |
| Jacobi Carbons India | IndiaBiz / IndiaMART / Panjiva; address and phone confirmed | Phone: +91 422 4397208 or 097509 22307; email: infoin@jacobi.net |
| OVC 4×8 product page | Calgon Carbon official; OVC 4×8 grade confirmed | https://www.calgoncarbon.com/products/ovc/ |
| FORMASORB product page | Calgon Carbon official; formaldehyde-specific grade confirmed | https://www.calgoncarbon.com/products/formasorb/ |
| Acrylic tube India | IndiaMART (75 mm OD 3 mm wall ₹465/m — note: this is OD not ID) | https://www.indiamart.com/proddetail/white-acrylic-pipe-20751539791.html |

---

*See also: `docs/PHASE17B_OVC4X8_RFQ.md` for ready-to-send letters; `docs/PHASE17A_PRESSURE_DROP_RESULTS.md` for what the hardware will be used for; `docs/PHASE16_PROCUREMENT_PLAN.md` for the build order.*
