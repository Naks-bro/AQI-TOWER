# Supplier questions before component freeze

Prepared 2 October 2026. DRAFT FOR TEAM REVIEW — not sent. No supplier approval, commitment or price is implied.

Project: student-led particulate air-cleaning tower; first commissioning indoors, later a separately designed outdoor pilot. Round-shell packaging is preliminary. Screening flow 1,200–1,300 m3/h is not a final accepted performance target. Carbon, solar and water are not part of the first test assembly.

## Fan supplier

3 October fan-specific revision: use [selection brief R00](FAN_SELECTION_BRIEF_R00.md) and [response sheet](FAN_SUPPLIER_RESPONSE_R00.csv) for named clean/loaded screening points and complete OEM evidence. Earlier broad ranges are exploratory, not an ordering specification. Both requests remain NOT SENT.

Please propose a suitable fan for a sealed prefilter/HEPA assembly and provide:

1. Exact purchasable model/article number, India availability, lead time, warranty and quote including tax/freight.
2. Full speed-dependent pressure/flow curves with stated static/total pressure basis, air density, electrical input and sound data at duty points. The complete loss budget is being developed; provide selection coverage around 1,200–1,300 m3/h over 200–500 Pa as an exploratory range, NOT an established requirement.
3. Dimensioned drawing or STEP: casing, inlet/outlet, mounting holes, mass, allowed orientation and service clearances. Clarify whether the old KVO 250 / KVO 250 L / article 2027 reference is supported or superseded; do not substitute an EC version without identifying the new curve and drawing.
4. OEM power/control schematic, motor protection and reset behaviour, approved speed controller, inrush/current, earthing, enclosure rating and environmental limitations.
5. Recommended adapters, guards and mounting isolation; confirm no unintended throttling or bypass in the proposed installation.

Do not freeze the fan just because its free-air flow exceeds the target. Current historical curve yields about 137 Pa at 1,300 m3/h, nearly all used by the optimistic clean filter/duct estimate. New guards, transitions and filter loading require reevaluation.

## HEPA supplier

Reference candidate: Freudenberg SF13-B, 593 x 593 x 292 mm. Please confirm exact article and offer alternatives if preferable:

1. Dimensioned frame section, actual media opening, tolerances, weight, seal plane/profile, handling limits and permitted horizontal/upward-flow orientation.
2. Initial pressure-loss curve across our proposed flow range, terminal pressure/flow limits and safe storage/humidity conditions. A single nominal point is insufficient to characterize loaded behaviour.
3. Unit-level class/test documentation and instructions for installed seal/integrity verification. Confirm service availability and recurring replacement cost/lead time.
4. Gasket material, uncompressed/installed size, required seating force or compression, mating ledge finish/flatness and compatible clamp arrangement. Review the illustrative R01 interface; do not assume it fits the actual frame.

## Coarse-filter supplier

Reference candidate: washable coarse panel, approximately 592 x 592 x 48 mm. Confirm classification/testing, dimensions, mass, clean/loaded curves, safe final resistance, washing/drying procedure if washable, replacement life conditions and supply. Historical G4 language must not be assumed equivalent to a particular ISO coarse percentage without documented testing.

## Fabricator / qualified paid mechanical reviewer

Current delivery basis: no college lab or faculty reviewer assumed. Optional ENTC feedback is separate and unconfirmed; it does not replace required qualified physical review.

Read `docs/build/M05_HARDWARE_GASKET_REVIEW.md`: C5 cutouts are not drop-in replacements for the generic blocks. Ask closure supplier for usable closing-force/travel data, not only maximum static load. Ask seal supplier for full force-versus-compression curve, thickness tolerances, suitable profile/material, corner/joint details and required compression stops. Review rim-only versus relocated through-cover or external closures and supported removal before choosing quantities. The illustrative PORON calculation is not a selected seal requirement.

Latest access option is `docs/build/M05_HEPA_SERVICE_HATCH.md`. Review a removable 675x340 mm cover study with eight generic latch locations—not selected hardware. Request actual closure CAD, grip/travel, catches/mounting, load/environment limits and working sweep; obtain gasket profile/force-compression data and decide closing-force distribution. Review cover stiffness and support against dropping during release. Do not quote/order eight latches or use 3 mm as a compression requirement from this sketch.

Review supplier drawings first. Specify frame/base design, rated fan/filter supports, enclosure gauge, sealing ledges, service tray/clamp/door mechanisms, guarding, corrosion finish and structural stability. R01 wall/plate dimensions are geometry assumptions, not approved manufacturing selections. Ask for a reviewed drawing quotation, not immediate cutting from the STEP.

## Response acceptance checklist

Record source/date/revision and exact SKU for every response. Match the curve to that SKU; distinguish static vs total pressure and measured vs extrapolated values. Confirm components fit and remain serviceable together. Update CAD, BOM and full clean/loaded loss budget before selecting; obtain electrical/mechanical sign-off before fabrication release.
