# AQI Tower Phase 16 — Procurement Plan

**PHASE 16 — CLEAN-AIR PRESSURE-DROP RIG ONLY**
**STATUS: SPECIFICATION — NO EXPERIMENT PERFORMED, NO CFD RUN**
**Date: 2026-09-06**

---

## 1. Scope

This document covers procurement decisions and the 15-step build order for the Phase 16 clean-air pressure-drop test system. It is restricted to clean-air measurements. All HCHO-related items (gas cylinder, MFCs, SFA30 sensors, DNPH cartridges) are listed under BUY LATER and must not be purchased until Phase 17 institutional safety approval is in place.

Phase 16 does **not** include HCHO testing, adsorption CFD, tower CFD changes, or tower CAD changes.

---

## 2. BUY NOW — Clean-Air Rig Items

These items are required to begin Stage A and Stage B testing. They involve no hazardous chemicals and do not require institutional safety approval beyond normal workshop access.

### 2.1 Column and media containment

| Item | Specification | Vendor / Source | Estimated India Price | Status |
|---|---|---|---:|---|
| Acrylic tube | 75 mm ID × 76 mm OD × 300 mm length; clear; round; no seam | Local plastics supplier (Ahmedabad / Mumbai / Pune / Delhi) | ₹500–1,200 | CANDIDATE PRODUCT — get quote from ≥ 2 suppliers |
| Acrylic end caps (×2) | Machined from 10 mm acrylic sheet; 75 mm bore; 2 side ports per cap; O-ring groove | Local machine shop (same supplier or separate) | ₹1,000–3,000 | FABRICATE — requires machining drawings |
| Viton O-rings (×2 + spares) | 70 mm ID × 5 mm cross-section; for column-to-cap seals | IndiaMART (Seals India, Hydrojet); ~₹50–120 each | ₹200–600 for 6-piece set | CANDIDATE PRODUCT |
| SS316 woven wire mesh | ≤ 2 mm opening; 75 mm disc cut; 2 per bed depth = 6 discs for all stages (plus spares) | IndiaMART metalware suppliers; mesh sheet ₹16–75/sq ft | ₹300–1,000 for 100 × 100 mm sheet + cutting | CANDIDATE PRODUCT |
| PTFE sheet gaskets | 1 mm thick; cut to 75 mm disc with bore matching mesh; used between screen and end cap | IndiaMART (Bhosari, Pune); ~₹100–300/sheet | ₹300–600 for 4 gaskets | CANDIDATE PRODUCT |

**Subtotal column + containment:** ~₹2,300–5,800

### 2.2 Differential pressure instruments

| Item | Specification | Vendor / Source | Estimated India Price | Status |
|---|---|---|---:|---|
| Sensirion SDP810-500Pa | ±500 Pa; I²C; 1 Pa resolution; 2.7–5.5 V | Tanotis India (tanotis.com) — CANDIDATE; international: DigiKey / Arrow ($15–25 USD ≈ ₹1,250–2,100 + shipping/duty) | ₹1,500–3,000 (estimated with import) | CANDIDATE PRODUCT — confirm India stock before ordering internationally |
| Testo 510 digital manometer | 0–100 hPa (0–10,000 Pa); 1 Pa resolution; rubber pressure tubes | testo.com/en-IN; toolbuy.com India | ~₹11,148 (observed) | CANDIDATE PRODUCT |
| Pressure tube adapters | Push-in fitting or compression fitting for 1.5 mm to 6 mm PTFE tube transition; ×2 | Local pneumatic fittings supplier or IndiaMART | ₹100–400 | CANDIDATE PRODUCT |

**Subtotal DP instruments:** ~₹12,750–14,550

> Note: If the Testo 510 is available via borrowing from the physics or civil engineering laboratory, substitute BORROW — reduces BUY NOW spend by ~₹11,000.

### 2.3 Airflow measurement

