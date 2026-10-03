# M03 — continuous frame around an independent inner housing

2 October 2026. FIT OPTION ONLY — NOT FOR FABRICATION.

## Simple idea

The round outer casing provides the appearance. Inside it, a separate square housing directs air through the filters. Continuous support posts stay outside that inner housing, so they do not need to pass through its filter seats. Fan loads can follow a continuous frame route instead of passing through split post-to-filter-plate joints.

This is a new comparison branch, not a selected final construction. The inner housing is intended to be sealed; actual joints, gaskets and leakage are not validated.

```text
Round outer casing (appearance / access)
  Continuous frame posts (support route)
    Independent inner housing:
      side intakes -> prefilter -> HEPA -> clean plenum -> transition -> fan -> outlet

Filter housing seat ears -> side rails -> posts -> future reviewed base
Fan -> future OEM-approved cradle -> frame -> future reviewed base
```

## What changed from the previous branches

- Existing circular filter bulkheads are omitted from this new assembly snapshot, not edited or deleted from R02.
- Two assumed square filter seats have integral side ears that rest on side rails at z445 and z640 mm.
- Four filter-level cross rails are omitted because they would intersect the inner housing walls. Continuous posts, bottom rails and fan-level rails are retained.
- The inner enclosure has lower intake walls, dirty-air walls, clean-air walls, bottom/top panels and two removable service-panel pieces.
- Eight inner intake openings are modeled: two per side, each 160 x 140 mm. Their total projected gross area is 0.1792 m2, matching the earlier gross opening sum. Two layers of openings and the intervening approach path introduce new losses; equal gross area does NOT establish equal airflow.

No guards, weather louvres, rated connections, mounting fasteners, base, feet or electrical enclosure are added. No new CFD or physical test was performed. Old flow predictions do not automatically transfer to this branch.

## Executed fit evidence

**DETECTED:** 36 valid solids in the combined snapshot; zero positive-volume pairwise clashes. FreeCAD native reopen and STEP reimport passed. Assumed lifted HEPA, lifted prefilter and retainer withdrawal sweeps clear with the relevant inner/outer panels removed and retainer clamps already removed. Eight nominal ear/side-rail contacts were calculated, each 1,225 mm2. Source hashes for R02, M04 and the continuous-frame CAD are unchanged.

**ASSUMPTIONS:** inner enclosure outer side 653 mm, 2 mm wall, clear side 649 mm; seats 5 mm thick; prefilter opening 562 mm; HEPA opening 563 mm. Housing walls have no approved material, stiffness or fabrication tolerance. Frame profiles remain the earlier assumed 35 x 35 x 3 mm geometry, not selected sections.

**TIGHT MARGINS, NOT APPROVED:** nominal housing-to-post side gap is only 6 mm. The 633 mm retainer has only 1 mm per side through the 635 mm inner service opening. Actual gasket/flange space, seal compression, paint/coating, deformation, tooling, fingers and supplier tolerances are NOT represented. Geometric clearance alone is insufficient; service-panel flange/latch geometry may require a different opening or larger housing/casing.

The square seat's side ears create a geometric bearing route, not a reviewed joint. They still need strength/deflection, shear/uplift restraint, fatigue/vibration and assembly review. The prefilter seat has no modeled supplier-approved gasket; washing and permitted orientation remain supplier questions. The existing HEPA gasket/retainer envelopes remain illustrative.

## Weight comparison — not yet optimized

Follow-on [grouped weight and service-envelope comparison](M03_WEIGHT_SERVICE_DECISION.md) preserves this CAD but identifies density-only hybrid options and a tolerance issue. Its wider/larger examples have NOT been modeled or approved.

Assuming every non-envelope material shape in this branch is steel at 7,850 kg/m3, the partial sum is **191.27 kg**. It excludes the fan, actual filters, gasket, base, all hardware and electrics. Adding the unselected 14 kg fan would give about 205.27 kg, still not total machine weight.

For comparison, the previous R02/M04 material subtotal plus segmented steel frame was about 183.70 kg, with similar major exclusions. The independent housing adds material while removing the circular bulkheads and four rails; it is not automatically lighter. Earlier 135.60 kg was only casing/plate/air-path material, without a frame, so comparing it directly as a whole-machine weight would be misleading.

**RECOMMENDATION:** retain this architecture as a useful fit candidate, but do not freeze its all-steel gauges. Review frame section sizing, formed/stiffened housing panels and lighter cosmetic cladding. Do not simply replace all steel with aluminium or thin every part without engineering checks. Structure, sealing and stability must be reassessed together.

## What remains before this branch can be built

1. Confirm exact fan/filter article numbers, mounting/installation drawings, masses, orientation and clean/loaded curves.
2. Resolve the narrow service/side margins with real flange, latch, clamp, gasket and tolerance geometry.
3. Design and review seat-ear/frame joints, fan cradle, base, feet and lifting/handling; calculate loads, stiffness and full mass/CG/stability.
4. Detail every pressure-boundary seam, door, seat, adapter and penetration; define installed leak testing. “Posts outside the housing” does not certify the assembled tower.
5. Update the complete pressure budget for the inner approach/intake and housing geometry, then evaluate the exact fan duty and commissioning measurements.

See [build remaining checklist](BUILD_REMAINING.md) for the whole project, including electrical release and physical validation.

## Files and repeatability

- `cad/parametric/independent_housing_m03.json`: assumptions, not supplier dimensions.
- `cad/packaging/AQI_M03_Independent_Housing_STUDY.FCStd`: combined shape snapshots; JSON/generator controls dimensional regeneration.
- `cad/packaging/AQI_M03_Independent_Housing_NOT_FOR_FABRICATION.step`: exchange study.
- `cad/packaging/M03_INDEPENDENT_HOUSING_AUDIT.json`: clashes, nominal contacts, sweep margins, mass and source hashes.

```powershell
& 'D:\Applications\FreeCAD 1.1.3\bin\python.exe' scripts/geometry/create_independent_housing_study.py
python -m unittest discover -s scripts/analysis -p 'test_independent_housing_audit.py'
```

Regeneration replaces these derived branch outputs; preserve manual edits first. Historical models remain untouched. All computed clearances, contacts and masses are digital study evidence, not physical measurements or release approvals.
