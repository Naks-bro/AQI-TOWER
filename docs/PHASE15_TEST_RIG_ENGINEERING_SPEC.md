# AQI Tower Phase 15 — Test-Rig Engineering Specification

**PHASE 15 — ENGINEERING PREPARATION ONLY**
**STATUS: SPECIFICATION DOCUMENT — NO EXPERIMENT PERFORMED, NO CFD RUN**
**Date: 2026-09-06**
**Supersedes: nothing. Supplements Phase 14 frozen requirements.**

All evidence labels follow the Phase 14 convention:
- **PROPOSED PROJECT TARGET** — selected requirement, must be verified experimentally
- **ENGINEERING ASSUMPTION** — provisional; must be checked before use
- **VERIFIED PRODUCT** — product confirmed to exist with cited evidence
- **CANDIDATE PRODUCT** — product believed to be available; procurement not confirmed
- **GENERIC REQUIREMENT** — functional need; specific product not yet selected
- **REQUIRES QUOTE** — specification clear but price/availability not confirmed
- **UNKNOWN** — requires investigation before deciding

---

## 1. Scope and Purpose

Phase 15 converts the Phase 14 experimental requirements into a buildable, procurement-ready engineering system.

**Phase 15 does NOT:**
- Run CFD
- Invent adsorption coefficients, breakthrough times, removal efficiencies, or bed-life estimates
- Select a final tower carbon-bed geometry
- Claim CADR
- Produce or use formaldehyde
- Claim that OVC 4×8 or FORMASORB is suitable for the AQI Tower

**Phase 15 DOES:**
- Define the exact packed-bed column architecture for the controlled bench test
- Select a column diameter with documented justification
- Tabulate required flows, EBCTs, and bed volumes for all Phase 14 matrix conditions
- Specify pressure, flow, HCHO, T/RH, and analytical measurement architectures
- Define the DNPH–HPLC reference workflow
- Verify the current SFA30 documentation
- Define HCHO generation system requirements (not a specific commercial device)
- Document media containment, sealing, and blank/zero-air procedures
- Produce a procurement table with availability classification for all items
- Provide three cost tiers (minimum viable / recommended / reference-grade)
- Define a synchronized data schema

---

## 2. Rig Architecture Overview

### 2.1 Conceptual flow path

```
[Zero/clean air supply]
        |
        v
[Humidity conditioner]  ← RH control branch
        |
        v
[HCHO generation / injection point]   (institutional laboratory only; Section 8)
        |
        v
[Static mixer / conditioning length]
        |
        v
[Upstream T/RH sensor + SFA30 #1]    ← upstream sample port
        |
        v
[DNPH upstream cartridge port]
        |
        v
[Packed-bed test column]
  - inlet distributor
  - upstream pressure tap
  - media retaining mesh
  - granular GAC bed (OVC 4×8 or FORMASORB)
  - downstream retaining mesh + support
  - downstream pressure tap
        |
        v
[Downstream T/RH sensor + SFA30 #2]  ← downstream sample port
        |
        v
[DNPH downstream cartridge port]
        |
        v
[Flow measurement device]
        |
        v
[Fan / flow controller]
        |
        v
[HCHO exhaust capture / scrubber → facility exhaust]
```

### 2.2 Zero-air / blank path

A bypass valve before the HCHO injection point routes clean air through the entire downstream rig without challenge. This path is used for:
- System leak checks
- Transport-delay measurement
- Instrument co-location and zero verification
- Blank DNPH cartridge collection

No HCHO is introduced during blank tests.

### 2.3 Rig material constraints

All wetted surfaces downstream of the HCHO injection point must have documented HCHO compatibility and low HCHO adsorption. Preferred materials:
- **Tubing:** PTFE or stainless steel 316 — **GENERIC REQUIREMENT**
- **Fittings:** stainless steel or PTFE-lined — **GENERIC REQUIREMENT**
- **Column body:** stainless steel 316 or borosilicate glass — **GENERIC REQUIREMENT**
- **Seals/gaskets:** PTFE or Viton — **GENERIC REQUIREMENT**
- **Avoid:** PVC, natural rubber, silicone tubing, untreated acrylic — each can adsorb or off-gas HCHO significantly at ppb levels

---

## 3. Packed-Bed Column Geometry Analysis

### 3.1 Wall-effect criterion

The wall-effect criterion for packed beds requires the column internal diameter to be at least 10× the maximum particle diameter of the media.

For OVC 4×8 US mesh:
- 4 mesh = 4.75 mm screen; 8 mesh = 2.36 mm screen
- `d_max = 4.75 mm` (as defined by the 4-mesh upper screen) — **MANUFACTURER SPECIFICATION**
- Minimum ID = 10 × 4.75 mm = **47.5 mm** — **DERIVED ENGINEERING ASSUMPTION**

Actual particle-size distribution may differ from the mesh nominal; measure the as-received lot before testing.

### 3.2 Column comparison table

All values are **DERIVED** from the Phase 14 velocity matrix and column geometry.

#### Area and wall-effect ratio

| Column ID | Cross-section area | ID / d_max (d_max = 4.75 mm) | Wall-effect criterion |
|---:|---:|---:|---|
| 50 mm | 19.63 cm² | **10.5** | Marginal — just meets ≥10× rule |
| 75 mm | 44.18 cm² | **15.8** | Good — recommended minimum |
| 100 mm | 78.54 cm² | **21.1** | Excellent — larger flows required |

