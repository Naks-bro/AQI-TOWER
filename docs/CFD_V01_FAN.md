# V01 — Systemair KVO 250 / empty tower

## Objective

Run the supplied real six-point KVO 250 characteristic against the EMPTY Concept A air path. This is Phase 7 under the current brief. No filters, particles, water, power-system models or optimization are included. V00 remains the preserved PARTIAL / NON-CONVERGED imposed-flow reference.

## Takeover findings

The repository contradicts the handoff statement that V01_fan does not exist: it has an UNRUN 300 Pa totalPressure placeholder. That setup and its documentation are archived in `cfd/V01_fan/archive_placeholder/`. It is not executed or passed off as real fan evidence. The current task calls the real-fan case V01, superseding older references to a future V02.

## Fan and source data

Systemair KVO 250, article 2027, 230 V / 50 Hz, nominal 2480 rpm. Use `data/fans/systemair_KVO_250.json` unchanged. Rated electrical power is a catalog parameter, not a CFD power prediction. Source: Systemair KVO catalog hosted at the URL in that dataset. Previously audited Phase 6D values are accepted with their recorded uncertainty, not independently redigitized in Phase 7.

| Q m³/s (authoritative input) | Q m³/h (computed) | Fan static pressure Pa | Dataset confidence |
| --- | --- | --- | --- |
| 0 | 0 | 688 | Graph-digitized ±20 Pa |
| 0.1042 | 375.12 | 640 | Graph-digitized ±20 Pa |
| 0.2083 | 749.88 | 480 | Graph-digitized ±15 Pa |
| 0.254 | 914.4 | 388 | Confirmed numeric source |
| 0.3333 | 1199.88 | 205 | Graph-digitized ±15 Pa |
| 0.417 | 1501.2 | 0 | Confirmed numeric source |

Use linear interpolation in Q, not a polynomial fit or rescaled velocity curve. The original rounded m³/h labels are not substituted for the supplied m³/s inputs. Numerical source points are not uncertainty-free measurements: only their digitization uncertainty is omitted in the dataset. Source hashes and exact points are recorded in `fan_implementation.json`.

## Fan representation and pressure convention (before running)

A lumped terminal suction fan is applied at existing AIR_OUTLET. No blades or new cells are necessary. The installed OpenFOAM 14 `fanPressure` source was inspected: for outward flow it sets static patch pressure to p0 minus its curve value, with a kinetic correction only during backflow. Feeding the catalog fan-static curve directly into it would silently confuse pressure definitions in this nonuniform discharge. The old claim that OpenFOAM universally requires at least five curve points is a project sampling rule, not a software minimum.

