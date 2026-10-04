# Mechanical batch result — current R03M

**Digital requirement calculations completed; physical build release remains OPEN.**

## What was actually solved

Saved CAD mesh independently confirms both filter stop gaps are **43 mm**: 40 mm filter proxy plus 3 mm installed gasket. Each inner sleeve is **36 mm**, leaving a 7 mm stack offset. This is a dimension extraction, not a delivered-filter measurement.

The new interval solver establishes whether ONE fixed stop can cover every supplied filter/gasket/flatness tolerance. It also returns the required sleeve length if a robust window exists. No new CAD branch was created.

| Assumed case | Required nominal gap, mm | Fixed stop possible? | Candidate sleeve, mm |
|---|---:|---|---:|
| historical_thickness_sensitivity | 43.65 to 41.95 | NO | — |
| illustrative_matched_parts | 42.66 to 42.92 | Yes, for these assumptions only | 35.79 |
| illustrative_wider_gasket_tolerance | 42.90 to 42.60 | NO | — |

**Do not manufacture these candidate sleeves.** The illustrative 20–40% compression bounds are not a supplier recommendation. With broad 39–41 mm filters, no fixed stop satisfies that illustrative range. Individually matched measured parts may admit a narrow window, but actual gasket limits must replace these assumptions first. Tightening more is not a valid substitute: gasket force and filter frame strength remain unknown.

## Cabinet joint demand, not capacity

Four actual groups of eight cabinet through-bolts were extracted. Loads are distributed using a linear equal-stiffness in-plane model, with no friction credit. All forces and moments are recovered by explicit equilibrium tests. In the illustrative 30 N vertical / 100 mm horizontal-offset case:

- `K06_End_False_`: 8 bolts; peak calculated in-plane demand **5.151 N/bolt**.
- `K06_End_True_`: 8 bolts; peak calculated in-plane demand **5.151 N/bolt**.
- `K07_Seat_False_`: 8 bolts; peak calculated in-plane demand **5.036 N/bolt**.
- `K07_Seat_True_`: 8 bolts; peak calculated in-plane demand **5.036 N/bolt**.

These are not accepted service/test loads or capacity ratings. The model omits out-of-plane prying, panel bending/racking, wood bearing/edge breakout, screw withdrawal, joint compliance and clamps. The four groups cannot be summed as if they share load equally. Top/base wood screws remain unsuitable as an assumed lifting path; never lift by the lid.

Exact modeled gasket ring area: **12800.0 mm²** per filter. Total idealized clamp force = supplier compression stress (MPa) × this contact area (mm²). The stress and resulting force are intentionally **UNKNOWN**; filter airflow pressure does not define gasket closing force.

## Remaining exact evidence

- Exact filter delivered thickness/frame tolerance and compression strength
- Selected gasket free thickness tolerance, compression window, force/relaxation/adhesive data
- Measured reducer/retainer flatness and assembled stop gap; seam/feedthrough leak integrity
- Selected plywood/cleat grades, fastener threads/grades/torque and withdrawal/bearing design
- Cabinet racking, guard perforated plate/weld/attachment/probe and stability review
- Full installed mass/CG, foot contact/friction and accepted service/cable/push loads

Actual perforated guard/weld/attachment/probe qualification is still open. Existing solid-strip sensitivity is not a perforated guard proof and has not been promoted to one. No restart/isolation requirement was weakened. Physical prototypes: **0**.

## Reproduce / review

`python scripts/analysis/d01_mechanical_release_batch.py`

`python scripts/analysis/test_d01_mechanical_release_batch.py`

Standard library only, repository or packaged engineering root. JSON records exact input hashes, extracted coordinates, conditional force vectors and unresolved inputs. Tests are synthetic/arithmetic—not physical. Original R03M native CAD, DXFs and historical evidence are unchanged.
