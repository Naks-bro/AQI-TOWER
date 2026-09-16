# AQI Tower Phase 16 — Instrument Selection

**PHASE 16 — CLEAN-AIR PRESSURE-DROP RIG ONLY**
**STATUS: SPECIFICATION — NO EXPERIMENT PERFORMED, NO CFD RUN**
**Date: 2026-09-06**

---

## 1. Phase 15 Calculation Audit

All Phase 15 numerical results were independently recalculated. Results and audit status follow.

### 1.1 Cross-sectional areas

| Column ID | Phase 15 value | Recalculated (A = π d²/4) | Audit |
|---:|---:|---:|---|
| 50 mm | 19.63 cm² | 19.635 cm² | ✓ CORRECT (rounding) |
| 75 mm | 44.18 cm² | 44.179 cm² | ✓ CORRECT (rounding) |
| 100 mm | 78.54 cm² | 78.540 cm² | ✓ CORRECT |

### 1.2 Wall-effect ratios (d_max = 4.75 mm, OVC 4×8 upper screen)

| Column ID | Phase 15 value | Recalculated | Audit |
|---:|---:|---:|---|
| 50 mm | 10.5 | 10.526 | ✓ CORRECT |
| 75 mm | 15.8 | 15.789 | ✓ CORRECT |
| 100 mm | 21.1 | 21.053 | ✓ CORRECT |

### 1.3 Flow required — 75 mm column (Q = A × U_s × 60,000 mL/min per m³/s)

| U_s (m/s) | Phase 15 value | Recalculated | Audit |
|---:|---:|---:|---|
| 0.13 | 34.5 L/min | 34.459 L/min | ✓ CORRECT |
| 0.26 | 68.9 L/min | 68.919 L/min | ✓ CORRECT |
| 0.52 | 137.8 L/min | 137.837 L/min | ✓ CORRECT |
| 0.80 | **212.2 L/min** | **212.058 L/min** | MINOR ROUNDING — difference 0.14 L/min; not significant; no correction required |
| 1.05 | 278.4 L/min | 278.325 L/min | ✓ CORRECT |

### 1.4 Bed volumes — 75 mm column (V = A × L)

| Bed depth | Phase 15 value | Recalculated | Audit |
|---:|---:|---:|---|
| 26 mm | 114.9 mL | 114.864 mL | ✓ CORRECT |
| 52 mm | 229.7 mL | 229.729 mL | ✓ CORRECT |
| 104 mm | 459.5 mL | 459.458 mL | ✓ CORRECT |

### 1.5 EBCT (L / U_s)

All Phase 15 EBCT values were verified. Every value matches the recalculation. ✓ CORRECT throughout.

### 1.6 Pressure sensor range — FLAG

**Phase 15 specifies 0–500 Pa as the sensor range.**

An independent Ergun-equation estimate (d_p = 3.5 mm, ε = 0.43, air at 25°C, using standard spherical-particle Ergun) gives:

| L (mm) | U_s (m/s) | Ergun estimate ΔP (Pa) |
|---:|---:|---:|
| 26 | 0.52 | ~42 Pa |
| 26 | 0.80 | ~90 Pa |
| 26 | 1.05 | ~147 Pa |
| 52 | 0.52 | ~85 Pa |
| 52 | 0.80 | ~179 Pa |
| 52 | 1.05 | ~293 Pa |
| 104 | 0.52 | ~169 Pa |
| 104 | 0.80 | ~359 Pa |
| **104** | **1.05** | **~586 Pa** |

**ERGUN ESTIMATE ONLY — non-spherical particle correction not applied; actual ΔP may differ.**

At the highest test condition (L = 104 mm, U_s = 1.05 m/s), the Ergun estimate exceeds the Phase 15 sensor range. The Ergun equation using spherical-particle parameters tends to overestimate for non-spherical granular carbons; actual ΔP is likely lower. The manufacturer graph for OVC 4×8 ends at approximately 0.56 m/s so there is no direct upper-bound reference beyond that.

**Phase 15 old range:** 0–500 Pa
**Recommended Phase 16 range:** Primary sensor 0–500 Pa (Sensirion SDP810-500Pa); backup/high-range instrument 0–2000 Pa or 0–10,000 Pa for cross-check. Do not begin the 104 mm × 1.05 m/s condition until measured ΔP at lower velocities confirms the primary sensor is not at risk of overrange.

