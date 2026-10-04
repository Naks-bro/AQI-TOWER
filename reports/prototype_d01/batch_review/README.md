# Current handoff consistency and parts

`CURRENT_COMBINED_PARTS_REGISTER.csv` reconciles the current R03M indoor cabinet
and E05 external control-module candidates. It is an onboarding register, not
a purchase or construction approval. Candidate product identity does not imply
India stock, price, delivered dimensions, protective suitability or actual fit.
Do not add historical BOM quantities to this register; custom fastening uses
the controlling mechanical schedule.

`HANDOFF_CONSISTENCY.json` and `AUDIT_FINDINGS.csv` record the last executable
digital audit. Run `python scripts/maintenance/check_d01_handoff_consistency.py`
from the repository for a current read-only result. Existing bundled report
Python enables the optional PDF extraction check without installation.
`--write-results` refreshes only these audit reports; rebuild both bundles
afterward, then run the checker again without that flag.

The checker validates unchanged 493-object native tower provenance, current
E05 three-pair service evidence, default-disabled firmware and target-build
source hashes, current pressure inputs, package manifests and source copies.
Text files may be content-identical with LF/CRLF differences; this is recorded
explicitly while ZIP manifests always require exact payload bytes. Historical
IH02 pages are preserved references, not the current product/controls decision.

Passing this checker proves digital consistency only. Physical prototypes and
physical tests remain zero. Guards/structure/seals, exact connectors, protection,
commissioning and measured performance are not approved by a software audit.