#### Flow required (L/min) — Q = A × U_s

| Superficial velocity U_s | 50 mm ID | 75 mm ID | 100 mm ID |
|---:|---:|---:|---:|
| 0.13 m/s | 15.3 L/min | 34.5 L/min | 61.3 L/min |
| 0.26 m/s | 30.6 L/min | 68.9 L/min | 122.5 L/min |
| 0.52 m/s | 61.3 L/min | 137.8 L/min | 245.0 L/min |
| 0.80 m/s | 94.3 L/min | 212.2 L/min | 376.9 L/min |
| 1.05 m/s | 123.7 L/min | 278.4 L/min | 494.8 L/min |

**Derivation:** Q (L/min) = A (m²) × U_s (m/s) × 1000 × 60

#### Bed volumes (mL) — V_bed = A × L

| Bed depth L | 50 mm ID | 75 mm ID | 100 mm ID |
|---:|---:|---:|---:|
| 26 mm | 51.0 mL | 114.9 mL | 204.2 mL |
| 52 mm | 102.1 mL | 229.7 mL | 408.4 mL |
| 104 mm | 204.1 mL | 459.5 mL | 816.8 mL |

#### EBCT matrix — EBCT = L / U_s (seconds)

| | U_s = 0.13 m/s | U_s = 0.26 m/s | U_s = 0.52 m/s | U_s = 0.80 m/s | U_s = 1.05 m/s |
|---:|---:|---:|---:|---:|---:|
| L = 26 mm | **0.200 s** | **0.100 s** (baseline) | **0.050 s** | 0.033 s | 0.025 s |
| L = 52 mm | 0.400 s | **0.200 s** | **0.100 s** | 0.065 s | 0.050 s |
| L = 104 mm | 0.800 s | 0.400 s | **0.200 s** | 0.130 s | 0.099 s |

Bold values are the Phase 14 proposed EBCT levels (0.05, 0.10, 0.20 s) and their depth/velocity combinations. EBCT does not depend on column diameter.

### 3.3 Column diameter selection and justification

#### 50 mm ID assessment

**Advantages:** lowest flows (15–124 L/min), smallest media mass, lowest HCHO consumption per run.
**Disadvantages:** wall-effect ratio = 10.5 is the minimum boundary; any particle batch with a slightly coarser tail will violate it. At 0.52 m/s the flow (61 L/min) is still modest.
**Decision:** acceptable as a minimum viable size if the exact lot is screened and the d_max is confirmed ≤ 4.75 mm.

#### 75 mm ID assessment — **RECOMMENDED**

**Advantages:** wall-effect ratio = 15.8 provides a comfortable margin over the ≥10× criterion. Baseline condition (0.26 m/s) requires 68.9 L/min — achievable with a 0–100 L/min rotameter and a suitable fan or lab air supply. All five velocity points fall within 0–280 L/min, manageable with available Indian lab equipment. Bed volume (115–460 mL) gives sensible media masses for a student experiment.
**Disadvantages:** higher flows than 50 mm, more HCHO required per unit time.
**Decision:** **75 mm ID is the recommended primary column diameter** — **PROPOSED PROJECT TARGET**.

#### 100 mm ID assessment

**Advantages:** excellent wall-effect margin, larger bed volume reduces screen-to-media ratio concerns.
**Disadvantages:** baseline flow = 122.5 L/min, high-velocity points reach 500 L/min — requires a large lab fan and high-capacity MFC or blower. More expensive column hardware. Higher HCHO consumption per run.
**Decision:** not recommended for initial student-scale work; revisit if a later phase needs larger throughput or better flow uniformity.

### 3.4 Media mass estimates (75 mm ID column)

No bulk density is confirmed for the OVC 4×8 lot yet. The following uses a placeholder bulk density of **450–550 kg/m³** (dense-packed GAC, typical literature range) as an **ENGINEERING ASSUMPTION** until the actual lot is weighed.

| Bed depth | Bed volume | Estimated dry media mass (at 450 kg/m³) | At 550 kg/m³ |
|---:|---:|---:|---:|
| 26 mm | 114.9 mL | ~52 g | ~63 g |
| 52 mm | 229.7 mL | ~103 g | ~126 g |
| 104 mm | 459.5 mL | ~207 g | ~253 g |

Measure actual bulk density from the received lot: fill a graduated cylinder with a known dry mass and read settled volume. Record loose and settled density separately.

---

## 4. Media Containment Design

### 4.1 Column body

- **Material:** stainless steel 316 tube with flanged end caps, or borosilicate glass chromatography column body with PTFE end fittings — **GENERIC REQUIREMENT**
- **Internal diameter:** 75 mm (as selected above)
- **Total column length:** ≥ 200 mm to accommodate 104 mm max bed plus support screens, settling length, and pressure-tap spacing
- **Pressure rating:** the rig operates near atmospheric; 1 bar gauge is adequate
- **Transparency is desirable** but not required for pressure-drop tests; it allows visual detection of channeling, media movement, or flooding. If a glass column is used, verify chemical compatibility with HCHO and the carrier air.
- Flanges must allow interchangeable end caps for different screen/distributor configurations

### 4.2 Inlet distributor

- **Purpose:** produce a uniform velocity profile across the full column cross-section before the media bed
- **Type:** sintered metal disc (SS316), perforated plate (≥ 30% open area), or woven wire mesh (300–500 µm opening) — **GENERIC REQUIREMENT**
- **Location:** at the inlet face of the column, upstream of the media
- A straight entry length of ≥ 1× column diameter (≥ 75 mm) between the inlet fitting and the distributor is recommended