**Required documentation update:** Phase 15 Section 5.3 should note that a backup wide-range instrument is required in addition to the 0–500 Pa primary. This is flagged, not silently corrected. The underlying 500 Pa primary specification is retained; only the backup requirement is added.

### 1.7 Audit summary

**All calculations in Phase 15 are correct or correct within rounding.** The 0.14 L/min rounding difference at 0.80 m/s has no engineering consequence. The pressure-sensor range concern (Section 1.6) is a new finding not an error — Phase 15 did not have Ergun estimates to compare against, and the 500 Pa specification was documented as a design assumption.

**No Phase 15 values are wrong. No Phase 15 document requires a corrected value. The Phase 16 addition is a backup wide-range DP instrument.**

---

## 2. Column Selection

### 2.1 Requirements

- Internal diameter: 75 mm (Phase 15 selected; Phase 16 confirmed)
- Total usable length: ≥ 200 mm (to accommodate 104 mm bed + screens + inlet/outlet sections + pressure tap clearance)
- Pressure rating: > 2 kPa gauge (rig operates near atmospheric; very modest)
- Removable ends: for media loading and screen installation
- Transparent: desirable for visual channeling detection during clean-air tests
- Material for clean-air phase: glass, SS316, or acrylic acceptable
- Material for HCHO phase later: SS316 or borosilicate glass required (acrylic is excluded from HCHO breakthrough work)

### 2.2 Options evaluated

#### Option A — Borosilicate glass chromatography column (ESAW India / Glassco Labs / JLab Export)

Indian manufacturers include ESAW India (esawindia.com), Glassco Laboratory (glasscolabs.in), and JLab Export (jlabexport.com). Standard catalogue columns range from 20 mm to 60 mm ID with fritted-disc or plain designs; 75 mm ID is a non-standard size that requires a custom order.

Evidence: ESAW India page lists glass columns as manufacturable; Glassco lists plain and fritted columns up to at least 50 mm ID from catalogue. Custom 75 mm requires contacting manufacturer.

Small standard columns (20–50 mm): ₹250–460 observed (IndiaMART, Ambala/Ahmedabad).

75 mm custom glass: **REQUIRES QUOTE** — contact ESAW India and Glassco Labs directly.

**Assessment:** Excellent material compatibility; transparent; chemical resistant; fragile; expensive at custom size. Preferred for Phase 15+ if available at reasonable cost.

#### Option B — Acrylic tube (local plastics supplier)

Acrylic (PMMA) tube with 75 mm or 76 mm ID is available from plastics suppliers in most Indian cities. Custom cut lengths are standard service. End caps can be machined from acrylic sheet.

Known HCHO adsorption limitation: acrylic adsorbs HCHO at ppb levels. For clean-air pressure-drop tests (no HCHO), this is irrelevant. Acceptable for Phase 16 clean-air work only.

Cost estimate: acrylic tube and fittings — **~₹2,000–5,000 total including machining** — CANDIDATE PRODUCT.

**Assessment:** Lowest-cost transparent option. Suitable for Phase 16 clean-air only. Must not be used for HCHO breakthrough testing later without a blank test confirming negligible uptake.

#### Option C — SS316 custom-fabricated column

A local precision engineering workshop can fabricate a SS316 tube with flanged end caps to specification. Most industrial cities in India have fabricators with SS316 capability.

Cost estimate: **₹8,000–25,000** depending on specification and location — REQUIRES QUOTE.

**Assessment:** Best long-term material; not transparent; more expensive; suitable for both clean-air and HCHO phases. Recommended if budget allows and a fabricator is available.

### 2.3 Recommendation

**For Phase 16 (clean-air pressure-drop only): Acrylic column, 75 mm ID, 250 mm length, with machined acrylic end caps.**
- Cost: lowest, procurable quickly
- Limitation: HCHO breakthrough tests require replacement with SS316 or glass

**For later HCHO work: SS316 custom fabrication or borosilicate glass custom-order.**

Both should be quoted simultaneously. If the glass column can be obtained at reasonable cost and lead time, it is the better single investment that covers both phases.

### 2.4 End cap and flange design (applies to all materials)

Each end cap requires:
- One central bore (same ID as column = 75 mm) for flow
- One side port: 6 mm OD PTFE or SS316 tubing compression fitting for pressure tap
- One side port: 6 mm OD fitting for sample port (T-junction with SFA30/DNPH, future HCHO phase)
- O-ring groove: 70 mm ID × 5 mm cross-section Viton or PTFE O-ring for column seal

