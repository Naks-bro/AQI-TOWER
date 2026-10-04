# E03 — external control-module body layout

## CURRENT: E05 consolidated control fit

[Current build decision](D01_CURRENT_BUILD_DECISION.pdf), [corrected layout / input drawing](D01_E05_LID_CONTROLS_REVIEW.pdf), [editable current CAD](D01_E05_CURRENT_CONTROL_LAYOUT.FCStd), [STEP](D01_E05_CURRENT_CONTROL_LAYOUT.step), [coordinates](CURRENT_CONTROL_PLACEMENT.csv), [current fit evidence](CURRENT_CONTROL_CHECKS.json), [release gates](CURRENT_RELEASE_GATES.csv).

DETECTED DIGITAL: E04 cable-space conflicts are now closed without reducing any assumed reservations. Hub rotated 90 degrees in the panel plane, lower-left X=-15/Y=-70 mm; controller lower-left X=68/Y=-65 mm. Button centres X=-15/45/105, Y=55 mm. All six rear/tail volumes, three body and three service envelopes clear the exact OEM box; mounting-panel support excluded. Service volumes mutually clear; button-tail reservations no longer overlap them. Geometry script reopens 18 valid native objects and checks 18 STEP solids. Native R03M remains unchanged. Earlier E03/E04 files below are preserved, NOT the current placement.

ASSUMPTIONS unchanged: rear stack 40×40×55 mm, wire-tail depth 20 mm, body-only OEM envelopes, unselected carrier and actual connectors. UNKNOWN: actual assembly depth, bends/strain relief, supports and whole enclosure heat. Passing these reservations is not physical fit, wiring approval or proof that remaining protection/terminals fit. No drilling release.

