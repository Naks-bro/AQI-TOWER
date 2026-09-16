# Development Environment

Inspection date: 2026-09-05  
Workspace: `D:\DUDE\AQI-TOWER`

## Status Labels

- **FACT:** A directly observed project or system condition.
- **DETECTED:** The item was found and, where possible, its version was queried successfully.
- **RECOMMENDATION:** A proposed future action; it is not evidence that the action has occurred.
- **UNKNOWN:** The item could not be safely or conclusively verified.
- **NOT INSTALLED:** The item was not found in the inspected Windows command paths, application records, common installation folders, or relevant Ubuntu environment.

## Computer

| Item | Status | Recorded value |
| --- | --- | --- |
| OS | DETECTED | Microsoft Windows 11 Home Single Language, 64-bit; version 10.0.26200, build 26200 |
| CPU | DETECTED | 13th Gen Intel(R) Core(TM) i7-13650HX; 20 logical processors |
| RAM | DETECTED | 16,849,256,448 bytes (15.69 GiB) |
| Discrete GPU | DETECTED | NVIDIA GeForce RTX 3050 6GB Laptop GPU; 6,144 MiB dedicated memory; driver 596.08 |
| Integrated GPU | DETECTED | Intel(R) UHD Graphics; driver 32.0.101.7085 |
| Integrated GPU memory | UNKNOWN | Windows reports shared/adapter memory in a way that is not a reliable dedicated-memory measurement |

## Storage

Values are the free space observed during the Phase 1 inspection and will change over time.

| Drive | Volume | Total | Free | Status |
| --- | --- | ---: | ---: | --- |
| `C:` | OS | 337.93 GiB | 60.04 GiB | DETECTED |
| `D:` | New Volume; project workspace | 298.34 GiB | 170.92 GiB | DETECTED |
| `E:` | New Volume | 293.46 GiB | 96.94 GiB | DETECTED |

## Requested Software

| Software | Status | Version or note |
| --- | --- | --- |
| Python | DETECTED | 3.13.1 on Windows |
| Git | DETECTED | 2.51.0.windows.1 |
| Node.js | DETECTED | v24.19.0 on Windows |
| npm | DETECTED | 11.9.0 on Windows |
| FreeCAD | DETECTED | 1.1.3, revision 20260725; installed at `D:\Applications\FreeCAD 1.1.3` during Phase 4 with explicit approval |
| OpenFOAM | DETECTED | Foundation 14, Ubuntu package 20260724; `/opt/openfoam14` in WSL Ubuntu; installed in Phase 5 |
| CfdOF | NOT INSTALLED | No CfdOF workbench found; unnecessary for the selected direct FreeCAD-to-blockMesh workflow |
| ParaView | DETECTED | 5.11.2; Ubuntu package 5.11.2+dfsg-6build5, including python3-paraview/pvpython; installed in Phase 5 |
| Three.js / Node environment | DETECTED / NOT INSTALLED | Node.js and npm are available; the project has no `package.json`, and Three.js is NOT INSTALLED locally or globally |

## Other Relevant Software Detected

| Software | Status | Version or note |
| --- | --- | --- |
| WSL | DETECTED | WSL 2; default distribution is Ubuntu |
| Ubuntu | DETECTED | Ubuntu 24.04.4 LTS under WSL 2 |
| Python in Ubuntu | DETECTED | 3.12.3 |
| Git in Ubuntu | DETECTED | 2.43.0 |
| Node.js in Ubuntu | DETECTED | v20.20.0 |
| npm in Ubuntu | DETECTED | 11.10.1 |
| Visual Studio Code | DETECTED | 1.134.0 |
| CMake | DETECTED | 3.27.1 |
| GCC / MinGW-w64 | DETECTED | 13.2.0 |
| Clang / MinGW | DETECTED | 16.0.6 |

## Project Environment Facts

- **FACT:** `D:\DUDE\AQI-TOWER` is not currently a Git repository.
- **FACT:** No Python virtual environment was created in Phase 1.
- **FACT:** No Node project was initialized in Phase 1.
- **FACT:** No software was installed or purchased in Phase 1.
- **FACT:** Pre-existing draft files under `cad/parametric/` and `scripts/` were preserved and not executed.
- **UNKNOWN:** The inspection was targeted at relevant engineering and development tools; unrelated applications and software stored in nonstandard locations were not exhaustively inventoried.

