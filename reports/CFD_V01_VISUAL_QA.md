# V01 figure contract and QA

Delivery: user-requested local static technical figures, not a dashboard. Evidence: actual iteration-4000 OpenFOAM fields, actual solver logs and unchanged six-point fan JSON.

| Figure | Analytical question / encoding | Caveat |
| --- | --- | --- |
| velocity_streamlines.png | Where does speed concentrate? Central Y=0.4 m scalar section with actual inlet-seeded trajectories | Interpolated points; closed pockets need separate reverse-flow metrics |
| pressure_section.png | What gauge pressure field accompanies suction? Pa on same plane | Not absolute or hydrostatic pressure |
| stage03_cross_section.png | How uneven is stage through-flow? Signed Ux, symmetric diverging scale, X=0.305 m | Empty stage, not filter velocity validation |
| fan_curve_operating_point.png | Where is the computed point on the source curve? Original knots, stated digitization bars, actual CFD marker | Q² dotted guide is not a CFD sweep; error bars omit unprovided measurement uncertainty |
| residual_history.png | Were convergence targets met? 4000 actual iteration rows, logarithmic residuals and criteria | Nonlinear initial residuals, not linear-solver final values |

Palette: sequential continuous map for speed; symmetric diverging map for signed stage velocity; pressure uses a labelled continuous map; residuals use explicit blue/gold plus distinct line styles and neutral threshold lines. Continuous scientific colormaps are intentional exceptions to categorical-chart palette limits. No decoration or unrelated branding.

QA: all five PNGs opened and inspected. The first field-image pass put the title too close to the domain top; the camera was widened and the warning header separated into four lines. The fan-point annotation was moved clear of the curve knots. Final images carry SIMULATION — V01, SYSTEMAIR KVO 250, EMPTY TOWER, and GRAPH-DIGITIZED FAN CURVE — UNCERTAINTY APPLIES. Units, scale extrema, complete geometry and partial-convergence context are visible. The V00 record was not altered.
