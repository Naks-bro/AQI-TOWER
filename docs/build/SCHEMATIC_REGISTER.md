# Plans and schematic register — R00

2 October 2026. All sheets below are **PRELIMINARY / NOT FOR FABRICATION OR WIRING**.

Open [Visual schematic pack](SCHEMATICS.html) in a browser. It contains selectable vector drawings and can be printed. These are new schematic concepts, not final FreeCAD assemblies. The existing mechanical, electrical, BOM and validation plans supply the accompanying requirements.

| Sheet | Content delivered | Still needed for release |
|---|---|---|
| M01-R00 | Round-shell / standard-panel concept section | Exact fan envelope, enclosure dimensions, CAD interference check and maintenance clearance |
| F01-R00 | Air path and static pressure tap plan | OEM filter orientation/curves, tap geometry and sensor range selection |
| E01-R00 | Power, monitoring and independent safety functions | Exact OEM wiring, device ratings, terminal/cable schedule and qualified electrical review |

## Layout recommendation for the first packaging study

Study a round metal housing with horizontal standard panel filters and upward flow. This uses the existing documented panel-filter candidates instead of inventing a cylindrical HEPA cartridge. It does not mean this option is finalized. The nozzle shape is not a Dyson copy; use a simple guarded outlet first and compare other outlets later.

For this orientation, the 593 mm square HEPA face has an 839 mm diagonal. A **950 mm internal diameter** is a working packaging assumption, not an approved device size: it leaves about 55.7 mm radial corner clearance before mounting hardware. If wall thickness is t, outer diameter is at least 950 + 2t mm, excluding doors/base. The square filter must sit in a sealed full-width bulkhead; otherwise air passes around its corners.

Candidate vertical zoning, all ASSUMPTIONS except filter depths:

| Zone | Height/depth mm | Status |
|---|---:|---|
| Base/support separation | 150 | Packaging assumption |
| Guarded intake/dirty plenum | 300 | Packaging assumption |
| Prefilter depth | 48 | Historical supplier candidate |
| Inter-stage/service gap | 150 | Packaging assumption; not approved access clearance |
| HEPA depth | 292 | Historical supplier candidate |
| Clean plenum/transition | 250 | Packaging assumption |
| Fan installation allowance | 600 | Placeholder; NOT an OEM fan dimension |
| Outlet/guard zone | 200 | Packaging assumption |
| Total study height | 1,990 | Not a manufacturing dimension; cassette frames/fasteners can increase it |

These heights describe modules only, not the geometry of the side-mounted electrical enclosure, mounting shelves, weather hood or removable service panels. Show each in actual CAD before accepting the envelope. Horizontal HEPA mounting/support must be approved by its supplier. Removal of a heavy filter requires a rated tray/support and sufficient external service space; a side door alone does not make it removable.

## Filter seal detail to develop (M03 next)

```text
dirty side -> filter media -> clean side
                   |
 filter frame -> OEM-compatible gasket -> flat sealing ledge
                   ^
     reviewed clamp applies specified gasket compression

Full-width airtight bulkhead surrounds the rectangular filter aperture.
Doors and panel seams also seal. No open route around the filter.
```

Gasket section, compression, clamping force, ledge flatness and fasteners remain UNKNOWN. Do not turn this sketch into an unreviewed workshop specification.

## What the electrical sheet means

Solid connections show functional power paths; dashed lines show monitoring/control information. These are not wire routes or terminal connections. Local safety functions act independently of the logger. The exact design may differ for an AC fan versus an EC fan; the historical KVO variant is unresolved. Speed adjustment, if fitted, uses its approved OEM controller/interface.

## Next sheets and order of work

M02 structure/base and mass/stability; M03 filter sealing; M04 fan support/guards; M05 service enclosure; M06 manufacturing sheets. E02 OEM-based power/control wiring; E03 terminal/cable schedule; E04 panel layout/bonding; E05 rating/coordination calculations; E06 commissioning record. Prepare after exact component drawings and faculty review; do not fill unknown ratings with guesses.

No outdoor dimensions, weather protection approval, bubble radius or tower spacing is established by these drawings. First indoor assembly is a test platform; outdoor design requires a separate review.