Current OEM source: [2026 Schneider Digest section19](https://www.se.com/us/en/download/document/0100CT2401-SEC-19/), dated22 July2026, page19-42/table19.99, confirms ZBE1016/ZBE1026 low-power blocks and separates dusty P variants. It does not state minimum switching values. A2005 manufacturer catalogue mirror quotes5–24V/0.1–100mA for historical assemblies, but is not used to release today's parts because variant descriptions have changed. Current numeric limits remain UNKNOWN; do not silently substitute historical data. Private source copies are not redistributed.

Reproduce: `scripts/geometry/close_d01_control_layout.py` using existing FreeCAD Python, then report runtime `scripts/reports/build_d01_lid_controls.py --e05`, `scripts/reports/build_d01_closeout.py`, and `scripts/reports/build_shareable_delivery.py`. Required E03/E04 and private OEM model instructions follow. The combined technical PDF now puts current decision/E05/E02 pages first; historical drawings remain unchanged. Final review is consolidated; physical build release still depends on the five explicit gates in the decision PDF. No procurement, upload or physical test.

## Latest continuation: E04 closed-lid ordinary controls

[Two-page lid layout and input schematic](D01_E04_LID_CONTROLS_REVIEW.pdf), [editable FreeCAD](D01_E04_LID_CONTROL_ENVELOPES.FCStd), [STEP](D01_E04_LID_CONTROL_ENVELOPES.step), [candidate button parts](LID_CONTROL_PARTS.csv), [checks and source links](LID_CONTROL_CHECKS.json). E03 below remains the preserved body-layout snapshot. E04 extends that same module, not the tower geometry.

RECOMMENDATION: three spring-return buttons, START green ZB5AA3 + NO ZBE1016, STOP red ZB5AA4 + NC ZBE1026, RESET blue ZB5AA6 + NO ZBE1016; each with ZB5AZ009 collar. Ordinary software controls, **not emergency stop, isolation or protective restart**. Default firmware cannot run fans: all relays remain disabled. Prices and India stock UNKNOWN; no order placed.

VERIFIED: Schneider [BRU46063 installation instruction](https://download.se.com/files?p_Doc_Ref=BRU46063), page 2, specifies ordinary-head holes 22.3 mm with +0.4/-0 tolerance and panel range 1–6 mm. Proposed centres X=-15/45/105 mm, Y=0, provide 60 mm pitch. DETECTED: private Hammond STEP lid surfaces Z=46/50 mm at those centres, local thickness 4 mm. **No drilling release:** inspect delivered lid, head stack, torque, labels, sealing and all hardware first. Stock box/head ingress ratings do not rate this modified assembly.

ASSUMED rear envelopes: 40 × 40 × 55 mm beneath inner lid, with a further 20 mm wire-tail reservation. They clear all 24 OEM box solids and the three E03 body proxies; minimum combined reservation/body gap 6.03 mm. **Routing conflict remains:** STOP/RESET tail space overlaps both the hub and speed-controller assumed service spaces. JSON records actual overlaps; these are not hidden or counted as a full fit pass. Actual assembled head/collar/contact depth and cable bends remain UNKNOWN. Public CAD contains 18 original proxy objects, not OEM manufacturing geometry.

VERIFIED: [Harmony catalogue](https://iportal.se.com/Contents/docs/DIA5ED2121213EN.PDF) identifies ZBE1016/ZBE1026 as gold-flashed low-power contacts. Numerical minimum switching voltage/current at our conditions is UNKNOWN: designation alone does not release their use. Opta inputs draw 1.12 mA at 10 V per OEM datasheet; nominal 12 V / 8.9 kΩ gives 1.348 mA, a resistance screen only. Candidate input branches use I1/A0 START, I2/A1 healthy NC STOP, I3/A2 RESET; branch protection, contact terminal IDs, wire sizes, terminations and independent protection are unselected. Never substitute an ordinary STOP press for source disconnection.

Speed-access decision: retain the unmodified internal NA-FC1 and propose an **isolated preset**, not a live external knob. Disconnect the external source before accessing it, set the speed, close the box before operation. This is a planning sequence, not commissioning permission; run-down, access protection and source/isolation review remain required. Live speed-adjustment hardware is not designed.

Reproduce: existing FreeCAD Python runs `scripts/geometry/layout_d01_lid_controls.py` after E03; report runtime runs `scripts/reports/build_d01_lid_controls.py`. Checks 18 reopened native shapes and 18 exported STEP solids, exact-box clearance and unchanged native R03M hash. Private OEM CAD/PDFs stay ignored; no redistribution permission presumed. Access date: 5 October 2026. No physical tests or energization release.

[Dimensioned drawing](D01_E03_DIMENSIONED_CONTROL_LAYOUT.pdf), [FreeCAD envelopes](D01_E03_CONTROL_ENVELOPES.FCStd), [STEP envelopes](D01_E03_CONTROL_ENVELOPES.step), [placement coordinates](PLACEMENT.csv), [fit evidence](FIT_CHECKS.json). **Not for drilling, wiring or energization.**

FACT: the40mm tower reservation cannot accommodate the proposed Opta in normal DIN orientation. DETECTED: three OEM-sized body proxies and three assumed service volumes clear the downloaded Hammond STEP, excluding its support panel. Body separations65,85 and47mm. Native493-object tower CAD unchanged; physical prototypes0. **Body fit is not a completed control-panel fit:** PR1, fuse holders, terminals, buttons, actual cables and supports absent; do not assume these will fit the remaining space.

VERIFIED references: Hammond1554XA2GY nominal300x200x120mm, matching1554XPL panel285x185mm; Opta70x88.8mm front/61.1mm depth reservation; Noctua hub93x43x12.5mm, controller21x25x48mm. Panel page rounds thickness to2mm; supplied STEP models1.6256mm. Verify delivered thickness/fastener stack. ASSUMED Opta back at7.5mm rail crest;5mm hub/controller carrier lift, not selected hardware. Magnets alone not accepted installed retention. Reference Phoenix0801733 rail35x7.5mm,15x6.2 slots/25mm pitch; proposed125mm cut and4.5mm rail holes at X-122.5/-22.5,Y0 are NOT drilling release. Recommend obtainable equivalent standard cut piece, not the25-piece/50m catalogue pack. India stock/price UNKNOWN.

Critical finding: NA-FC1 dial/switch cannot be operated through a closed lid here. A reviewed enclosed access arrangement or different component is required. Do not run with an open box. No lid, cable or thermal-vent cutouts released.

## Reproduce / licensing

Use existing FreeCAD bundled Python. Download [exact Hammond STEP ZIP](https://www.hammfg.com/files/parts/stp/1554XA2GY.zip) into local `tmp/control_oem`, extract `1554XA2GY.stp` into `tmp/control_oem/step`, run `scripts/geometry/layout_d01_control_module.py`. Then run `scripts/reports/build_d01_control_layout.py` using the existing report runtime. Checks solid count/panel envelope, intersections and saved/reopened shapes; source hash recorded.

OEMSTEP/PDFs stay ignored local references: redistribution license not established. PublicCAD contains original simplified envelopes, not moulded geometry/panel contour/holes/gasket/threads. Not manufacturing geometry or permission to reproduce the OEM product. Same proposed D01 module, not an alternative tower branch.

Primary sources checked5 October2026:

- [Box drawing, rev28 February2020](https://www.hammfg.com/files/parts/pdf/1554XA2GY.pdf), [box page](https://www.hammfg.com/part/1554XA2GY), [panel drawing, rev1 November2019](https://www.hammfg.com/files/parts/pdf/1554XPL.pdf).
- [Opta datasheet, dimensions page16](https://docs.arduino.cc/resources/datasheets/AFX00001-AFX00002-AFX00003-datasheet.pdf).
- [Noctua hub](https://www.noctua.at/en/products/na-fh1/specifications), [speed controller](https://www.noctua.at/en/products/na-fc1/specifications).
- [Phoenix rail](https://www.phoenixcontact.com/en-us/products/din-rail-ns-35-75-perf-2000mm-0801733).

Remaining: selected protection/terminals and their volumes, retained rail/carriers, real entries/bends, closed-lid controls, heat rise, functional earth/metal panel treatment, module placement/retention, tower harness interface. External unmodified adapter stays outside; no mains inside proposal. Qualified acceptance and unpowered fit checks precede dummy-load commissioning. Stock IP68 does not rate our modified assembly; no protective requirement waived.