The pressure tap port must be flush with the inner bore. No protrusions into the flow path.

---

## 3. Differential Pressure Instrument Selection

### 3.1 Primary instrument — Sensirion SDP810-500Pa

| Parameter | Specification |
|---|---|
| Manufacturer | Sensirion AG |
| Model | SDP810-500Pa |
| Range | ±500 Pa differential |
| Interface | I²C |
| Resolution | 1 Pa (12-bit within the ±500 Pa range) |
| Accuracy | ±1.5% of measured value at 25°C (from Sensirion SDP8xx datasheet) |
| Supply | 2.7–5.5 V; compatible with 3.3 V Raspberry Pi I²C |
| Tube connection | Two tubes (inlet and outlet), 1.5 mm ID port |
| India availability | Tanotis India — **CANDIDATE PRODUCT** (listed; price not confirmed); international: DigiKey, Arrow, RS ($15–25 USD) |
| Status | **CANDIDATE PRODUCT** |

**Justification:** The SDP810-500Pa connects directly to the Raspberry Pi I²C bus, integrating into the same logging loop as the T/RH sensor without additional ADC hardware. Its 1 Pa resolution covers the smallest expected ΔP (~2–5 Pa at 26 mm, 0.26 m/s) adequately.

**Limitation:** If ΔP at 104 mm, U_s ≥ 0.80 m/s exceeds 500 Pa in practice, the sensor will saturate. Monitor readings as velocity increases and stop at the 104 mm high-velocity conditions if saturation is approached.

### 3.2 Secondary / check instrument — digital manometer

| Parameter | Specification |
|---|---|
| Purpose | Independent cross-check of SDP810 readings; wider range for high-velocity points |
| Required range | 0–2,000 Pa minimum; 0–10,000 Pa preferred for safety margin |
| Resolution | ≤ 5 Pa |
| Example product | Testo 510 (range 0–100 hPa = 0–10,000 Pa; 1 Pa resolution) |
| India source | testo.com/en-IN; toolbuy.com India (~₹11,148 observed for Testo 510) |
| Status | **CANDIDATE PRODUCT** |

**Justification:** The Testo 510 has a wider range (0–10,000 Pa) than the SDP810 but similar 1 Pa resolution, making it an ideal cross-check for the full velocity matrix including the potentially high-ΔP conditions at 104 mm × 1.05 m/s. It uses rubber pressure tubes that connect to any standard pressure tap fittings.

**Note on Testo 510 range:** 100 hPa = 10,000 Pa. This means the instrument's display resolution of 1 Pa corresponds to 0.01% of full scale. At low ΔP (< 10 Pa), the Testo 510 reads at roughly the same absolute uncertainty as the SDP810. Both instruments should agree within ±3 Pa at all conditions; if they disagree by more, investigate before accepting either reading.

### 3.3 Tertiary — inclined water manometer (fabricated)

An inclined water manometer can be constructed from a glass tube (10 mm bore), a reservoir, and a spirit level. Sensitivity: 1 mm water column = 9.81 Pa. An inclination angle of 5° gives 1 mm resolution ≈ 0.85 Pa — adequate for the low-ΔP region (< 20 Pa).

Cost: negligible; fabricated in-house. Used to verify sensor zeros and spot-check readings at 1–3 velocity points.

### 3.4 Pressure tap to sensor connection

- Pressure tap ports in end caps: 1/8" NPT or 6 mm compression fitting to PTFE or SS316 tubing
- Tube runs from column end caps to sensor: ≤ 500 mm; must be free of trapped water or condensate
- The SDP810 has a 1.5 mm ID inlet port; connect via a PTFE 1.5 mm push-in nipple or a small-bore PTFE tube adapter
- Both pressure tubes (UP and DOWN) must be horizontal or slope upward from the column tap to the sensor to prevent water accumulation

---

## 4. Airflow Measurement Selection

### 4.1 Requirements

- Range: 34–278 L/min for 75 mm column across the full velocity matrix
- Accuracy: ±3% FS or better (adequate for Darcy–Forchheimer fitting)
- Clean dry air only (no HCHO for Phase 16)
- Practical for student operation (readable, adjustable, repeatable)

### 4.2 Rotameter selection (primary flow measurement)

