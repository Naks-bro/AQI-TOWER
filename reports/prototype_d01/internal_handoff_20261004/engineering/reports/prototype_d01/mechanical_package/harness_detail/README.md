# Fan harness routing study — R03M

## Final public-source check — 4 October 2026

The current ARCTIC support downloads link the [P14 Max straight-spoke drawing, revision24 January2025](https://support.arctic.de/products/p14-max/techdocs/P14%20Max%20%28Straight%20spokes%29%20-%20%202D%20drawing%20%2820250124%29.pdf). Published dimensions confirm140 x140 x27 mm,125 mm mounting pitch and4.40 mm holes for ACFAN00287A. The reviewed drawing does not establish the required cable/connector envelope or clamping section. The [current Noctua NA-SEC1 information sheet](https://cdn.noctua.at/media/noctua_na_sec1_datasheet_en_web.pdf?download=true) confirms300 mm extensions but does not supply the required connector and sleeve cross-section dimensions. Packaging dimensions are NOT connector dimensions.

**This interface is blocked on specific missing evidence, not on another CAD iteration.** Keep the guard uncut. Obtain either authoritative dimensioned cable/connector drawings for the exact revisions, or an unpowered physical sample of one P14 Max and one intended extension to measure the connector maximum envelope, cable section where clamped, lead emergence and usable length. Also establish permitted bend/retention treatment before finalizing strain relief. A sample inspection closes geometry only, not startup, electrical protection, guard strength or airflow validation.

Recommended next external action: request the missing drawings from the manufacturers with user authorization. No enquiry sent. Alternative: sample-only acquisition and unpowered inspection with separate purchase authorization; do not order the full tower bill of materials. Further broad catalogue searches or generic connector substitution will not establish the exact supplied interface. Do not portray this as the entire project's only remaining blocker.

4 October2026. **Not a released harness or guard entry.** Open D01_R03M_HARNESS_REVIEW.FCStd for the existing assembly plus four internal routing reservations. Source R03M is unchanged; do not substitute this study for manufacturing CAD.

## What was done

Four assumed3 mm diameter routes use the central gap between fan rows and the right-hand perimeter space. They terminate at x433, inside the guard, at z590/594/598/602 mm. Each clears the existing physical CAD objects; six route-pair checks also show no positive-volume intersection. Native file reopened with497 valid objects. Fan cable emergence points are assumptions, not verified OEM geometry. Sharp polyline elbows are not manufacturing bend radii.

| Lead | Approximate path to enclosure reference + assumed50 mm allowance | Margin against listed400 mm lead |
|---|---:|---:|
| F1 |448 mm| -48 mm |
| F2 |302 mm| +98 mm |
| F3 |456 mm| -56 mm |
| F4 |310 mm| +90 mm |

Lengths include an unmodeled crossing and external corridor. Actual connector seating, route emergence, bend radius, retention and enclosure internals can change them. Positive margin is not fit approval.

## Source-backed parts direction

- [ARCTIC P14 Max specification sheet](https://www.arctic.de/media/8a/18/01/1710507321/Spec_Sheet_P14_Max_EN.pdf) lists400 mm cable. Historical black/white SKU inconsistencies remain unresolved; confirm delivered revision rather than assuming all sheets match.
- [Noctua NA-SEC1 specifications](https://www.noctua.at/en/products/na-sec1/specifications) list three300 mm extensions per set. Candidate: use an extension on the two longer paths if actual fit confirms the need. It is not a splitter, a protective device or a strain-relief component. Excess cable must be restrained away from fans; no purchase or India stock claim.
- [icotek QVT](https://www.icotek.com/en/products/cable-glands/qvt) and [KVT](https://www.icotek.com/en/products/cable-glands/kvt) are genuine split-entry families for cables with connectors. This supports a non-destructive entry approach, not selection of an insert or size. Sealing/retention of a flat bundle, sleeved lead or separate wires must not be assumed from a round-cable range. Component ingress ratings do not rate our guard or tower.

Sources checked4 October2026. Exact connector body dimensions, actual cable section, entry insert/blank choice, India availability and pricing UNKNOWN. Some legacy OEM PDF links failed; no downloaded product drawing or installation approval is claimed.

## Protected entry and restraint: still unresolved

Do not drill the guard based on the3 mm routing envelope. All guard geometry stays unchanged. Before a cutout is released, establish actual lead/connector geometry; select a compatible split insert/frame, locknut/backing and thickness range; place it outside fan/fastener/tool interference; design positive restraint on both sides without crushing insulation; and verify access protection with the entry fitted and under foreseeable pull/deflection.

Do not cut/depin OEM connectors just to fit an arbitrary hole. Do not pass unprotected wires over a sharp sheet edge. Do not use a loose foam plug or adhesive-only restraint as the sole protection against cable entry into the impeller. The outer guard's removal sequence must not pull on the fans' leads; isolation and reconnection prevention remain mandatory before service.

**Honest boundary:** internal route space and provisional extension needs are now checked. Actual guard entry, clamp geometry, fan cable emergence and complete routed harness remain incomplete. We have not completed the previously requested protected entry detail; the necessary exact interface dimensions were not established from public sources in this pass.

Reproduce with FreeCAD Python: `python scripts/geometry/route_d01_fan_harness.py`. Results in ROUTING_CHECKS.json. No physical tests, purchases, installations or contacts. Original package PDF/ZIP is unchanged.