### 4.3 Media retaining screens

- **Upper screen (inlet side of bed):** retains media in place; must not obstruct flow significantly
  - Opening: ≤ d_min = 2.36 mm for OVC 4×8; use ≤ 2.0 mm opening to be safe
  - Material: SS316 woven wire — **GENERIC REQUIREMENT**
- **Lower screen (outlet side):** same specification; also catches fines
- Additional filter paper (Whatman Grade 1 or equivalent, SS316 disc holder) between screen and end cap catches dust if media has significant fines
- Screens must be documented as low-HCHO-adsorption materials

### 4.4 Pressure tap locations

- **Upper tap (UP):** in the column wall at the inlet face of the media (above upper screen, below distributor)
- **Lower tap (DOWN):** in the column wall at the outlet face of the media (above lower screen)
- Tap geometry: 1–2 mm diameter drilled port, flush with inner column wall (no burr), connecting to 1/8" SS or PTFE tubing leading to the differential pressure sensor
- Tap-to-tap distance = settled bed depth L (measure after each packing); record this as the effective `L` for the ΔP/L calculation

### 4.5 Sample ports

- **Upstream gas sample:** Swagelok-type or PTFE-sleeved bulkhead fitting, 6 mm OD, immediately upstream of the media bed (before upper screen) — connects to upstream SFA30 and DNPH port via a T-junction
- **Downstream gas sample:** same fitting, immediately downstream of lower screen — connects to downstream SFA30 and DNPH port

DNPH and SFA30 must draw from the same port without interfering with the main flow. A T-piece with the DNPH pump pulling side-stream at << 5% of total flow is acceptable; verify that the side-draw does not reduce main column flow below the target U_s by more than ±2%.

### 4.6 Sealing strategy

- All flanged joints: PTFE spiral-wound gaskets or flat PTFE sheet gaskets — **GENERIC REQUIREMENT**
- Column end caps: O-ring sealed, Viton or PTFE — **GENERIC REQUIREMENT**
- Tubing connections: compression-fit Swagelok or equivalent (SS316) or PTFE push-fit
- Perform a mandatory **blank leak test** before every HCHO campaign: pressurize the sealed column + rig to ~ 1 kPa above atmospheric with clean air, then monitor for pressure decay or use a portable HCHO monitor around all joints

### 4.7 Media filling and settling procedure (to be developed before first test)

1. Dry media to constant mass at 110°C; cool to room temperature in a desiccator.
2. Tare the column assembly (without media).
3. Pour media slowly into the upright column through a funnel; record poured height.
4. Tap the column 10× with a rubber mallet on the side; record settled depth.
5. Level the surface gently; install upper screen and end cap.
6. Weigh the assembled column; record net dry media mass.
7. Calculate settled bulk density: mass / (A × settled depth).
8. Photo-document before sealing.
9. Replicate this procedure independently for each of the three required packing replicates.

---

## 5. Pressure Measurement Architecture

### 5.1 Purpose

Measure `ΔP` versus superficial velocity versus bed depth for each media and packing replicate, to provide the future Darcy–Forchheimer fitting data. The coefficients themselves are **NOT calculated in Phase 15** — they must come from measurements.

### 5.2 Required measurement

- **Differential pressure:** measured between the upstream and downstream pressure taps (across the packed bed only — not across the distributor)
- **Empty-column correction:** the empty column with screens installed but no media must be measured at every velocity point; this fixture ΔP is subtracted from the packed-bed measurement
- **Velocity range:** 0.13, 0.26, 0.52, 0.80, 1.05 m/s — as defined by Phase 14

### 5.3 Pressure sensor specification

| Parameter | Requirement | Justification |
|---|---|---|
| Range | 0 to 500 Pa differential | Covers all bed depths and velocities including extrapolated 1.05 m/s at 104 mm; leaves margin for unexpected high-resistance packing |
| Resolution | ≤ 1 Pa | Required to resolve ΔP at low velocity/short bed (estimated 2–5 Pa at 0.26 m/s, 26 mm bed) |
| Accuracy | ≤ 2% FS (≤ 10 Pa full-scale error) | Adequate for Darcy–Forchheimer fitting; confirm against a reference water manometer |
| Operating temperature | 15–40°C | Covers laboratory range |
| Output | Analog 4–20 mA or digital (I²C / SPI) | Compatible with chosen DAQ system |
| Wetted parts | SS316 or PTFE | HCHO compatibility required if on the HCHO side of the rig |
| Status | **GENERIC REQUIREMENT** — no specific product selected |

**India procurement note:** Sensirion SDP510 (+500 Pa range, I²C, compact) or SDP600-500Pa are **CANDIDATE PRODUCTS** available through RS Components India — verify current India stock and price. Industrial differential pressure transmitters (e.g., Dwyer 616, Honeywell HSC series) are available through IndiaMART distributors at **REQUIRES QUOTE**.

### 5.4 Tap geometry and tubing

- Pressure tap tubes: 3–6 mm OD SS or PTFE, ≤ 500 mm length from tap to sensor
- Tubes must be dry and free of condensate before each test; tilt column slightly if liquid could accumulate in taps
- Purge tap lines with clean dry air and zero the sensor before each velocity point

### 5.5 Measurement procedure