Fan static pressure Ps equals fan total rise minus the fan discharge velocity pressure, equivalently discharge static pressure minus suction total pressure. See [AMCA pressure-curve explanation](https://www.amca.org/educate/articles-and-technical-papers/amca-inmotion-articles/straightening-out-fan-curves.html) and [ASHRAE Fans, pressure definitions](https://handbook.ashrae.org/Handbooks/S24/IP/S24_Ch21/S24_Ch21_ip.aspx).

ASSUMPTION: the external fan discharges at atmospheric static pressure (zero gauge), and an ideal adapter connects the tower outlet to its suction without additional total-pressure loss. Thus the required suction total pressure is -Ps(Q). Fan outlet diameter is 250 mm, area 0.049087 m²; tower outlet is 0.125 m². These are NOT treated as the same area. Physical transitions and their losses remain unmodelled. In this terminal formulation the fan discharge kinetic term cancels algebraically between fan total rise and free discharge; it must not be added again to Ps.

OpenFOAM `codedFixedValue` supplies a uniform static suction pressure on AIR_OUTLET:

    Q = sum(phi_outlet) [m³/s, outward positive]
    K = sum(phi_outlet * |U|²/2) / Q [m²/s²]
    p_kinematic = -Ps(Q)/rho - K, rho = 1.20 kg/m³

Consequently the signed-flow-weighted patch total pressure is -Ps(Q) at a fixed point. This is an ideal uniform-static-pressure suction boundary, not a local blade or actuator-disk model. Signed flux weighting accounts for any backflow; Q must remain positive. Q outside [0,0.417] is clamped for startup stability and flagged in the solver log; a final clamped/out-of-range operating point is unacceptable.

The pressure law is generated directly from the JSON and compiled using OpenFOAM's supported coded boundary facility. A 0.1 numerical relaxation factor on the scalar suction head is applied once per outer iteration to damp fan/system feedback; it does not change the converged curve. Log `closure_Pa` measures the relaxed law error. Require small late-run closure before interpreting an operating point. No desired Q or inlet speed is enforced.

## Fan location / geometry

Existing AIR_OUTLET plane: X=0.700 m, Y=0.150–0.650 m, Z=1.600–1.850 m. Air travels in +X across this plane into the idealized fan, then discharges to ambient outside the model. This is the clean-side / pull-through position requested where practical. It does not make a claim that air is clean in this empty model. The fan is a boundary element, so no internal fan zone, baffle or CAD alteration is required.

The ten original cell zones remain empty air. Native CAD and all V00 files are read-only inputs to this phase.

## Mesh

Reuse V00 `constant/polyMesh` byte-for-byte; record source/destination hashes. Original cells 57,645; planned new cells 57,645. Volume 0.424 m³. No refinement or remeshing. Re-run all topology and geometry checks before solving. Geometric mesh quality does not establish discretization accuracy or eliminate numerical causes of residual oscillation.

## Boundary conditions / solver

AIR_INLET: totalPressure p0=0 gauge (ambient reservoir), pressureInletOutletVelocity. AIR_OUTLET: KVO suction law above, pressureInletOutletVelocity. WALLS: unchanged noSlip, pressure zeroGradient, smooth-wall functions. No fixed inlet flow remains; initial velocities are only starting guesses. Retain V00's fixed inlet k=0.00375 m²/s² and epsilon=0.000834 m²/s³ as documented turbulence assumptions; actual turbulence is unknown.

OpenFOAM Foundation 14 incompressibleFluid / steadyState / kEpsilon. nu=1.5e-5 m²/s, rho=1.20 kg/m³ for pressure reporting. Start from V00's best numerical settings: SIMPLEC, p relaxation 0.3, U 0.7, k/epsilon 0.5, bounded linearUpwind U and limitedLinear turbulence. Initial run maximum 3000 iterations. No new software required.

## Convergence / diagnostic plan

Require initial equation residuals p<1e-5 and U/k/epsilon<1e-6, mass imbalance <0.1%, late-100-iteration Q range <0.1% of mean, and fan boundary closure <0.1 Pa. Inspect trends rather than a single residual. If stalled, one bounded numerical adjustment/run is allowed and retained separately; no endless tuning. Periodic steady-iteration residuals are evidence of solver nonconvergence, NOT proof of physical unsteadiness. The inherited V00 interpretation remains archived; that particular causal claim is unverified without further tests.

## Operating point / results plan

Extract actual conservative patch phi, pressure means, signed flux-weighted total pressure, cell speeds, region reverse-flow indicators and cross-section statistics. Compare the final fan-static pressure and Q against the unchanged six-point curve. Do not equate inlet-minus-outlet static pressure directly with fan static head: kinetic energy differs between sections. Compare with V00 iteration 6000 only, noting different driving boundaries and incomplete baseline convergence.

### Actual outcome

The 4000-iteration result is PARTIAL / NON-CONVERGED: Q=0.409927 m³/s (1475.74 m³/h), curve Ps=17.3232 Pa, independently integrated equivalent head=17.3257 Pa. Tower static difference=32.4614 Pa; peak cell speed=6.5313 m/s, volume mean=1.7435 m/s. Riser reverse-volume indicator=23.12%. Final mass imbalance=6.84e-8%; late-100-iteration flow range=0.000651%. Initial p/U residuals remain above criteria. The diagnostic continuation exited cleanly (code 0), validating the library-retention workaround. No further tuning was performed.

Interpretation: PROMISING WITH GEOMETRY ISSUES, not a final fan or purifier operating point. Full airflow, pressure, velocity, recirculation, V00 comparison, uncertainties and limitations are in `results/CFD_V01_FAN_RESULTS.md`. The independently extracted metrics and verification checks are in `results/CFD_V01_FAN/`.

## Uncertainty / limitations / interpretation

### Execution notes

Two setup-only compilation errors were resolved before any flow iterations: OpenFOAM dynamic-code build options require a single continued options line, and Foundation 14 uses individual field headers rather than the older `fvCFD.H` umbrella header. Their logs are retained as `setup_compile_error.log` and `setup_header_error.log`; no software installation was needed.

The first physical run uses the documented settings and is retained in `logs/foamRun_kvo.log` with its inputs in `logs/initial_kvo_setup/`. It develops a small residual cycle while Q and fan-law closure are stable. The single diagnostic continuation tightens all linear solver absolute tolerances to 1e-10 and relative tolerance to zero, leaving relaxation, discretization and all physics unchanged. This tests incomplete inner solves as a numerical cause; it does not assume the residual cycle proves a physical oscillation. The diagnostic is bounded at iteration 4000 (1000 additional iterations; reduced from an initially allowed 6000 end limit), with the original residual criteria unchanged.

The initial run wrote complete iteration-3000 fields and printed End, then raised a segmentation fault in coded-boundary destruction (exit code 139 inside WSL). It is NOT recorded as a clean run. The continuation explicitly preloads the exact compiled boundary library via controlDict `libs` so it remains loaded while the solver destroys its fields. This is a software-lifetime workaround, not a physics or fan-curve change. Preserve the compiled library and generated source under `dynamicCode/`; if regenerating on another machine, compile it there and update the matching path before using that workaround.

### Reproduction

Run `prepare_kvo250_v01.py` with Windows Python, then `run_kvo250_v01.sh` in WSL Ubuntu. The preparation script protects an existing real-fan run and archives the old placeholder automatically. For exact initial-run reproduction in a separately copied project, use `logs/initial_kvo_setup/` dictionaries before launching. The working case's final settings may instead describe the documented continuation. The continuation script never rebuilds the mesh. `analyze_kvo250_v01.py` runs with WSL `pvpython --force-offscreen-rendering`; it refuses an unfinished solver log and writes only `results/CFD_V01_FAN/`.

No reproduction step is permission to delete or reset the preserved cases; use a separate working copy if rerunning from zero.

Graph-digitization ±15–20 Pa applies at the marked knots; interpolation uncertainty is additional and not statistically characterized. The ideal adapter, uniform suction pressure, inlet turbulence, coarse mesh and RANS wall treatment are substantial modelling limitations. No detailed fan wake, swirl, blade passage, installation effect, stall, acoustic behaviour, mechanical fit or electrical power is predicted. The outlet-velocity-pressure correction is explicitly included in the boundary mapping, not silently ignored.

Filters are absent; actual filter, prefilter, biochar and water-stage losses are unknown. There is no final CAD validation or physical test. V01 cannot establish final system CADR, AQI reduction, filtration efficiency or final fan selection. No Phase 8 work is authorized by this run.