| Item | Specification | Vendor / Source | Estimated India Price | Status |
|---|---|---|---:|---|
| Rotameter A | 0–100 L/min; air; float-type; ±2–3% FS | Shree Aashapura Instrument, Mumbai (IndiaMART) | ₹1,950 | CANDIDATE PRODUCT |
| SS316 needle valve (×1) | 1/4" NPT or 6 mm compression; fine-adjustment; to pair with Rotameter A | IndiaMART (Alfa Valves, Bhosari) | ₹600–1,200 | CANDIDATE PRODUCT |
| Bubble flowmeter or soap-film meter | For single-point calibration check of rotameter at 50 L/min | Physics lab (borrow) or DIY from graduated burette | ₹0 (borrow) or ₹200–400 (DIY) | BORROW preferred |
| Rotameter B | 0–300 L/min; air; for high-velocity stages (U_s ≥ 0.52 m/s) | Deluxe Gases Pune, IndiaMART vendors | REQUIRES QUOTE | BUY LATER — needed only for Stage C / Stage D high-velocity points |

**Subtotal airflow (Phase 16 minimum, Rotameter A only):** ~₹2,550–3,150

### 2.4 Temperature and RH sensor

| Item | Specification | Vendor / Source | Estimated India Price | Status |
|---|---|---|---:|---|
| SHT40 breakout board (×2) | ±0.2°C, ±1.8% RH; I²C; 3.3 V; 2.54 mm header | Robu.in; Evelta Electronics; Amazon.in | ₹300–600 per board | CANDIDATE PRODUCT — buy 2 now (1 for Phase 16; 1 for Phase 17 downstream) |

**Subtotal T/RH:** ~₹600–1,200

### 2.5 Tubing and fittings — flow path

| Item | Specification | Vendor / Source | Estimated India Price | Status |
|---|---|---|---:|---|
| PTFE tubing | 6 mm OD × 4 mm ID; 3 m total | IndiaMART (Sealco, Pune; others) | ~₹85/m → ₹255 for 3 m | CANDIDATE PRODUCT |
| Compression fittings, straight (×4) | 6 mm OD push-in or compression; SS316 or PP; for tube-to-cap connections | SMC India, Festo India, or IndiaMART | ₹80–180 each → ₹320–720 total | CANDIDATE PRODUCT |
| Compression fittings, tee (×2) | 6 mm OD tee; for pressure tap branches to SDP810 and Testo 510 | Same vendors | ₹120–250 each → ₹240–500 total | CANDIDATE PRODUCT |
| Hose clamps (×6) | 10–20 mm range; for any non-compression PTFE to barb connections | Hardware store | ₹5–15 each → ₹90 | CANDIDATE PRODUCT |

**Subtotal tubing and fittings:** ~₹900–1,565

### 2.6 DAQ hardware

| Item | Specification | Vendor / Source | Estimated India Price | Status |
|---|---|---|---:|---|
| Raspberry Pi 4B (2 GB) | Linux SBC; I²C for SDP810 + SHT40; USB for backup; 40-pin GPIO | Robu.in; Evelta; Amazon.in India | ₹5,500–7,000 | CANDIDATE PRODUCT |
| MicroSD card (32 GB) | For RPi OS + data logging | Amazon.in / local electronics | ₹400–600 | CANDIDATE PRODUCT |
| RPi 4B power supply (5 V 3 A USB-C) | Official or certified 3 A supply | Amazon.in / Robu.in | ₹400–600 | CANDIDATE PRODUCT |
| I²C cable and Dupont connectors | For SDP810 and SHT40 connections to GPIO; 4-wire (GND, 3V3, SDA, SCL) | Robu.in; electronics local market | ₹50–150 | CANDIDATE PRODUCT |
| DS3231 RTC module | Battery-backed; I²C; for timestamps if lab has no network | Robu.in; Amazon.in | ₹150–350 | CANDIDATE PRODUCT — buy if no reliable network in lab |

**Subtotal DAQ:** ~₹6,500–8,700

> Note: If a Raspberry Pi 4B is already available in the lab, borrow it — eliminates ~₹6,500 from BUY NOW spend.

### 2.7 Miscellaneous lab supplies

