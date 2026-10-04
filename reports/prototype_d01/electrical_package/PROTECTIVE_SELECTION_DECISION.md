# Protective control decision — 4 October 2026

**Outcome: no drop-in protective relay selected.** This closes three specific candidate screens, not the electrical release gate. Do not buy one of these parts merely because it is described as a safety relay.

## Actual products checked

| OEM reference | Verified relevant data | Project decision |
|---|---|---|
| [Pilz PNOZ X5, 774326](https://www.pilz.com/en-INT/eshop/product/774326) | 12 V DC; 2.5 W; automatic/manual start; body87 x22.5 x121 mm | Fits voltage, not a demonstrated solution to the required monitored restart sequence. Catalogue manual start must not be assumed to reject a held button. |
| [Pilz PNOZ X9P, 777607](https://www.pilz.com/en-INT/eshop/product/777607) | 12 V DC; 7 W; monitored start; body94 x90 x121 mm | Reject as a drop-in on the current24 W supply and side enclosure. Fans plus relay already23.8 W nominal, before hub/controller consumption. |
| [Pilz PNOZ s4, 750104](https://www.pilz.com/en-US/eshop/product/750104) | 24 V DC; 2.5 W | Retain as a reference for a separately powered external control assembly, NOT a selected part. Cannot connect its supply input to the12 V rail. |

The [s4 manual 21396-EN-17](https://www.pilz.com/download/open/PNOZ_s4_Operat_Man_21396-EN-17.pdf), printed pages10–11 and28, documents monitored-edge start and a98 x22.5 x120 mm body. It calls for at least IP54 control-cabinet protection. These are component requirements, not proof that an assembled D01 meets any safety level. A reset/start input energizing relay outputs is not automatically our separate RESET-then-START sequence.

Checked4 October2026. Prices, India stock, lead times and delivered revisions UNKNOWN. Product listings are evidence of products/specifications, not availability commitments. No procurement or supplier contact.

## Numerical consequences

Calculated from the published nominal values:

- X5 + fans:19.3 W, leaving4.7 W before other loads and startup. This arithmetic alone does not approve the combination.
- X9P + fans:23.8 W, leaving0.2 W. With an **assumed**, not measured,1.25x fan-current multiplier, demand becomes28 W before other loads.
- s4 needs a compatible24 V supply domain; no converter or second adapter is selected. A second supply creates another isolation and recovery condition.

Normal DIN mounting puts120–121 mm device depth against a40 mm reservation: not a fit. However, we must not claim that every orientation fails: bare s4 and X5 bodies can fit after rotation inside the nominal140 x100 x40 box. That excludes enclosure walls, DIN rail, terminals, cables, hub/controller and clearances, so it is not an enclosure design. X9P fails all six axis-aligned body orientations. Do not enlarge the cabinet or modify CAD based on an unselected circuit.

## Why simply adding a safety relay does not solve the circuit

Two reproducible counterexamples are in PROTECTIVE_CANDIDATE_SCREEN.json:

1. **Separate control power survives:** RUN contact remains closed while fan12 V disappears. Fan12 V returns; power reaches fans again without a fresh START. An upstream relay with no relevant power-domain sensing does not block this path.
2. **Downstream recovery:** upstream12 V remains healthy while hub/fan output disappears and later recovers. An upstream voltage monitor sees no change. Adding that monitor alone cannot establish the required downstream recovery response.

These are logical possibilities, not measurements or claims about exact OEM timing. Fan-speed feedback cannot prove safe standstill. One hub RPM signal cannot establish the state of all four fans. No single named relay above has been shown to supply the complete required sensing, separate start sequence and coordinated switching.

## Design direction, without silently weakening requirements

Keep the current fixed-guard, supervised indoor route. Treat physical service isolation and prevention of hazardous access as essential; do not rely on RPM or a laptop to permit access. Determine through a documented risk assessment which restart events create a hazard with guards fitted and which are only test interruptions. Do not assume industrial safety-relay complexity is mandatory merely because fans can restart, and do not delete restart requirements merely to simplify shopping.

The broad existing rule that **every internal fan/hub reset must latch the entire system off** is not yet supported by a hazard-to-protection analysis. It remains the current requirement pending review, not a proven feature. A justified fixed-guard appliance architecture may be simpler; that requires actual guard/access and abnormal-operation evaluation. This is a proposed review direction, not permission to build or operate.

The precise missing design decision is the required protective function/reliability for actual reachable hazards. Once defined, select sensing, switching, sequence, isolation and enclosure together. Contact current ratings for resistive loads alone do not establish suitability for electronic fan startup. No fuse, terminal, wire size or protective-level claim is invented here.

## Reproduce and limits

Run `python scripts/analysis/d01_protective_candidate_screen.py` from the repository root. Eight checks cover load arithmetic, orientation screening and idealized failure paths. None is a hardware safety test. Historical PDF E00 remains unchanged; this decision and JSON are supplementary evidence in its existing folder. Source CAD remains unchanged. No physical prototype or test result is claimed.
