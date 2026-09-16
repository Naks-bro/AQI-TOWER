"""Prepare cfd/FILTER_H13/CASE_M_SEALED — Phase 10B bypass-sealed case.

Copies CASE_M configuration and adds a wall baffle that blocks the
unintended dirty-to-clean connection at z=850 mm, x=260-305 mm.
Does NOT rerun CFD. Does NOT modify the original CASE_M.
Does NOT change filter resistance, fan curve, or any other physics.

Run with plain Python (not FreeCAD, not pvpython):
    python scripts/simulation/prepare_case_m_sealed.py
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "cfd" / "FILTER_H13" / "CASE_M"
DEST   = ROOT / "cfd" / "FILTER_H13" / "CASE_M_SEALED"

# ---------------------------------------------------------------------------
# Guard
# ---------------------------------------------------------------------------
if DEST.exists():
    raise SystemExit(f"CASE_M_SEALED already exists at {DEST} — remove it first if you want to recreate it.")
if not SOURCE.exists():
    raise SystemExit(f"Source CASE_M not found at {SOURCE}")

print(f"Creating {DEST.relative_to(ROOT)} from CASE_M...", flush=True)

# ---------------------------------------------------------------------------
# Copy case structure — skip solved timesteps and regenerated polyMesh
# ---------------------------------------------------------------------------
DEST.mkdir(parents=True)

# 0/ — initial conditions (no solved data)
shutil.copytree(SOURCE / "0", DEST / "0", dirs_exist_ok=False)

# constant/ — everything EXCEPT polyMesh (will regenerate via blockMesh)
(DEST / "constant").mkdir()
for p in (SOURCE / "constant").iterdir():
    if p.name == "polyMesh":
        continue    # will be regenerated
    if p.is_file():
        shutil.copy2(p, DEST / "constant" / p.name)
    elif p.is_dir():
        shutil.copytree(p, DEST / "constant" / p.name)

# system/ — all files
shutil.copytree(SOURCE / "system", DEST / "system", dirs_exist_ok=False)

# dynamicCode/ — compiled coded BC library
shutil.copytree(
    SOURCE / "dynamicCode",
    DEST / "dynamicCode",
    ignore=shutil.ignore_patterns("lnInclude"),
    dirs_exist_ok=False,
)

# logs/
(DEST / "logs").mkdir()

# .foam file
(DEST / "CASE_M_SEALED.foam").touch()

print("  Files copied.", flush=True)

# ---------------------------------------------------------------------------
# Modify createBafflesDict: add bypass-seal baffle + use relaxation 0.005
# ---------------------------------------------------------------------------
baffles_path = DEST / "system" / "createBafflesDict"
original = baffles_path.read_text(encoding="utf-8")

# Change relaxation 0.2 → 0.005 for the filter baffles
# (avoids the multi-phase solver startup used in CASE_M)
modified = original.replace("relaxation 0.2;", "relaxation 0.005;")

bypass_seal_entry = """
    bypassSeal
    {
        // Phase 10B: blocks the open dirty-to-clean connection at the
        // z=0.850 m horizontal interface in the x=0.260-0.305 m overlap
        // zone where INTERSTAGE_02 / STAGE_03 (dirty, z<0.85) face
        // CLEAN_RISER (clean, z>0.85) with no separating wall.
        // origin and span in metres; plate is horizontal (span z=0).
        type surface;
        surface plate;
        origin (0.260 0.150 0.850);
        span (0.045 0.500 0.0);
        owner
        {
            name BYPASS_SEAL_DIRTY;
            type wall;
            patchFields
            {
                p { type zeroGradient; }
                U { type noSlip; }
                k { type kqRWallFunction; value uniform 0.00375; }
                epsilon { type epsilonWallFunction; value uniform 0.000834; }
                nut { type nutkWallFunction; value uniform 0; }
            }
        }
        neighbour
        {
            name BYPASS_SEAL_CLEAN;
            type wall;
            patchFields
            {
                p { type zeroGradient; }
                U { type noSlip; }
                k { type kqRWallFunction; value uniform 0.00375; }
                epsilon { type epsilonWallFunction; value uniform 0.000834; }
                nut { type nutkWallFunction; value uniform 0; }
            }
        }
    }
"""

# Insert before the closing brace of the baffles { ... } block
close = modified.rfind("\n}")
if close < 0:
    raise RuntimeError("Cannot locate closing brace in createBafflesDict")
modified = modified[:close] + bypass_seal_entry + modified[close:]

baffles_path.write_text(modified, encoding="utf-8")
print("  createBafflesDict updated: bypassSeal added, relaxation set to 0.005.", flush=True)

# ---------------------------------------------------------------------------
# Tighten fvSolution: use the already-known optimal relaxation from the start
# (CASE_M used fvSolution.initial then switched; SEALED starts tight)
# ---------------------------------------------------------------------------
# The current system/fvSolution in the copied case already has tight settings
# from Phase 9 (it was copied from CASE_M which ended on tight settings).
# No change needed — verify it has SIMPLEC and consistent=yes.
fvsol = (DEST / "system" / "fvSolution").read_text(encoding="utf-8")
assert "consistent" in fvsol, "fvSolution missing SIMPLEC consistent setting"
print("  fvSolution: SIMPLEC settings confirmed, no change needed.", flush=True)

# ---------------------------------------------------------------------------
# controlDict: update caseName references and set endTime
# ---------------------------------------------------------------------------
ctrl_path = DEST / "system" / "controlDict"
ctrl = ctrl_path.read_text(encoding="utf-8")
ctrl = ctrl.replace("CASE_M", "CASE_M_SEALED")
# Use endTime 5000 (same as CASE_M final run)
ctrl = re.sub(r"endTime\s+\d+\s*;", "endTime 5000;", ctrl)
ctrl_path.write_text(ctrl, encoding="utf-8")
print("  controlDict: endTime=5000, caseName=CASE_M_SEALED.", flush=True)

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("\nCASE_M_SEALED prepared at:")
print(f"  {DEST}")
print()
print("Next steps (run in WSL from AQI-TOWER root):")
print("  cd /mnt/d/DUDE/AQI-TOWER/cfd/FILTER_H13/CASE_M_SEALED")
print("  blockMesh 2>&1 | tee logs/blockMesh.log")
print("  checkMesh 2>&1 | tee logs/checkMesh.log")
print("  createBaffles -overwrite 2>&1 | tee logs/createBaffles.log")
print("  foamRun 2>&1 | tee logs/foamRun_baffleRelax0005.log")