1. **Zero check:** with no flow, record DP reading; it must be within ±1 Pa of zero after zeroing.
2. **Empty-column baseline:** insert screens only (no media), run each velocity point in increasing order, wait for steady state (≥ 30 s), record 10 readings, take mean.
3. **Packed column:** install media, repeat at each velocity point.
4. **Hysteresis check:** repeat one velocity point after decreasing flow.
5. **Fixture-corrected ΔP** = packed-column ΔP − empty-column ΔP at the same velocity.
6. **Replicates:** three independently repacked beds per material per depth.
7. Record air temperature and ambient pressure at each point for density correction if needed.

### 5.6 Independent verification

Cross-check the sensor reading at ≥ 2 points against a calibrated inclined water manometer or electronic reference calibrator. If the deviation exceeds 5 Pa at any check point, recalibrate the sensor before continuing.

---

## 6. Airflow Measurement Architecture

### 6.1 Distinction from tower airflow

- **Tower operating flow (Phase 10B):** Q ≈ 1332 m³/h through the full GEO_C tower — this is a CFD result, not a bench measurement
- **HEPA face velocity:** 1.053 m/s across the 0.3516 m² filter face — also a CFD-derived value
- **Bench superficial velocity:** the velocity at the 75 mm ID column cross-section during the experiment — the quantity controlled and reported in Phase 15

These are different quantities in different systems. Never substitute one for another.

### 6.2 Bench airflow measurement method

For pressure-drop tests (clean air, no HCHO):

| Method | Range | Suitability |
|---|---|---|
| Calibrated rotameter (acrylic, 0–100 L/min) | 0–100 L/min | Covers U_s = 0.13–0.26 m/s for 75 mm column; **CANDIDATE PRODUCT** ~₹1,950 (IndiaMART) |
| Calibrated rotameter (0–300 L/min) | 0–300 L/min | Covers U_s up to 0.52–0.80 m/s for 75 mm column; **CANDIDATE PRODUCT** — REQUIRES QUOTE |
| Thermal mass flow meter | 0–300 L/min | Higher accuracy; suitable for breakthrough tests too; **REQUIRES QUOTE** |
| Needle valve + pressure differential across orifice plate | Custom range | Can be accurate but requires calibration; **GENERIC REQUIREMENT** |

For breakthrough tests (HCHO challenge present), the flow measurement device must be placed **downstream of the scrubber** where no HCHO remains, or use a thermal mass flow element that is chemically inert to HCHO and is placed upstream before the HCHO injection point.

### 6.3 Flow control

- **Needle valve + rotameter** combination is the minimum viable control approach for pressure-drop tests
- **MFC (thermal mass flow controller)** is required if breakthrough runs demand constant flow over hours; a 0–100 L/min MFC for zero air and a smaller 0–5 L/min MFC for the HCHO standard gas stream are appropriate for the 75 mm baseline condition — **REQUIRES QUOTE** (India MFC suppliers: Alicat, Bronkhorst, Sierra — none confirmed at current India price)
- Report the **actual measured flow** at each data point, not only the setpoint

### 6.4 Superficial velocity calculation

`U_s (m/s) = Q (m³/s) / A_column (m²)`

For 75 mm ID column: A = 44.18 × 10⁻⁴ m²

| Target U_s | Target Q (75 mm) | Rotameter setting |
|---:|---:|---|
| 0.13 m/s | 34.5 L/min | Set with needle valve; read rotameter |
| 0.26 m/s | 68.9 L/min | Same |
| 0.52 m/s | 137.8 L/min | Requires 0–150 or 0–300 L/min instrument |
| 0.80 m/s | 212.2 L/min | Requires 0–300 L/min instrument |
| 1.05 m/s | 278.4 L/min | Requires 0–300 L/min instrument |

Note: rotameter readings depend on gas density; correct for temperature and pressure if the reading medium differs from the calibration condition.

---

## 7. HCHO Generation System Requirements

### 7.1 Safety preface

Formaldehyde is an IARC Group 1 human carcinogen and a respiratory sensitizer. Intentional HCHO generation is prohibited in any space that is not:

1. An institutionally managed chemical laboratory
2. Equipped with a suitable fume hood or exhausted enclosure certified for the concentration and quantity used
3. Approved in writing by the responsible institutional safety authority
4. Staffed by trained personnel with current HCHO training
5. Equipped with an independent calibrated area HCHO alarm monitor

The rig described in this document defines what system specification to request from an approved institutional laboratory. It does not authorize student construction or operation of a generation system outside institutional controls.

### 7.2 Explicitly prohibited generation methods

Exactly as stated in Phase 14:

- Open hotplate with formalin solution
- Heated paraformaldehyde in open container
- Polymer off-gassing (POM, MDF, pressed-wood)
- Room dosing or occupied-space generation
- Uncontrolled cylinder discharge without calibrated dilution
- Any method without downstream HCHO destruction/capture

### 7.3 Acceptable generation architectures

**Architecture A — Certified gas cylinder with dynamic dilution (recommended for student lab)**

Use a traceable HCHO calibration gas cylinder (e.g., 5 ppm HCHO in N₂ or air at ±2% uncertainty, NIST-traceable). Dilute with calibrated clean/zero air to the required challenge concentration.

Example dilution calculation for 75 mm baseline condition (100 µg/m³ challenge, 68.9 L/min total):

- 100 µg/m³ = 81.3 ppb at 25°C, 1 atm
- If standard gas is 5 ppm (5000 ppb): dilution ratio = 5000/81.3 = 61.5
- Standard gas flow = total flow / 61.5 = 68.9/61.5 = 1.12 L/min
- Zero air flow = 68.9 − 1.12 = 67.8 L/min

