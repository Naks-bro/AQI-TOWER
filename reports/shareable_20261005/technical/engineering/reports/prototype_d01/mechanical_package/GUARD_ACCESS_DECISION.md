# D01: what must prevent access to the fans

4 October 2026. Geometry-based preliminary hazard review, **not a safety assessment approval**. Applies only to indoor R03M. Existing restart requirements remain in force.

## Decision

**RECOMMENDATION:** develop D01 around independently retained fixed upper and lower fan guards, with physical isolation before any service. Do not select door switches or industrial relays until their protective function is tied to the actual access arrangement. A filter is not a fan guard.

This is a proposed protection architecture, not a waiver of the current electrical sequence. We have not demonstrated that routine access is infrequent enough for fixed guarding alone, that the guards prevent hazardous reach, or that all abnormal-operation risks are covered. If foreseeable service requires reaching a moving hazard, protection must prevent that access; an instruction label or supervisor alone is insufficient.

## Read-only CAD findings

Audit: `scripts/geometry/audit_d01_guard_access.py`, output `GUARD_ACCESS_AUDIT.json`. R03M native file SHA256 remains `fb28a31315968509dcdbbb2caac8c6d69c84ecb94a35ccd75937a5d9ecaa33a6`.

- Four fan body envelopes occupy z581–608 mm. Upper guard inward face is z630: nominal22 mm to fan bodies. Lower guard inward face is z531: nominal50 mm to fan bodies. These are **not blade locations or compliant reach distances**.
- Both guard assemblies have minimum geometric distance zero to the fan plate. That proves contact somewhere, not a continuously closed, strong perimeter.
- Perforations are **not modeled in native 3D faces**. The separate proposed2D pattern has4 mm holes. A collision/probe test against the solid CAD face would falsely treat every hole as blocked; no safe-reach PASS is issued.
- Existing filter service checks remove retainers and service hardware, not fan guards. Both200 mm straight filter sweeps were clear. Retainer/hand/tool trajectories and access around the guards are unverified.
- The horizontal cable reservation starts at x435, tangent to the outer guard's exterior, and runs outward. It has **zero positive-volume overlap** with either guard. There is no modeled fan-to-reservation crossing, drilled opening, gland or harness. The correct defect is a **missing connection detail**, not a detected cable/guard collision.

## Hazard-to-protection map

| Use state | Credible hazard / exposure | Proposed primary measure | Current evidence and remaining gap |
|---|---|---|---|
| Normal operation, all panels fitted | Finger/object insertion at outlet; fan contact if guard bends or detaches | Retained upper guard, assessed openings/edges, stiff joints | Upper envelope exists; actual perforation reach, weld/fastener strength and deflection unproven |
| Filter removed | Hand or tool enters plenum toward fan inlet | Independent retained lower guard; service under isolation | Lower guard retained in service geometry; bypass-around-guard reach and removal trajectories not tested |
| Guard/top assembly removed | Direct fan contact and unexpected restart | Stop, isolate all power, prevent reconnection, verify stopped before removal | No released isolation hardware/procedure; no measured run-down; PWM zero not isolation |
| Cable connection or repair | Unprotected opening; abrasion or pull exposing conductors; cable touching fan | Closed retained feed-through, restraint and wiring kept out of moving region; isolated service | Connection route missing; no drilling or wiring released |
| Power or internal protection recovers, guards intact | Restart may create a hazard if access protection fails; test data invalidation | Effective access protection plus justified restart behavior | Current no-uncommanded-restart requirement remains; no proof that all recovery events need safety-rated latching |
| Tip, impact, blocked inlet, overheating or misuse | Guard deformation, exposed fan, fire or loss of stability | Structural/thermal/abnormal-operation evaluation, stable installation | Not resolved by an RPM signal, relay or current geometry audit; outdoor/public use excluded |

## Which functions stay, and which need justification

## Guard bending sensitivity — 4 October continuation

Executable: `python scripts/analysis/d01_guard_bending.py`; detailed output: [GUARD_BENDING_SENSITIVITY.json](GUARD_BENDING_SENSITIVITY.json). **28 synthetic arithmetic checks; 36 assumed scenarios; no guard strength PASS.** Native CAD, cut patterns and original PDF/ZIP are unchanged.

DETECTED: each proposed face is320x320x1 mm with2822 holes. The fabrication proposal joins its perimeter to side skirts; it is not a verified simply supported or fully clamped boundary. There is no designed central support. Net face material area from the actual pattern is0.0669377 m2. At an ASSUMED7850 kg/m3, the perforated face alone is0.525 kg; two faces total1.051 kg, excluding skirts, brackets and all fasteners.

ASSUMED diagnostic model: a solid rectangular strip with central force, simple end supports and E200000 MPa. Span300 mm, widths30/300 mm and forces10/30/60 N deliberately explore sensitivity. They are NOT actual load distribution, validated bounds or safety-standard proof loads. A150 mm span case assumes a new effective support that does not exist in current CAD.

