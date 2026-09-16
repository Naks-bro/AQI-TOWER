# V00 figure plan and quality checks

User-selected delivery: local static scientific result images, not a website or dashboard. All images carry SIMULATION — V00 and use actual case data.

| Image | Question | Evidence and encoding | Intended limitation |
| --- | --- | --- | --- |
| velocity_streamlines.png | Where does the empty path accelerate and turn? | Final OpenFOAM U, central Y=0.4 m section; continuous scalar colour, actual inlet-seeded ParaView trajectories | A central slice and inlet seeds cannot identify every 3D recirculation pocket |
| pressure_section.png | How does gauge pressure vary through the path? | Final p multiplied by rho=1.20, Pa; same central plane/camera | Flow-induced gauge pressure, not hydrostatic or absolute pressure |
| residual_history.png | Did equation residuals reach the requested levels? | One row per actual solved iteration, six initial-equation-residual series, logarithmic Y, labelled criteria | Iterations are not physical time; linear solver final residuals are not nonlinear convergence |

Rendering: ParaView 5.11.2 for field images (1100 × 950); Matplotlib for residual PNG (1440 × 720). Scientific continuous colour maps are an intentional exception to categorical palette guidance; no decorative gradients or inferred data. Residual series use explicit colours plus distinct dash patterns; labels, units and neutral criteria remain readable without relying only on colour. This is an AQI student-project figure, not a branded research-publication template, so no unrelated branding is added.

QA before handoff: view exported PNGs, check complete domain, legend scale, units, readable labels, no overlap/clipping, actual time selection and evidence-backed interpretation. Numerical metrics are independently extracted before figures and remain authoritative where point interpolation smooths plotted values.