These flows are controllable with two calibrated MFCs. The mixture enters a static mixer before the test column inlet.

**Status of standard gas cylinder:** REQUIRES QUOTE — contact BOC India, Linde India, or National Chemical Laboratory Pune for 5–50 ppm HCHO/N₂ certified gas.

**Architecture B — Permeation tube system**

A calibrated HCHO permeation tube in a temperature-controlled oven provides a known permeation rate (ng/min). The permeation stream is swept by a carrier flow and diluted to the challenge concentration. Permeation-based generation is described in OSHA Method 52 and NIST literature as a validated traceable approach.

Status: **REQUIRES QUOTE** for both the permeation tube (Kin-Tek, VICI Metronics) and the controller oven. India availability **UNKNOWN**.

**Architecture C — Validated electrochemical generator**

Some laboratory instruments generate HCHO electrochemically from methanol oxidation at a calibrated rate. These require validation, regular standard-gas verification, and are typically higher cost.

Status: **UNKNOWN** — not recommended for initial setup without institutional analytical chemistry support.

### 7.4 Required system elements (for Architecture A)

| Element | Specification | Status |
|---|---|---|
| Standard HCHO gas cylinder | ≥ 5 ppm HCHO in zero air or N₂; NIST/NPL-traceable; ±2% certified uncertainty; SDS | REQUIRES QUOTE |
| MFC for standard gas | 0–2 L/min range, air/N₂ compatible, calibrated; ±1% FS | REQUIRES QUOTE |
| MFC for zero air | 0–80 L/min range; calibrated ±1% FS | REQUIRES QUOTE |
| Zero/clean air supply | Compressed air with activated-carbon trap + molecular sieve (HCHO blank < 5 µg/m³ verified) | GENERIC REQUIREMENT |
| Static mixer | 100–200 mm SS or PTFE tube with turbulence inserts or a baffle | GENERIC REQUIREMENT |
| RH conditioning | Humidifier (Nafion tube or bubbler) + RH sensor; delivers 50 ± 5% RH into the mixing volume | GENERIC REQUIREMENT |
| Downstream capture | Carbon scrubber (Purafil or equivalent HCHO-rated media) → facility exhaust | GENERIC REQUIREMENT |
| Area HCHO monitor | Calibrated, independent from research sensors; alarm at ≥ 0.05 ppm | REQUIRES QUOTE |
| Fume hood / enclosure | Institutional certified, ≥ 0.3 m/s face velocity, exhausted | GENERIC REQUIREMENT |

### 7.5 HCHO challenge verification

Do not rely solely on the calculated dilution ratio to confirm the actual challenge concentration. Before directing challenge air through the test bed:

1. Run challenge air through the bypass path (no media) with both upstream and downstream SFA30s in-line.
2. Compare SFA30 upstream and downstream readings — they must agree within ±5% on the bypass.
3. Collect one upstream DNPH reference sample during the stabilization period.
4. Analyze the DNPH sample to verify that the actual C_in matches the calculated generation rate.
5. Only after verified stable C_in should the HCHO stream be routed through the test bed.

---

## 8. SFA30 — Verified Current Documentation

