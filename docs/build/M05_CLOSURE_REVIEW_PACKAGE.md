# HEPA hatch: supplier and workshop review package

3 October 2026. DRAFT FOR REVIEW — NOT AN ORDER OR FABRICATION DRAWING.

## What we need to decide

Choose a real way to close, seal and safely remove the HEPA access cover. The current CAD only shows available space. Do not manufacture it or order eight latches yet.

**RECOMMENDATION:** ask the mechanical reviewer/fabricator to compare an external compression closure first, because the previously reviewed through-panel cutouts do not fit wholly within our assumed rim. This is a review priority, not a selected part or a claim that an external closure fits. Keep the filter's seating clamps separate from the access-door closure.

| Option | What changes in the design | Evidence needed before choosing |
|---|---|---|
| External compression latch and catch | Real brackets/supports outside the sealing strip; check how loads return into the housing | Exact body/catch drawing, working travel, closing force, opening sweep, mounting strength and material compatibility |
| Through-cover compression latch | New cutouts, sealed penetrations and internal catch space; relocate rather than copy the eight blocks | Exact cutout, grip definition, sealing detail, operating clearance, closing force and reviewed panel reinforcement |
| Retained removable cover with captive fasteners | Reviewed fastening/support arrangement; service may require tools | Captive hardware drawing, force-setting method, tightening sequence, stops, thread/joint strength and safe removal |

All options are OPEN. No count, bolt size, torque, gasket material or flange thickness is approved. Do not treat a material data sheet or latch static-load rating as an installed assembly approval.

## Existing geometry to send as context

**DETECTED IN DIGITAL STUDY; ALL DIMENSIONS ARE ASSUMPTIONS:**

- Inner clear access: 645 x 310 mm. Cover: 675 x 340 mm, assumed 2 mm thickness.
- Flange: 15 mm land, assumed 3 mm thickness. Gasket-space ring: outer 665 x 330 mm, inner 645 x 310 mm, assumed installed gap 3 mm.
- Inner housing-to-frame gap is only 6 mm. Outer casing study ID is 980 mm, outer access 700 x 380 mm.
- Remove the outer decorative panel before the inner cover. The previous straight cover-removal sweep is not a real latch-operating check.
- Cover-only steel-density calculation is about 3.60 kg, excluding hardware; material is not selected. Actual filter weight remains UNKNOWN.

References: [hatch CAD assumptions and service study](M05_HEPA_SERVICE_HATCH.md), [reviewed OEM drawings and gasket calculations](M05_HARDWARE_GASKET_REVIEW.md), `cad/parametric/hepa_service_hatch_m05.json`.

## Copyable request for the team to send

> We are developing a student air-cleaning tower for an indoor first test. We need help reviewing a removable, sealed HEPA access cover—not an immediate fabrication quote from our preliminary STEP. Our current opening is an assumed 645 x 310 mm and cover 675 x 340 mm. These dimensions can change after review.
>
> Please propose a closure/catch arrangement and supply dimensioned drawings, usable closing force and travel, panel/grip requirements, installation details and operating clearance. Please distinguish working/closing force from maximum static load. Also propose a compatible door gasket with its profile, free thickness/tolerance, compression limits and force-versus-compression data.
>
> Please review panel/flange stiffness, joint load paths, compression stops, safe supported removal and any sealed penetrations. We also need the filter supplier's separate seating-gasket and clamping instructions. Return exact part numbers, drawing revisions, price/lead time and limitations. Do not order or fabricate until the team approves the reviewed assembly.

**Not sent.** The team must review recipient and attachments before sending. Do not attach every historical CAD version: identify M05 as a space study, not an approved construction model.

## Load and tolerance worksheet for the reviewer

Record each case separately; do not simply sum every maximum regardless of direction or operating condition.

| Review case | Input status | Required result |
|---|---|---|
| Normal and worst credible door differential, fan operation/stoppage and relevant faults | UNKNOWN; earlier 500 Pa was an example, not a design limit | Actual pressure sign/range and applicable load cases; assess inward/outward loading |
| Gasket closing load | UNKNOWN; coupon-based estimate exists, not installed preload | Actual profile/contact area, full force curve, compression limits, repeat-use/aging conditions |
| Gravity and handling | Cover-only density estimate; full cover/filter masses UNKNOWN | Supported removal, drop prevention and allowable handling arrangement |
| Cover, flange, catch and mount reactions | UNKNOWN | Reviewed deflection/strength and seal-force distribution; choose gauge/grade/joints from this review |
| Tolerances | UNKNOWN | Stack of free gasket thickness, installed gap, stops, flatness, coating, manufacturing tolerance and load deflection |
| Operating motion and tools | Generic blocks only | Closed/open CAD positions, catch engagement, hands/tools and outer-panel removal sequence |

For each location, evaluate compression from actual free thickness and actual gap: `(free thickness - gap) / free thickness`. A negative value means a gap/no contact, not successful compression. Check all tolerance extremes against supplier limits. The historical 25% coupon value is not an approved target for a different gasket.

Pressure, seal preload, gravity and handling act through different paths. Mechanical reviewer must define applicable combinations and factors. No connection or thickness is sized here.

## Response and CAD acceptance sequence

Use [the response sheet](M05_SUPPLIER_RESPONSE.csv). Fill answers with units, exact supplier revision/source and reviewer outcome. UNKNOWN is intentional; do not replace it with an illustrative number merely to complete the sheet.

1. Team confirms intended service arrangement and provides exact component identities.
2. Supplier returns closure/catch and gasket data; mechanical reviewer accepts or rejects the proposed arrangement.
3. Rebuild only the chosen CAD branch using supplied dimensions. Preserve M05 and original studies.
4. Recheck cutouts/supports, gasket path, catches, hardware motion, tool access and supported filter/cover removal. Check both prefilter and HEPA access before release.
5. Reviewer completes strength/deflection/tolerance/load-path assessment and approves drawings/BOM. Coordinate removable-panel bonding and isolation with the electrical reviewer where applicable.
6. After authorized fabrication, inspect actual geometry/compression and verify installed sealing under an approved test procedure. Test acceptance criteria and method must be defined before testing. CAD fit does not prove leakage performance.

## Honest current status

Closure selected: NO. Supplier reply: NONE recorded. Mechanical sign-off: NONE recorded. Physical cover/seal test: NONE. Fabrication release: NO.

The next meaningful input is a supplier drawing/force curve and mechanical reviewer decision. More assumed latch blocks will not close this gap. Fan selection, frame/base design, electrical release and physical validation remain separate open tasks in [the six build gates](BUILD_REMAINING.md).
