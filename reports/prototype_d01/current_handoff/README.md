# START HERE — one current D01 review handoff

**Continued by [package1 R03M mechanical](../mechanical_package/README.md).** That assembly supersedes R02G mechanical details below; this R02G handoff is preserved as historical evidence. Use R03M panel/base/guard files and fastener lengths together. No fabrication release in either revision.

03 October 2026. **Design review only. NOT construction-ready. Physical prototypes:0.**

Open [AQI_D01_CURRENT_REVIEW_PACKAGE.pdf](AQI_D01_CURRENT_REVIEW_PACKAGE.pdf). It combines a plain-language project handoff with current pressure/electrical boundaries, three remaining build gates and10 panel drawings taken directly from the current CAD. It replaces the need to assemble an understanding from earlier revision PDFs. Historical evidence remains preserved.

[Download the current review bundle](AQI_D01_CURRENT_REVIEW_HANDOFF.zip). It preserves project-relative paths and includes current CAD, PDF, panel DXFs, inventory, checks and the three current-generation scripts. MANIFEST.json records hashes. It is not the full project history or a released fabrication pack. Required CAD/runtime dependencies are not bundled.

## Current authority

- [R02G integrated FreeCAD assembly](../r02_guards/D01_R02G_ASSEMBLY.FCStd), [STEP](../r02_guards/D01_R02G_ASSEMBLY.step): geometry authority; no assembly change in this handoff.
- [Ten panel DXFs](panel_DXF_REVIEW_ONLY/): current CAD-face extraction, mm, no kerf compensation or released tolerances/materials. Do NOT send directly for cutting. Other brackets/guards/hardware are not covered by these flat-panel files.
- [Complete CAD object inventory](CAD_PART_INVENTORY.csv):245 rows, including reservations, simplified envelopes and inherited notes. This is NOT a complete purchase list.
- [OEM references and missing items](COMPONENT_AND_MISSING_ITEMS.csv): covers unmodeled controls, missing hardware, seals and services. Combined with the inventory, this exposes omissions rather than silently treating them as finished parts.
- [Current pressure CSV](CURRENT_PRESSURE_BUDGET.csv), [calculation evidence](CURRENT_PRESSURE_BUDGET.json).
- [Whole-assembly audit](assembly_audit.json), [panel geometry](current_panels.json), [three build gates](BUILD_GATES.csv).

## What changed in this pass

DETECTED: earlier deliveries were fragmented and delta-only audits did not constitute a single whole-assembly handoff. This pass checks the complete current assembly, extracts all10 flat panels from actual BRep faces, verifies face-area times thickness against part volume, and inventories every object.29,116 modeled part pairs pass the0.05 mm3 clash threshold;774 pairs involving reservations or guard-to-guard seams are excluded. Native/STEP checks were already completed for R02G; no new physical result is claimed. The source CAD hash is recorded and unchanged.

New current-geometry pressure budget includes the350x270 mm openings and a separate reducer-path sensitivity. At300 total m3/h, each filter sees150 m3/h and the K=1 scenario leaves14.61 Pa filter allowance after assumed losses. This is a balance allowance, NOT an operating target approved by the user, actual filter resistance, performance margin or measured airflow. At400 total, the same assumptions leave negative allowance even before adding a filter. Eight arithmetic checks pass. No filter curve was invented and no old R01 flow prediction is presented as R02G performance.

## When does the preparation end?

There are three closure packages, not a commitment to one chat turn per small feature:

1. **Mechanical (assistant prepares; still OPEN):** finish guard face/corner/rivet joins, remaining cabinet/fan/M5 fastening stacks, sealing/compression details, cable housing/entry, and load/access/stability checks. Some quantities, materials and strengths are still unknown. Selected-component dimensions and qualified physical fit/review are needed before release.
2. **Electrical (assistant prepares; still OPEN):** rated protective isolation/restart arrangement, exact connectors/cables/enclosure and installation checks. The present OEM speed-control chain does NOT implement the stated protective functions. Qualified review and commissioning remain necessary, not delegated to an unconfirmed friend.
3. **Performance evidence (still OPEN):** actual filter resistance and seal behavior, then installed flow/power/noise and controlled indoor particle trials. Where manufacturers do not publish the needed data, measurements of real parts cannot be replaced with internet research. No supplier-contact task is being assigned to the user.

Gates1/2 and actual component fit govern safe construction/energization; gate3 governs what performance can be claimed. A safe test assembly may be built to discover performance only after its mechanical/electrical release, not by declaring unknown performance a safety approval. Internet/public evidence work may continue, but repeated cosmetic CAD revisions are not progress on the missing test evidence.

No exact number of days is defensible: no approved parts order, confirmed stock/delivery, fabricator/reviewer booking or test location exists. Do not confuse assistant computation time with supply, fabrication and test time. Funding should be staged for samples, confirmed parts, fabrication, review/commissioning and measurement. No prices or total cost fabricated.

## Sources / assumptions / unknowns

- FACT: indoor first test, funding but no college lab, eventual outdoor goal, no physical prototype.
- DETECTED: saved R02G geometry, public OEM references and archived curve numeric data.
- RECOMMENDATION: finish one supervised indoor particulate demonstrator; keep outdoor/weather/solar/gas/water and network work outside this first build release.
- ASSUMPTION: equal parallel fan/filter flows, full2800 rpm, density1.2 kg/m3, guard active area300x300 mm at40% open, plenum K1.5, guard K1.5 each, fan-aperture-based installation allowance K1, reducer K0.5/1/2. Added reducer loss may overlap the existing plenum allowance; none of these K values is validated. No bypass assumed. No physical uncertainty band implied.
- UNKNOWN: selected filter clean/loaded curve and frame landing, installed fan performance, seal compression/leakage, materials/strength, mass/tipping, protective electrical implementation, procurement and test outcomes.

Source references (previously accessed03 October2026): [ARCTIC numeric workbook](https://support.arctic.de/products/p14-max/techdocs/P14%20Max%20-%20PQ%20Curve%20for%20CFD.XLSX), [ARCTIC support](https://support.arctic.de/p14-max), [IKEA STARKVIND104.633.30](https://www.ikea.com/in/en/p/starkvind-filter-for-particle-removal-10463330/), [Noctua NV-PS1](https://www.noctua.at/en/products/nv-ps1), [NA-FH1](https://www.noctua.at/en/products/na-fh1/specifications), [NA-FC1 total-current FAQ](https://www.noctua.at/en/support/faqs/how-many-fans-can-i-connect-to-the-na-fc1-controller).

The IKEA part is intended by its OEM only for STARKVIND. This custom integration is experimental, not endorsed. No HEPA/MERV rating is assigned to our current assembly. ARCTIC numeric/brochure discrepancies remain unresolved; the numeric curve is not averaged with the brochure. Hardware dimensional sources are in the preserved R02H/R02G READMEs. OEM material is evidence, not an open-source manufacturing licence. The handoff ZIP does not redistribute OEM downloads.

The aqi-build-review skill drove whole-assembly verification, same-flow pressure accounting, and the explicit separation of digital work from physical release. No purchase, install, contact or public publishing occurred.

## Reproduce

```powershell
& 'D:\Applications\FreeCAD 1.1.3\bin\python.exe' scripts/geometry/audit_d01_current.py
& 'C:\Users\G15 5530\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts/analysis/d01_current_pressure_budget.py
& 'C:\Users\G15 5530\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts/reports/build_d01_current_handoff.py
```