**Source: Sensirion SFA30 Datasheet v1.3, January 2025 — VERIFIED PRODUCT**
[https://sensirion.com/media/documents/DEB1C6D6/6789009D/GAS_DS_SFA30_D1.pdf](https://sensirion.com/media/documents/DEB1C6D6/6789009D/GAS_DS_SFA30_D1.pdf)

### 8.1 Measurement range and accuracy

| Parameter | Specification | Source | Interpretation |
|---|---|---|---|
| Measurement principle | Electrochemical | Sensirion DS v1.3 | Consumes an electrochemical cell; has finite lifetime |
| HCHO range | 0 to 1000 ppb | Sensirion DS v1.3 | Covers 0–1000 ppb; 81.3 ppb = 100 µg/m³ |
| Resolution | 1 ppb | Sensirion DS v1.3 | Display resolution, not accuracy |
| Accuracy | ±20 ppb or ±20% of reading, whichever is larger | Sensirion DS v1.3 | Applies at reference conditions only |
| Reference conditions for accuracy | 25 ± 3°C, 50 ± 5% RH | Sensirion DS v1.3 | Outside these limits, accuracy is unspecified |
| LOD | < 20 ppb (manufacturer stated) | Sensirion flyer | Manufacturer claim; not independently verified for this project |
| Output update rate | 0.5 s | Sensirion DS v1.3 | Internal averaging is slower than 0.5 s |
| Power-up suppression | First 10 s output suppressed | Sensirion DS v1.3 | Allow ≥ 60 s warm-up before recording breakthrough data |
| Response time (t63) | ~ 1 min (approximate, from flyer) | Sensirion flyer | True t63 must be measured for the actual deployment configuration |
| T/RH output | Integrated SHT sensor; reports T and RH | Sensirion DS v1.3 | Allows T/RH monitoring on same module |

### 8.2 Interface and supply

| Parameter | Specification |
|---|---|
| Primary interface | I²C, up to 400 kHz |
| Secondary interface | UART (selectable) |
| Supply voltage | 3.3 V ± 0.15 V (VDD) |
| Optional VPP | 4.5–5.5 V (pin 3) for UART mode |
| Typical current | < 4 mA in operation |
| Connector | 7-pin ZIF connector |
| Module dimensions | 56 mm × 16 mm × 5.5 mm (PCB) |
| Lifetime (manufacturer) | 6 years |
| Operating temperature | 0–50°C |
| Operating humidity | 0–95% RH non-condensing |

### 8.3 Cross-sensitivity

The SFA30 datasheet states "ultra low cross-sensitivity to ethanol." A peer-reviewed laboratory study (PMC12115294, 2026) evaluated low-cost electrochemical HCHO sensors, including response in the presence of CO, NO, NO₂, O₃, isobutylene, methanol, and isopropyl alcohol. Specific quantified cross-sensitivity values for the SFA30 from the Sensirion v1.3 datasheet are not reproduced here because they should be read from the current official document for the specific lot tested.

**Known limitation:** electrochemical sensors can respond to other reducing gases. For a clean-air packed-bed breakthrough test where the challenge gas is controlled, cross-sensitivity is a secondary concern. If the experiment ever uses mixed atmospheres (humidity, CO₂), the cross-sensitivity response must be characterized before interpreting small concentration changes.

### 8.4 Critical limitations relevant to Phase 15

| Issue | Consequence for experiment |
|---|---|
| ±20 ppb accuracy floor | At 50 µg/m³ inlet (40.7 ppb), the sensor accuracy is ±20 ppb = ±49% of reading. The SFA30 cannot reliably measure `C/C0 = 0.10` at the 50 µg/m³ inlet level alone. |
| Accuracy applies only at reference conditions (25 ± 3°C, 50 ± 5% RH) | At 25°C/70% RH (stress condition), sensor output may be outside the stated accuracy; log actual T/RH and treat readings as indicative only |
| ~1 min response time | A step change in HCHO at the downstream port takes ~1 min to register fully; this sets a minimum time-resolution for computing `C/C0(t)` |
| Must not be the sole validation instrument | SFA30 is the continuous trend instrument; DNPH–HPLC is the concentration reference. Around `t10`, the SFA30 reading must be bracketed by DNPH reference samples. |
| Co-location requirement | Two modules from the same lot may have channel-to-channel bias; co-locate on the same inlet stream before every campaign and quantify offset; swap positions in a repeat run |

### 8.5 India procurement

| Channel | Status | Notes |
|---|---|---|
| E Control Devices India | ₹7,099/unit for SFA30-D-T — **CANDIDATE PRODUCT** | Price is a single observed distributor listing; verify current stock and pricing |
| RS Components India | Listed (RS part 212-1795 for SFA30-D-T) — **CANDIDATE PRODUCT** | Check in.rsdelivers.com for current India stock and price |
| Arrow.com | $56.21 USD single unit — **CANDIDATE PRODUCT** | International shipping; import duty applies |

**Minimum recommended quantity:** 2 units (upstream + downstream). Buy 3 to allow one spare.

---

## 9. DNPH / HPLC Reference Method

### 9.1 Method basis

- **Primary method:** ISO 16000-3:2022 — *Indoor air — Determination of formaldehyde and other carbonyl compounds* — active sampling on DNPH-coated sorbent, HPLC/UV analysis — **AUTHORITY SOURCE**
- **Supporting method:** US EPA Compendium Method TO-11A — same analytical principle, widely referenced
- **Approximate method range:** 1 µg/m³ to 1 mg/m³ depending on sampling volume and laboratory method — **ISO 16000-3 stated range**

### 9.2 Sampling workflow

| Step | Specification | Evidence class |
|---|---|---|
| Sorbent | DNPH-coated silica gel cartridge (e.g., Waters Sep-Pak DNPH-Silica Plus, or Supelco LpDNPH S10 equivalent) | **CANDIDATE PRODUCT** — confirm India supplier (see Section 9.6) |
| Sampling pump | Calibrated personal sampling pump, flow 0.5–2.0 L/min ± 2%, suitable for HCHO environment | **GENERIC REQUIREMENT** |
| Sampling duration | 30–120 min per cartridge; adjust to collect ≥ 3 µg total HCHO above the method quantification limit | **DERIVED** from expected C_in and pump flow |
| Upstream sample | Paired cartridges (A + B) at upstream port, same interval as downstream | **PROPOSED PROJECT TARGET** |
| Downstream sample | Paired cartridges at downstream port | **PROPOSED PROJECT TARGET** |
| Blank cartridge | Collect one blank (capped, not exposed to air) per campaign batch | **PROPOSED PROJECT TARGET** |
| Field blank | Use one cartridge at ambient lab air before the run to characterize background | **PROPOSED PROJECT TARGET** |
| Transport and storage | Keep in sealed vials in a cool dark container; ship to laboratory on ice; analyse within 30 days (ISO 16000-3) | **ISO METHOD REQUIREMENT** |
| Chain of custody | Cartridge ID, collection start/end time, flow rate, total volume, operator, storage condition — label every vial | **GENERIC REQUIREMENT** |

### 9.3 Analytical sequence (outsourced to external laboratory)

This project does not currently own an HPLC. All analytical steps below are performed by an **external analytical laboratory service**.

| Step | Specification |
|---|---|
| Desorption | Elute with acetonitrile under the laboratory's validated protocol |
| HPLC analysis | Reverse-phase HPLC with UV detection at 360 nm; C18 column |
| Calibration | Five-point calibration curve with formaldehyde-DNPH certified reference standard |
| Reporting | µg/m³ HCHO per sample with expanded uncertainty (k=2) and method LOQ |
| QA | Analytical blank, duplicate injection, %RSD < 5% between replicates |

The external laboratory must:
- Hold ISO/IEC 17025 accreditation or institutional equivalence for carbonyl compound analysis
- Provide a calibration certificate for the reference standard (e.g., AccuStandard CRM47177 or Sigma-Aldrich equivalent)
- Report the expanded measurement uncertainty alongside the concentration

### 9.4 Calculation

HCHO concentration from DNPH sampling:

`C (µg/m³) = (mass_analyte_µg − mass_blank_µg) / V_sample_m³`

where `V_sample = Q_pump × t_sample`.

For C/C0 reference validation:
`(C/C0)_DNPH = C_downstream / C_upstream`

where both concentrations are derived from cartridges collected over the same time interval.

### 9.5 Limitation on breakthrough time resolution

DNPH cartridges integrate over the sampling interval; they cannot resolve instantaneous C/C0. Around `t10`:
- Use shorter sequential cartridges (e.g., four 30-min intervals instead of one 2-hour cartridge)
- Compare the resulting time-integrated DNPH ratios with the SFA30 continuous curve
- If DNPH brackets indicate `C/C0` crossing 0.10 within an interval but the SFA30 shows it earlier or later, report `t10` as an interval rather than a precise timestamp

### 9.6 India analytical laboratory options

**In-house:** Not applicable — no HPLC is available.

**Institutional collaboration (preferred):** Chemistry or environmental engineering departments of IITs, NITs, and CSIR institutes (NCL Pune, NEERI Nagpur, TERI) commonly perform aldehyde analysis. This project should approach an institutional collaborator before purchasing DNPH cartridges.

**Commercial laboratory services:** Bureau Veritas India, SGS India, NABL-accredited environmental labs — **REQUIRES QUOTE** for carbonyl compound analysis.

**DNPH cartridge procurement India:**
- Waters Sep-Pak DNPH-Silica or Supelco LpDNPH S10 — available through scientific distributors (Sigma-Aldrich India, HiMedia, Himedia Labs) — **CANDIDATE PRODUCT, REQUIRES QUOTE**
- Typical cost internationally: $5–15 USD per cartridge (quantity-dependent) — India price **UNKNOWN, REQUIRES QUOTE**

---

## 10. Temperature and Relative Humidity Measurement

### 10.1 Required measurement points

| Location | Purpose |
|---|---|
| Upstream of packed bed (combined with SFA30 #1) | Baseline T/RH entering the bed; needed to confirm 25 ± 2°C, 50 ± 5% RH |
| Downstream of packed bed (combined with SFA30 #2) | Detect temperature rise (adsorption is mildly exothermic); monitor humidity change across bed |
| Room ambient | Log laboratory conditions for data record |

### 10.2 SFA30 integrated T/RH sensor

The SFA30 module includes an integrated SHT sensor reporting temperature and relative humidity on the same I²C bus. This provides convenient co-location of HCHO, T, and RH at each measurement port.

Accuracy from the SFA30 datasheet:
- Temperature: ±0.5°C typical (SHT specifications)
- Relative humidity: ±3% RH typical

The integrated SHT sensors are adequate for monitoring the baseline conditions and detecting large deviations. If stress conditions (25°C/70% RH or 30°C/70% RH) are tested, a dedicated calibrated RH/T reference instrument should be co-located to confirm the setpoint.

### 10.3 Dedicated T/RH reference

For stress-condition experiments, use a calibrated reference probe (e.g., Vaisala HMP series, E+E EE33, or calibrated SHT4x-based instrument) — **CANDIDATE PRODUCT, REQUIRES QUOTE**. This instrument is not the primary measurement; it confirms the stress setpoint.

---

## 11. Transport-Delay Measurement

### 11.1 Why it matters

The downstream SFA30 is physically separated from the upstream SFA30 by the packed bed, tube lengths, and potentially a short settling chamber. A step change in upstream concentration takes a finite time to appear downstream even without any adsorption (simply due to the transit time of air in the rig). If this delay is not subtracted before computing `C/C0(t)`, the early breakthrough curve is artificially delayed and `t10` is reported too late.

### 11.2 Measurement procedure

Using clean air only (no HCHO):

1. Establish steady airflow at the baseline condition (68.9 L/min for 75 mm, 26 mm baseline bed).
2. With the packed bed bypassed or replaced by an empty column of the same internal volume, introduce a step-change in a detectable tracer gas (CO₂ from a cylinder or a known HCHO spike from the generation system with prior approval).
3. Record the upstream and downstream SFA30 responses at 0.5 s resolution.
4. Measure the lag time `Δt_transport` = time between the upstream step-rise midpoint and the downstream step-rise midpoint.
5. Repeat at each velocity point in the matrix.
6. Apply `Δt_transport(U_s)` as a time-shift correction to all downstream concentration records before calculating `C/C0(t)`.

**Note:** CO₂ is preferable to HCHO for this test because it involves no hazardous gas and a widely available sensor.

---

## 12. Blank and Zero Procedures

### 12.1 Media-off-gassing blank

Before any breakthrough test, operate the sealed packed bed with clean zero air at the test flow rate and temperature for at least 30 minutes. Log both SFA30s. If the downstream SFA30 shows sustained HCHO > 5 ppb above the upstream reading during this clean-air run, the media is releasing formaldehyde or another electrochemically active compound. **Do not proceed to breakthrough testing until this blank passes.**

### 12.2 Rig blank

With no media installed (empty column), pass zero air through the full rig and confirm both SFA30s read within ±5 ppb of each other and within ±5 ppb of zero. This checks for HCHO adsorption and off-gassing from tubing, seals, and column material.

### 12.3 DNPH blank

One unused DNPH cartridge per campaign should be handled identically to field cartridges but not exposed to air. Its analysis result is the cartridge blank. Subtract this from all field samples.

---

## 13. Experimental Readiness Gate

This sequence must be completed before any HCHO challenge gas is introduced:

| Gate item | Requirement | Verified by |
|---|---|---|
| Institutional safety approval | Written approval from laboratory/institutional safety office | Document held by PI / supervisor |
| Chemical risk assessment | Completed, reviewed, filed | Safety officer |
| Media available and documented | Lot certificate, SDS, dry mass, particle-size check | Physical measurement |
| Rig leak test | Zero pressure decay over 10 min at 1 kPa overpressure | Operator log |
| Instrument co-location | Both SFA30s read within ±5 ppb on the same air stream | Logged data |
| Transport-delay measured | `Δt_transport` recorded at each velocity | Logged data |
| Media-off-gassing blank | Downstream SFA30 ≤ 5 ppb above upstream on clean air for 30 min | Logged data |
| DNPH chain-of-custody ready | Cartridges labelled, pump calibrated, external lab confirmed | Pre-run checklist |
| Emergency stop and shutdown procedure | Written, trained, posted | Safety documentation |
| Exhaust/capture operational | Scrubber or facility exhaust confirmed running | Pre-run checklist |
| Area HCHO alarm tested | Alarm fires below 0.05 ppm in test | Safety log |

---

## 14. Safety Boundary

| Boundary | Limit | Enforcement |
|---|---|---|
| Maximum HCHO concentration in experiment | 200 µg/m³ (162.6 ppb) inlet; Phase 14 maximum test point | Set by MFC/dilution ratio before run start |
| NIOSH ceiling (occupational) | 0.1 ppm / 123 µg/m³ for 15 min | Area alarm must trigger at ≥ 0.05 ppm; 0.1 ppm is not an operating permission |
| Personnel in lab during HCHO operation | Trained personnel only; PPE as per risk assessment | Institutional safety procedure |
| Discharge to room | Prohibited | Scrubber + facility exhaust mandatory |
| Student operation without supervision | Prohibited | Institutional policy |
| Ppm-scale HCHO acceleration | Prohibited without separate institutional protocol | Phase 14 guardrail |

---

## 15. Acceptance Criteria

| Requirement | Status |
|---|---|
| Column architecture defined | **READY** |
| Column diameter selected (75 mm recommended) | **READY** |
| Bed-depth matrix defined (26, 52, 104 mm) | **READY** |
| Flow matrix defined (0.13–1.05 m/s, tabulated) | **READY** |
| Pressure measurement defined (0–500 Pa, ≤1 Pa resolution) | **READY** |
| Flow measurement defined (rotameter + needle valve; MFC for breakthrough) | **READY** |
| HCHO sensing defined (SFA30 × 2; architecture and limitations documented) | **READY** |
| DNPH validation defined (ISO 16000-3; outsourced HPLC) | **READY** |
| Controlled HCHO generation defined (Architecture A — cylinder + dilution) | **PARTIALLY READY** — specification complete; institutional facility and cylinder procurement not yet secured |
| Safety boundary defined | **READY** |
| Media containment defined | **READY** |
| Sampling ports defined | **READY** |
| Data schema defined | See PHASE15_DATA_ACQUISITION_SPEC.md — **READY** |
| BOM complete | See PHASE15_BOM.md — **PARTIALLY READY** — all items classified; prices partially unknown |
| India procurement researched | **PARTIALLY READY** — key items classified; quotes required for several critical items |
| Cost tiers established | See PHASE15_BOM.md — **READY** |
| Experimental readiness gate defined | **READY** |

---

## 16. References

- Phase 14 formaldehyde target specification: `docs/PHASE14_FORMALDEHYDE_TARGET.md`
- Phase 13 material selection: `docs/BIOCHAR_MATERIAL_SELECTION.md`
- Phase 13 experiment plan: `docs/BIOCHAR_EXPERIMENT_PLAN.md`
- Sensirion SFA30 Datasheet v1.3 (January 2025): https://sensirion.com/media/documents/DEB1C6D6/6789009D/GAS_DS_SFA30_D1.pdf
- Sensirion SFA30 Laboratory Testing Guide: https://sensirion.com/media/documents/BA78378E/65F015E2/GAS_AN_SFA30_Laboratory_Testing_Guide_D1.pdf
- ISO 16000-3:2022: https://www.iso.org/standard/81864.html
- US EPA TO-11A: https://www.epa.gov/sites/default/files/2019-11/documents/to-11ar.pdf
- OSHA Method 52 (permeation generation): https://www.osha.gov/sites/default/files/methods/osha-52.pdf
- Calgon Carbon OVC 4×8 Product Bulletin: https://www.calgoncarbon.com/app/uploads/DS-OVC4x815-EIN-E2.pdf
- Calgon Carbon FORMASORB Product Bulletin: https://www.calgoncarbon.com/app/uploads/FORMASORB.pdf
- Activated Carbon Industry pressure-drop test method: https://www.activatedcarbon.org/wp-content/uploads/2025/02/Test_method_for_Activated_Carbon_86.pdf