| Item | Specification | Vendor / Source | Estimated India Price | Status |
|---|---|---|---:|---|
| Laboratory weighing balance | 0.01 g resolution; 500 g capacity; for media dry-mass measurement | Borrow from chemistry lab | ₹0 (borrow) | BORROW |
| Digital caliper | 0.01 mm resolution; for measuring settled bed depth | Borrow from mechanical lab | ₹0 (borrow) or ₹500–800 (buy) | BORROW preferred |
| Vernier height gauge or depth micrometer | For confirming screen position and settled bed depth | Borrow | ₹0 (borrow) | BORROW |
| Nitrile gloves (box of 100) | For media handling (GAC dust) | Lab supply | ₹300–600 | CANDIDATE PRODUCT |
| Activated carbon (OVC 4×8 or equivalent) | 500 g sample for pressure-drop tests | Kuraray / Calgon Carbon India or local carbon supplier | REQUIRES QUOTE | REQUIRES QUOTE — initiate contact before ordering any instrument |
| Desiccator or sealed container | For media dry storage before and between runs | Borrow from chemistry lab | ₹0 (borrow) | BORROW |
| Cable ties, mounting brackets | For rig assembly and cable management | Hardware store | ₹100–200 | BUY |

**Subtotal misc:** ~₹400–1,400 (excluding media, assuming borrow of balance/caliper)

---

## 3. BUY LATER — HCHO Breakthrough Test Items

**Do not order these items until Phase 17 institutional safety approval is obtained.**

| Item | Why deferred | Estimated India Price | Notes |
|---|---|---:|---|
| Sensirion SFA30-D-T HCHO sensor (×2 + 1 spare) | No HCHO testing in Phase 16 | ~₹7,099/unit → ₹21,297 total | E Control Devices India; verify stock |
| Certified HCHO gas cylinder (BOC / Linde India) | Hazardous gas; requires institutional approval, cylinder SDS, and storage permit | REQUIRES QUOTE | Do not order without institutional chemical safety written approval |
| Mass Flow Controllers (×2) | For certified gas dilution; imported | REQUIRES QUOTE ($200–600 USD each) | Alicat, Brooks, or Bronkhorst; long lead time |
| Static mixer / mixing tee | For HCHO + air blending | ₹500–2,000 | Fabricate or buy SS316 |
| DNPH cartridge pump (×2) | For ISO 16000-3:2022 reference sampling | REQUIRES QUOTE | SKC, Supelco, or equivalent |
| DNPH cartridges (case of 50) | Consumable for reference analysis | REQUIRES QUOTE (~₹8,000–20,000 estimated) | Get from NABL lab or import |
| SS316 custom column (×1) | For Phase 17+ HCHO breakthrough (acrylic cannot be used) | REQUIRES QUOTE (~₹8,000–25,000) | Quote simultaneously with acrylic column; may be better long-term investment |

---

## 4. OUTSOURCE

| Task | Provider type | Estimated cost | Notes |
|---|---|---:|---|
| HCHO analysis — DNPH/HPLC (ISO 16000-3:2022) | NABL/17025-accredited external laboratory | ₹1,500–5,000 per sample set | Phase 17+ only; confirm lab can handle HCHO DNPH cartridges before ordering cartridges |
| Column machining (end caps) | Local precision workshop | ₹1,000–3,000 | Requires dimensioned drawing; include O-ring groove and port dimensions |
| Acrylic tube supply and cut to length | Local plastics fabricator | ₹500–1,200 | Confirm ID tolerance (75 mm ± 0.5 mm acceptable) |

---

## 5. Budget Tiers

### Tier 1 — Minimum Viable (BUY NOW only; borrow Testo 510 and RPi if possible)

This tier covers Stage A (empty rig) and Stage B (26 mm bed) at U_s = 0.13 and 0.26 m/s only. No high-velocity points, no HCHO.

| Category | Estimated cost |
|---|---:|
| Column (acrylic) + machining + O-rings | ₹3,500 |
| SS316 mesh screens + PTFE gaskets | ₹700 |
| SDP810-500Pa (primary DP sensor) | ₹2,000 |
| Testo 510 (BORROW from lab) | ₹0 |
| Rotameter A (0–100 L/min) | ₹1,950 |
| SS316 needle valve | ₹800 |
| SHT40 breakout ×2 | ₹900 |
| PTFE tubing + fittings | ₹1,200 |
| Raspberry Pi 4B + SD card + PSU (BORROW if available) | ₹0 |
| Misc lab supplies (gloves, cable ties) | ₹500 |
| OVC 4×8 media — 200 g sample | REQUIRES QUOTE |
| **TOTAL (excluding media and RPi if borrowed)** | **~₹11,550** |