| Solid-strip example,30 N,300 mm sharing width | Elastic deflection | Nominal elastic bending stress |
|---|---:|---:|
| 300 mm span,1 mm thick | 3.375 mm | 45 MPa |
| 300 mm span,1.5 mm thick | 1.000 mm | 20 MPa |
| 300 mm span,2 mm thick | 0.422 mm | 11.25 MPa |
| 150 mm span,1 mm thick; hypothetical added support | 0.422 mm | 22.5 MPa |

These are NOT predicted installed-guard deflections. In the1 mm example, deflection is already3.375 times thickness, warning against treating linear small-deflection plate behaviour as reliable. A30 mm sharing width raises the same strip deflection tenfold. Actual two-way action, local loading, hole ligaments, yielding, weld restraint and attachment compliance need a different analysis; neither strip width is a guaranteed conservative bound. Do not multiply solid stiffness by the remaining-area fraction to claim a perforated-sheet stiffness. No yield strength is assumed and no margin to failure is calculated.

RECOMMENDATION: retain the current CAD as review geometry, not a cutting release. Evaluate a thicker perforated face against an attached stiffener only with actual plate/support/joint behaviour. Doubling thickness doubles face mass (adds approximately1.051 kg across two faces at assumed density); a stiffener also obstructs airflow and loads its attachments. Neither option is selected here. Actual hole thickness-to-diameter effects can change losses even without changing open area. Do not transfer the current pressure-loss assumption as a measured result.

Closure remains a perforated-plate/attachment assessment with specified material and contact load, followed by an **unpowered** manufactured-guard strength/deformation and access assessment under applicable, qualified-review-approved criteria. No arbitrary force from this sensitivity table is a commissioning instruction.22/50 mm CAD face-to-body gaps are not allowable deflection or blade clearance.

Formula reference: [American Wood Council beam formulas, Figure7, hosted by Purdue](https://engineering.purdue.edu/~ce474/Docs/DA6-BeamFormulas.pdf), checked4 October2026. Only generic elastic beam equations are used, not wood material design values or guard requirements. `I=b*t^3/12`, `delta=P*L^3/(48*E*I)`, `M=P*L/4`, `sigma=M*t/(2*I)`, with N/mm/MPa units. Unknowns remain material grade, actual boundary stiffness, weld/attachment strength, applicable load/probe criteria and physical deformation.

## Protective functions retained

**Retain now:** local deliberate start/stop requirements; no remote start; service isolation with reconnection prevention; independently retained guards; no opening based on a zero-speed command; actual fault investigation before restarting a failed test. Do not accept powered filter service simply because the lower guard is drawn.

**Do not assume:** every internal fan reset requires a safety relay; every removable filter needs an interlocked door; an emergency stop is equivalent to service isolation; a relay's component safety rating certifies our system. Determine the relevant appliance/machine classification and applicable Indian requirements before claiming conformity.

**Potential simplification, pending review:** if fixed guards are verified to prevent access in all normal and filter-service configurations, internal fan restart need not be used as the sole means of preventing contact. This may avoid a multi-supply industrial safety panel. It does not remove electrical overload, thermal, service-isolation or normal stop/restart requirements. Any change to the existing blanket reset-latch rule must be recorded as an approved requirement revision, not silently applied here.

## Specific work needed to close this decision

1. Finish the actual fan harness and closed guard entry, including connector fit, bend/strain relief and maximum opening after assembly. Choose the entry with the real harness; no arbitrary large hole.
2. Establish guard test/probe and strength criteria from the applicable product safety requirements. Verify holes, side seams, fastener openings, cable entry and reachable routes with filters removed. Include deformation/tolerances; do not infer safety from nominal4 mm holes alone.
3. Establish service frequency/tasks and a workable isolation/reconnection-prevention arrangement covering every supply. Verify run-down without guessed delays.
4. Have a qualified reviewer accept the hazard-to-protection allocation and required reliability. Only then finalize whether an interlock/guard locking/restart latch is needed and select components accordingly.

These are exact release inputs, not a request for the user to contact suppliers. Digital preparation remains our work. Physical inspection/testing and qualified acceptance cannot be replaced by an online component search.

## Sources and limits

[HSE machinery safety](https://www.hse.gov.uk/work-equipment-machinery/introduction.htm) describes fixed guarding and alternatives where fixed guards are unsuitable. [HSE equipment overview](https://www.hse.gov.uk/work-equipment-machinery/puwer-overview.htm) distinguishes routine access and possible interlocked/locking guards. [HSE maintenance guidance](https://www.hse.gov.uk/work-equipment-machinery/maintenance.htm) supports safe maintenance and isolation. Checked4 October2026; used for general risk-reduction principles, **not Indian law or proof of D01 compliance**.

No numerical safety distance, required performance level, test force or stop time has been invented. No CAD geometry modified, physical test performed, purchase, contact or installation made. Original mechanical and electrical PDFs/ZIPs are unchanged; this is supplemental evidence.