**Two rotameters cover the full velocity matrix:**

| Rotameter | Range | Covers | India source | Price |
|---|---|---|---|---|
| Rotameter A | 0–100 L/min | U_s = 0.13 m/s (34.5 L/min) and U_s = 0.26 m/s (68.9 L/min) | Shree Aashapura Instrument, Mumbai, IndiaMART | ₹1,950 — **CANDIDATE PRODUCT** |
| Rotameter B | 0–300 L/min | U_s = 0.52 m/s (137.8 L/min), 0.80 m/s (212 L/min), 1.05 m/s (278 L/min) | IndiaMART vendors (Deluxe Gases Pune, others) | **REQUIRES QUOTE** |

For Phase 16 initial setup, Rotameter A alone covers the two EBCT-critical baseline conditions (0.13 and 0.26 m/s). Rotameter B can be added when higher-velocity points are ready.

**Each rotameter must be paired with a needle valve (SS316, 1/4" NPT) for fine flow adjustment.**

### 4.3 Density correction

Rotameters are calibrated for a reference gas (typically air) at a reference T and P (commonly 20°C, 1013 mbar). If the lab conditions differ, the actual volumetric flow is:

`Q_actual = Q_rotameter × √(ρ_ref / ρ_actual)`

For dry air at 25°C, 1013 mbar: ρ_actual = 1.184 kg/m³ vs ρ_ref = 1.204 kg/m³ (at 20°C) → correction factor = √(1.204/1.184) = 1.008 — a 0.8% correction, usually negligible.

Record lab T and P at each test. Apply correction if T differs from rotameter calibration by > 5°C or P differs by > 5 kPa.

### 4.4 Flow measurement position

**Place the rotameter downstream of the packed-bed column** (after the lower pressure tap, before the exhaust). This ensures the rotameter sees clean air free of carbon dust or media fines. The superficial velocity is then:

`U_s = (Q_rotameter × correction_factor) / A_column`

where A_column = 44.18 × 10⁻⁴ m² for 75 mm column.

---

## 5. Temperature and RH Sensor Selection

### 5.1 Purpose in Phase 16

For clean-air pressure-drop tests:
- Confirm the test is conducted within the Phase 14 baseline condition (25 ± 2°C, 50 ± 5% RH)
- Log T and RH for density correction and future comparison with HCHO breakthrough tests
- Detect significant temperature changes that would affect air density and rotameter readings

### 5.2 Recommended sensor: Sensirion SHT40 or SHT45

| Parameter | SHT40 | SHT45 |
|---|---|---|
| Temperature accuracy | ±0.2°C (SHT40) | ±0.1°C (SHT45) |
| RH accuracy | ±1.8% RH (SHT40) | ±1.0% RH (SHT45) |
| Interface | I²C | I²C |
| Supply | 1.8–3.6 V | 1.8–3.6 V |
| India availability | Breakout boards from Robu.in, Evelta, Amazon.in | Same |
| Approximate cost | ~₹300–600 for breakout board | ~₹400–800 |
| Status | **CANDIDATE PRODUCT** |

**Justification:** SHT40/SHT45 are calibrated factory-traceable sensors sharing the same I²C bus as the SDP810 and Raspberry Pi. No additional ADC is needed. The SHT40 accuracy (±0.2°C, ±1.8% RH) is adequate for monitoring baseline conditions. The SHT45 is a worthwhile upgrade for stress-condition testing later.

### 5.3 Placement

One SHT40/SHT45 at the column inlet (upstream) is sufficient for Phase 16 pressure-drop tests. For Phase 15+ HCHO tests, two sensors (upstream + downstream) are required. Buy two sensors now; use one for Phase 16.

---

## 6. Tubing and Fittings Selection

### 6.1 Main flow path (from compressor to column inlet and column outlet to exhaust)

For clean-air phase (Phase 16), any non-contaminating material is acceptable:
- **PTFE 6 mm OD × 4 mm ID**: confirmed available in India at ~₹85/m — **CANDIDATE PRODUCT**
- 3–5 m of PTFE tubing covers all connection runs
- Use SS316 compression-fit Swagelok or Parker A-Lok type fittings for leak-free connections

### 6.2 Pressure tap lines (from column taps to DP sensor)

- **PTFE 3 mm OD × 1.5 mm ID or similar small-bore**: matches SDP810 inlet port size
- Keep runs short (< 500 mm) and route to prevent condensate accumulation
- India supplier: standard PTFE small-bore tubing available from plastics distributors

### 6.3 Compression fittings

- **Swagelok India** has offices in Mumbai, Pune, and other metros — **CANDIDATE PRODUCT** for high-quality leak-free fittings
- Alternate: Parker A-Lok fittings from industrial distributors — **CANDIDATE PRODUCT**
- Estimated cost: ₹200–600 per fitting; budget 10–15 fittings for the rig

### 6.4 Ball valves

- SS316 mini ball valve, 6 mm or 1/4" NPT, for flow isolation: ₹300–600 each from IndiaMART industrial valve suppliers — **CANDIDATE PRODUCT**
- Two required: one at column inlet (shutoff during packing) and one at exhaust

### 6.5 Avoidance list

The following materials are excluded from any portion of the rig that will later be used for HCHO breakthrough tests:
- PVC tubing or fittings
- Natural rubber
- Silicone tubing (significant HCHO adsorption)
- Untreated acrylic fittings
- Neoprene gaskets

Using PTFE and SS316 throughout from Phase 16 avoids re-plumbing before Phase 17+ HCHO tests.

---

## 7. Media Retaining Screens

### 7.1 Requirements

- Opening: ≤ 2.0 mm (smaller than OVC 4×8 d_min = 2.36 mm, retains all media particles)
- Diameter: 75 mm OD to match column bore
- Material: SS316 woven wire mesh (or SS304 as acceptable substitute for clean-air phase)
- Rigidity: must not deflect under ΔP or media weight at the 104 mm bed loading

### 7.2 India sourcing

SS316 woven wire mesh is widely available in India:
- Sheet price: ~₹16–75/sq ft (IndiaMART — multiple suppliers confirmed)
- Cut 75 mm diameter discs from sheet: can be done at a local metal workshop or DIY with a hole saw
- Disc wire mesh filter suppliers also exist on IndiaMART — order 10–20 discs of 75 mm diameter, ≤ 2 mm opening, SS316

Estimated cost: ₹500–2,000 for mesh material + cutting of 10 discs — **CANDIDATE PRODUCT**.

### 7.3 Media distributor plate

A perforated SS316 disc (75 mm diameter, 1–2 mm thickness, ≥ 30% open area with ≤ 2 mm holes) acts as the inlet distributor. This can be:
- Fabricated from SS316 perforated sheet (available from metal suppliers) at a local workshop
- Combined with a woven mesh layer for finer distribution

Estimated cost: ₹500–1,500 fabricated — **GENERIC REQUIREMENT**.

---

## 8. Clean-Air Rig Flow Schematic

The following describes the exact flow path and instrument placement for Phase 16 pressure-drop testing.

```
[Oil-free air supply / compressor]
         │
         ▼
[Moisture trap + particulate filter]    ← protect column and instruments
         │
         ▼
[Needle valve A]                         ← coarse flow adjustment
         │
         ▼
[Rotameter A (0–100 L/min)]             ← primary flow reading
         │                               (or Rotameter B 0–300 L/min for high-velocity)
         ▼
[Straight inlet section, ≥75 mm]        ← flow development length
         │
         ▼
┌────────────────────────────────────┐
│         COLUMN BODY                │
│                                    │
│  [Column inlet fitting]            │
│  ├── [Pressure tap UP] ──────────────────────┐
│  ▼                                │          │
│  [Distributor plate]               │          │
│  [Upper retaining screen]          │          │  SDP810-500Pa
│  [GAC bed (or empty)]              │          │  (reads UP−DOWN)
│  [Lower retaining screen]          │          │
│  ├── [Pressure tap DOWN] ──────────────────────┘
│  ▼                                │
│  [Column outlet fitting]           │
└────────────────────────────────────┘
         │
         ▼
[SHT40 T/RH sensor]                  ← temperature and RH measurement
         │
         ▼
[Needle valve B]                      ← optional fine adjustment
         │
         ▼
[Exhaust to atmosphere or lab hood]
```

**Instrument placement rules:**
- Pressure taps UP and DOWN: in the column wall, flush with bore, at bed inlet and outlet faces
- Rotameter: downstream of column (clean side, no dust)
- T/RH sensor: downstream of column, in the outlet flow
- SDP810: mounted separately, connected to UP and DOWN taps via PTFE small-bore tubes
- Testo 510 check manometer: connected to the same taps via a T-junction or separate ports when cross-checking

**Note on column orientation:** The column should be vertical (upright) with airflow from bottom to top, to match the downward gravity settling of media and to prevent media from lifting out of the column. This also makes media loading easier.

---

## 9. Data Acquisition — Phase 16 Supplement

For the clean-air pressure-drop tests, the Phase 15 DAQ schema can be simplified. The following fields are **mandatory** for Phase 16 runs; HCHO-related fields may be present but will be zero/null.

**Minimum fields for Phase 16:**

| Field | Unit | Source |
|---|---|---|
| `timestamp_utc` | ISO 8601 | Raspberry Pi RTC |
| `run_id` | String | Operator |
| `stage` | String ("EMPTY"/"26mm"/"52mm"/"104mm") | Operator |
| `media_lot` | String | Operator |
| `media_name` | String ("OVC4x8" or "EMPTY") | Operator |
| `bed_depth_mm` | mm | Operator (measured) |
| `media_mass_g` | g | Operator (weighed) |
| `replicate` | Integer (1/2/3) | Operator |
| `flow_lpm` | L/min | Rotameter reading (operator log at each step) |
| `superficial_velocity_ms` | m/s | Derived: `flow_lpm / (60 × A_m2 × 1000)` |
| `temperature_C` | °C | SHT40 |
| `RH_pct` | % | SHT40 |
| `dp_total_Pa` | Pa | SDP810 (packed column or empty column) |
| `dp_empty_Pa` | Pa | From the Stage A (empty column) run at same flow |
| `dp_bed_Pa` | Pa | Derived post-processing: `dp_total_Pa − dp_empty_Pa` |
| `operator` | String | Operator |
| `notes` | String | Free text |

**Note:** `dp_empty_Pa` is entered into the post-processing dataset from the Stage A measurements; it is not logged in real time during packed-bed runs (the empty column has already been measured).

---

## 10. Acceptance Criteria Summary

| Item | Selection | Status |
|---|---|---|
| Column body | Acrylic 75 mm ID (Phase 16) / SS316 or glass (Phase 17+) | **READY — quote required** |
| DP sensor primary | Sensirion SDP810-500Pa (I²C, ±500 Pa) | **CANDIDATE PRODUCT** |
| DP sensor backup | Testo 510 digital manometer (0–10,000 Pa) | **CANDIDATE PRODUCT, ₹11,148 observed** |
| DP inclined manometer | Fabricated in-house (glass tube + water) | **CAN FABRICATE** |
| Flow meter (low range) | Rotameter 0–100 L/min | **CANDIDATE PRODUCT, ~₹1,950** |
| Flow meter (high range) | Rotameter 0–300 L/min | **REQUIRES QUOTE** |
| T/RH sensor | Sensirion SHT40 breakout board (I²C) | **CANDIDATE PRODUCT, ~₹300–600** |
| Tubing (main) | PTFE 6 mm OD × 4 mm ID | **CANDIDATE PRODUCT, ~₹85/m** |
| Tubing (pressure taps) | PTFE 3 mm OD small-bore | **CANDIDATE PRODUCT** |
| Fittings | SS316 compression (Swagelok / Parker A-Lok) | **CANDIDATE PRODUCT, REQUIRES QUOTE** |
| Ball valves | SS316 mini ball valve | **CANDIDATE PRODUCT, ~₹300–600 each** |
| Media retaining screens | SS316 woven wire mesh, ≤2 mm opening, 75 mm discs | **CANDIDATE PRODUCT, ~₹500–2,000 for set** |
| Distributor plate | SS316 perforated disc, ≥30% open area | **GENERIC REQUIREMENT / CAN FABRICATE** |
| Media (OVC 4×8) | Kuraray/Calgon Carbon India — lot certificate required | **REQUIRES QUOTE** |
| Digital scale | ±0.1 g resolution, ≥500 g capacity | **GENERIC REQUIREMENT** |

---

*Sources: Sensirion SDP810 datasheet (sensirion.com/products/catalog/SDP810-500Pa); Testo 510 India listing (toolbuy.com, ~₹11,148); rotameter India listing (IndiaMART, Shree Aashapura, ₹1,950); SS316 mesh India pricing (IndiaMART ₹16–75/sq ft); PTFE tubing India (~₹85/m, tradeindia.com); borosilicate columns (ESAW India, Glassco Labs).*