> Tier 1 is viable for initial Stage A–B only. Add Rotameter B and Testo 510 (if not borrowed) for full matrix.

### Tier 2 — Recommended (all clean-air instruments; no HCHO)

Covers the full velocity matrix Stages A–D (U_s = 0.13 to 1.05 m/s) for all three bed depths. Includes own Testo 510 and Raspberry Pi.

| Category | Estimated cost |
|---|---:|
| Column (acrylic) + machining + O-rings | ₹3,500 |
| SS316 mesh screens + PTFE gaskets | ₹700 |
| SDP810-500Pa (primary DP sensor) | ₹2,000 |
| Testo 510 (buy own) | ₹11,148 |
| Rotameter A (0–100 L/min) | ₹1,950 |
| Rotameter B (0–300 L/min) | REQUIRES QUOTE (~₹3,000–6,000 estimated) |
| SS316 needle valves ×2 | ₹1,600 |
| SHT40 breakout ×2 | ₹900 |
| PTFE tubing + fittings | ₹1,200 |
| Raspberry Pi 4B + SD card + PSU | ₹6,500 |
| I²C cables, DS3231 RTC, misc electronics | ₹500 |
| Misc lab supplies | ₹500 |
| OVC 4×8 media — 500 g | REQUIRES QUOTE |
| **TOTAL (excluding media and rotameter B quote)** | **~₹30,498** |
| **TOTAL if Rotameter B = ₹4,500** | **~₹34,998** |

### Tier 3 — Reference Grade (highest accuracy; suitable for publication)

Replaces acrylic column with SS316 or borosilicate glass; uses traceable calibrated DP sensor; adds calibration against reference instrument.

| Category | Estimated cost |
|---|---:|
| SS316 custom column (75 mm ID, 250 mm, flanged) | REQUIRES QUOTE (~₹12,000–25,000) |
| Calibrated Sensirion SDP810 with certificate | ~₹3,000–5,000 (with calibration certificate from supplier) |
| Testo 510 (own) | ₹11,148 |
| All flow / T-RH / DAQ as Tier 2 | ~₹13,000 |
| External rotameter calibration (3 points, certified lab) | ₹2,000–5,000 |
| OVC 4×8 media — 1 kg | REQUIRES QUOTE |
| **TOTAL (excluding media, SS316 column at ₹18,000 estimate)** | **~₹54,000–65,000** |

---

## 6. Critical Procurement Blockers

These must be resolved before the first experiment regardless of budget tier:

1. **OVC 4×8 India availability and lot confirmation.** Contact Kuraray India (formerly Calgon Carbon India) or their distributor. Obtain: SDS, lot number, lot bulk density, particle size analysis, minimum order quantity. No procurement makes sense if the media cannot be sourced.