## Phase 1 Recommendation Boundary

- **RECOMMENDATION:** Use the detected Python and Git installations for documentation and lightweight scripts.
- **RECOMMENDATION:** FreeCAD is the next installation to consider, but installation requires explicit approval.
- **RECOMMENDATION:** Defer OpenFOAM, ParaView, CfdOF, and Three.js setup until their corresponding development phases.

## Phase 4 Update

- **DETECTED:** FreeCAD 1.1.3 and its command-line executable both launch from `D:\Applications\FreeCAD 1.1.3\bin`.
- **FACT:** The official Windows x86_64 installer matched its published SHA-256 digest and had a valid signature from The FreeCAD project association AISBL before installation.
- **FACT:** OpenFOAM, ParaView, CfdOF, and Blender were not installed during Phase 4.

## Phase 5 Reinspection and Installation

Inspection/install date: 2026-09-05. The Phase 1 recommendations above are historical, not current installation instructions.

| Item | Status | Phase 5 observation |
| --- | --- | --- |
| Windows | DETECTED | Windows 11, version 10.0.26200.9278 reported by WSL |
| WSL | DETECTED | 2.6.3.0; kernel 6.6.87.2-1; WSLg 1.0.71; Ubuntu uses WSL 2 |
| Ubuntu | DETECTED | 24.04.4 LTS (Noble) |
| Available logical CPUs | DETECTED | 20 visible in Ubuntu; V00 uses one solver process to limit memory/coordination overhead |
| Windows visible RAM | DETECTED | 16,454,352 KiB total; 1,508,832 KiB free at pre-install inspection; availability varies |
| WSL RAM | DETECTED | 7.6 GiB total; approximately 6.8 GiB available before install and 6.5 GiB during the run; 2.0 GiB swap |
| C: physical disk | DETECTED | 60,286,324,736 bytes free after install (about 56.15 GiB) |
| D: project disk | DETECTED | 180,654,436,352 bytes free during run (about 168.25 GiB) |
| E: physical disk | DETECTED | 104,086,667,264 bytes free (about 96.94 GiB) |
| WSL virtual filesystem | DETECTED | Reported about 938 GiB available before install; sparse virtual capacity is NOT guaranteed physical space |
| FreeCAD | DETECTED | 1.1.3; native V00 opened and inspected successfully with its bundled Python |
| OpenFOAM/ParaView before install | NOT INSTALLED | No commands or matching Ubuntu packages detected |

**FACT:** Following the Phase 5 installation authorization, the official signed OpenFOAM Foundation Ubuntu Noble repository was added. Its signing key was downloaded from `https://dl.openfoam.org/gpg.key`; the source is `http://dl.openfoam.org/ubuntu noble main`. Package signatures were enforced by apt; no authentication or sudo configuration was changed. Installation used WSL's supported root-user invocation; simulations use the normal Ubuntu user.

Explicit package request: `apt-get -y --no-install-recommends install openfoam14 paraview python3-paraview`. ParaView's Python support is needed for reproducible field extraction and images. Optional recommended packages were suppressed: no CfdOF, Blender, Ansys, standalone Gmsh application, or Three.js was installed. Required shared libraries include libgmsh and MPI dependencies; these are package dependencies, not additional selected workflows.

The package transaction reported 177 newly installed packages, 14 dependency upgrades, 0 removals, 440 MB downloaded and 2114 MB additional installed size. Its complete package/version record is `cfd/V00/logs/installation.log`. Ordinary apt package-index refreshes also updated metadata for the distro's pre-existing repositories; no unrelated full-system upgrade or autoremove was performed.

**DETECTED:** `foamVersion` returned OpenFOAM-14; the solver and mesher executed successfully. `pvpython --version` returned ParaView 5.11.2. `dpkg-query` confirmed openfoam14 20260724 and paraview/python3-paraview 5.11.2+dfsg-6build5. Python scientific/plotting libraries are installed as dependencies of this Ubuntu visualization stack, not into the Windows Python environment.

**FACT:** Software lives in the existing Ubuntu filesystem; all AQI case inputs, logs, fields and images live on D: under this project. The WSL distribution was not relocated. No shell startup files were edited; the run script sources `/opt/openfoam14/etc/bashrc` explicitly.

Official compatibility and installation reference: [OpenFOAM 14 Ubuntu packages](https://openfoam.org/download/14-ubuntu/).