2. **Column machining lead time.** Identify a local machine workshop that can fabricate acrylic end caps to the Phase 16 drawing. Confirm: ID tolerance ±0.5 mm, port thread type (1/4" NPT or M10), O-ring groove dimensions. Lead time can be 1–3 weeks.

3. **Institutional media handling approval.** Even for non-hazardous activated carbon (OVC 4×8 is inert, non-toxic), the institution may require chemical inventory registration or handling procedure sign-off. Obtain this before first packing.

4. **SDP810-500Pa India stock confirmation.** Confirm Tanotis India or another local supplier has stock. If no India stock, allow 2–4 weeks for international shipping (DigiKey or Arrow ship to India).

5. **Rotameter B quote.** Request three quotes from IndiaMART rotameter suppliers for 0–300 L/min range. This determines whether Stage C and D high-velocity points are feasible within budget.

---

## 7. Build Order (15 Steps)

Steps 1–7 are pre-build (procurement, fabrication, software). Steps 8–11 are rig assembly. Steps 12–15 are qualification before first run. Do not advance to the next step until the current step passes its check.

### Step 1 — Media procurement
Contact Kuraray / Calgon Carbon India or a distributor. Request: SDS, lot certificate, bulk density, particle size analysis, minimum order quantity, delivery lead time. Target: 200–500 g for Phase 16 pressure-drop tests.

**Check:** Media lot certificate and SDS in hand.

### Step 2 — Column fabrication
Order acrylic tube (75 mm ID × 300 mm length) from local plastics supplier. Commission machining of two acrylic end caps per drawing (bore 75 mm; two 6 mm compression ports per cap; one O-ring groove per cap). Order Viton O-rings (70 mm ID × 5 mm).

**Check:** Tube ID measured with calipers = 75 ± 0.5 mm; end caps fit without gap; O-rings seat without extrusion.

### Step 3 — Mesh screen preparation
Obtain SS316 woven wire mesh sheet (≤ 2 mm opening). Cut six 75 mm discs using a sharp die-cutter or precision scissors (circle template from acrylic end cap bore). Deburr edges. Label each disc 1–6.

**Check:** Each disc sits flat in the column bore without buckling; no sharp edges.

### Step 4 — SDP810-500Pa acquisition
Order from India (Tanotis) or internationally (DigiKey/Arrow). Confirm tube port adapter for connection to PTFE 6 mm tubing.

**Check:** Package received undamaged; I²C address readable from Raspberry Pi (default 0x25); zero reading stable ≤ ±1 Pa in still air.

### Step 5 — Rotameter A calibration check
Obtain Rotameter A (₹1,950, Shree Aashapura Mumbai). Connect to air source. Compare rotameter reading at three set points (~20, 50, 80 L/min) against a bubble/soap-film meter or certified reference. Record correction factor or confirm ≤ ±3% deviation.

**Check:** Calibration record complete; correction factor (if any) entered in data schema header.

### Step 6 — SHT40 and DAQ setup
Set up Raspberry Pi 4B. Connect SHT40 via I²C. Connect SDP810 via I²C. Install Sensirion Python libraries (`pip install sensirion-i2c-sdp`, `pip install sensirion-i2c-sht`). Run the Phase 15 pseudocode logging loop for 5 minutes in free air. Verify CSV output contains all 14 mandatory fields with plausible values.

**Check:** CSV file generated with correct headers and no missing fields; timestamp_utc is NTP-synchronized or RTC-synchronized; SHT40 reads 20–35°C and 30–70% RH; SDP810 reads 0 ± 1 Pa.

### Step 7 — Air supply and needle valve setup
Connect compressed air or laboratory air supply to upstream fitting. Install needle valve between air supply and column inlet for flow adjustment. Connect Rotameter A downstream of the column outlet position.

**Check:** Air supply reaches > 5 kPa at 100 L/min without pressure cycling; needle valve gives stable flow at three set points.

### Step 8 — Empty column assembly (Stage A preparation)
Assemble the column with no media: end caps with O-rings on both ends; mesh screen at each end (for empty-rig ΔP measurement consistency). Tighten end cap bolts/clips uniformly. Connect pressure taps to SDP810 and Testo 510 (if available) via PTFE tubing tees.

**Check:** Visual inspection — no gaps between end cap and tube; O-ring seated; pressure tube connections leak-free (bubble test: apply soapy water to all joints at 200 Pa supply, ≤ 5 bubbles/min).

### Step 9 — Zero check (pressure sensors)
With both pressure taps open to atmosphere (no flow, both tap tubes disconnected from column), read SDP810 and Testo 510. Both must read 0 ± 1 Pa.

**Check:** Zero within ±1 Pa. If not: re-zero the SDP810 per Sensirion datasheet; re-zero Testo 510 per manual. Repeat. Do not proceed until zero is confirmed.

### Step 10 — Empty-rig Stage A runs
Run Stage A: empty column, no media. Measure ΔP at each velocity point (0.13, 0.26, 0.52, 0.80, 1.05 m/s = Q = 34.5, 68.9, 137.8, 212, 278 L/min). Log all runs with DAQ. Record fixture ΔP at each flow. Allow 3 minutes of stable flow before recording each point (3-minute stabilization window). Record three independent readings (each at 1 s intervals) per condition; average.

**Check:** ΔP increases monotonically with flow. Both sensors agree within ±3 Pa (or ±5% whichever is larger). Record as `fixture_dp_Pa_at_this_flow` in session header.

### Step 11 — Media packing (Stage B, first replicate)
Dry OVC 4×8 media to constant mass (105°C oven, 2 h). Cool in desiccator. Weigh to 0.01 g. Pack column to settled depth 26 mm (target mass ~51 g for 75 mm column at 450 kg/m³ — confirm with actual bulk density). Tap column 20 times on rubber mat. Measure settled depth with caliper through open upper end before installing upper end cap. Record mass and depth in session header.

**Check:** Settled bed depth = 26 ± 2 mm (within ±8% of target). If short: add media and re-tamp. If over: remove media and re-tamp.

### Step 12 — Stage B first replicate runs
Connect DAQ. Start logger. Run each velocity point in the sequence: 0.13 → 0.26 → 0.52 → 0.80 → 1.05 m/s. Allow 3 minutes stabilization per point before recording. Use stop criteria in the test protocol (Section 7 of PHASE16_CLEAN_AIR_TEST_PROTOCOL.md) to identify early termination conditions.

**Check:** ΔP rises with flow; no saturation of SDP810 at high velocity (if saturated, use Testo 510 readings for those points); data logged continuously.

### Step 13 — Stage B second and third replicates
Disassemble column. Discard used media (do not repack used media). Repeat Steps 11 and 12 with fresh media from the same lot, freshly dried and independently weighed and packed. Three independent packing replicates required.

**Check:** Bed depths within ±2 mm across three replicates; ΔP at each velocity within ±15% coefficient of variation across replicates (Phase 16 QC criterion).

### Step 14 — Stages C and D
Repeat Steps 11–13 for 52 mm and 104 mm bed depths (Stages C and D). For Stage D at U_s ≥ 0.80 m/s: monitor SDP810 actively; if reading > 480 Pa, stop the run and use Testo 510 reading only for that point. Do not run 104 mm at 1.05 m/s until readings at 0.80 m/s are below 480 Pa.

**Check:** All data logged; Darcy–Forchheimer fit residuals ≤ 15% of measured ΔP at each point.

### Step 15 — Data archive and Darcy–Forchheimer fitting
Copy all CSV files to at least two independent backup locations. Run Darcy–Forchheimer regression per Phase 16 test protocol. Report fitted coefficients a and b (Ergun linear and quadratic terms) with 95% confidence intervals. Archive raw CSVs permanently; post-processed CSVs in a clearly labelled subfolder.

**Check:** Fit R² ≥ 0.99 (for ΔP/L vs U_s); if not, investigate outlier runs before archiving.

---

## 8. Procurement Timeline (Indicative)

| Week | Action |
|---|---|
| Week 1 | Contact media supplier (OVC 4×8); request quote and SDS. Contact machine shop for column end caps. Order SDP810 (India or international). Order Rotameter A. |
| Week 2 | Order PTFE tubing, fittings, mesh, O-rings, SHT40 breakout boards. Set up Raspberry Pi and test I²C communication. |
| Week 3 | Receive instruments. Receive machined parts. Assemble column (Step 8). Zero-check sensors (Step 9). |
| Week 4 | Receive media. Dry and weigh. Run Stage A (empty rig) and Stage B (26 mm) first replicate. |
| Week 5–6 | Complete all three replicates for Stage B. Run Stage C. Begin Stage D. |
| Week 7 | Complete Stage D. Archive data. Run Darcy–Forchheimer fit. Prepare Phase 16 report. |

> Weeks are indicative and depend on local supplier lead times, media availability, and machine shop capacity. Adjust as needed.

---

*See also: `docs/PHASE16_INSTRUMENT_SELECTION.md` for instrument specifications, `docs/PHASE16_CLEAN_AIR_TEST_PROTOCOL.md` for the full test procedure, `docs/PHASE15_BOM.md` for Phase 15 procurement context.*
