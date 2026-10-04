# Electrical batch — the exact remaining design decisions

5 October 2026. **DIGITAL SCREEN; NOT FOR WIRING, PROCUREMENT OR ENERGIZATION.**

This extends current E05, not an alternative enclosure or replacement firmware. Physical prototypes: **0**. Original tower, E01/E02 evidence, firmware and existing restart requirements are preserved.

## Concrete findings

1. **DETECTED arithmetic:** four published 0.35 A fans plus the Opta's 2 W maximum-at-12-V screen total **1.5667 A** before hub/controller/input/other unallocated consumption. The 2 A source leaves **0.4333 A**. With those controls, simultaneous fan multiplier ceiling is **1.3095×**, not the fan-only 1.4286×. Adding an ASSUMED 0.10 A auxiliary draw reduces it to **1.2381×**. These are thresholds for obtaining data, not measured inrush or permission to start.
2. **Topology decision:** Opta is proposed on an independently protected unswitched branch upstream of the fan control path, not through the fan hub. That distribution/branch arrangement is **not selected or wired**. Source-total and fan-path currents are calculated separately. A larger adapter alone does not remove the hub's four-pin 24 W limit.
3. **VERIFIED voltage distinction:** Opta recommends 12–24 V and publishes a permissible range of 10.2–27.6 V. At a nominal 12 V source, any conductor/connector drop takes its input below the recommended minimum; a nominal **1.8 V** remains above the permissible minimum. Unknown source tolerance and transients must be subtracted from that 1.8 V: do not treat it as a guaranteed margin. Fan continuous minimum voltage remains unknown; its published start-voltage is not a system running-voltage acceptance value.
4. **DETECTED protection counterexample:** if this source limits a fault to an ASSUMED sustained 2 A, a 2 A fuse sees only 100% rating. The candidate's 110%, 135% and 200% timing test currents are 2.2, 2.7 and 4 A. No prompt clearing follows at 2 A; even the 110% minimum opening time is 100 hours. Actual source/hub profiles, wire damage limits and fuse-holder temperature are unknown. A fuse's interrupt rating is not proof that this supply can deliver enough current to open it. **No fuse selected.**
5. **DETECTED information gap:** hub upstream tachometry represents port 1 only. A working port-1 signal cannot prove all four fans run. An upstream unswitched source input cannot detect a downstream hub fuse recovery or individual fan internal recovery. The current ordinary logic therefore cannot close the retained downstream restart requirement.

## Low-current contact result — no hidden historical substitution

Current Schneider Digest, section 19, dated 22 July 2026, identifies ZBE1016/ZBE1026 low-power contacts. A fresh primary-source check found [FAQ FA100572](https://www.se.com/us/en/faqs/FA100572/), last modified 14 May 2026. Its answer says **“0 .1 A to 100 mA and 5 to 24 V. No minimum level is noted.”** That current-unit wording is internally ambiguous. We do **not** change A to mA, treat it as a verified range, or substitute a historical catalogue.

The Opta's published digital-input current is 1.12 mA at 10 V; 12 V / 8.9 kΩ gives a **nominal resistance screen of 1.348 mA**, not guaranteed impedance/current at all tolerances. The gold low-power contact candidates remain sensible candidates, **not a completed low-load qualification**. Exact contact screw IDs remain unverified. Final approval needs an unambiguous present-part OEM switching/reliability statement for this actual voltage/current/environment. No parallel wetting resistor is added speculatively.

## Hazard-to-function allocation — decide the smallest justified architecture

| Actual scenario | Function needed | Proposed allocation / exact unresolved decision |
|---|---|---|
| Reach to rotating impeller during ordinary use | Prevent hazardous contact | Fixed independent fan guards; verify real perforations, seams, attachment and strength. CAD reservations cannot establish safe reach. If accessible reach remains possible, stopping/access protection must be designed; do not assume software STOP solves it. |
| Filter removal / hub speed preset / wiring maintenance | Prevent energization and address coast-down | Isolate all identified sources, prevent reconnection, verify appropriate de-energization and safe access before opening. Unmodified external adapter remains outside; USB/service sources must be accounted for. A dark LED or button STOP is not isolation. |
| Door opened while fans are coasting | Prevent contact during residual motion | Decide whether retained fixed guarding still excludes reach for the entire service task. If not, guarding/access sequencing or validated stopping/access protection is needed. No guessed timer or blanket guard-lock part selected. |
| Overload/short circuit/closed-box heat | Prevent conductor/contact/component damage | OEM adapter and hub functions remain intact. Coordinate branch wiring and protection using actual current-time and temperatures; the screen above identifies why nominal 2 A fuse selection is insufficient. No automatic temperature trip invented. |
| Power loss/restoration | Avoid unexpected operation | Retained requirement: deliberate local START after restoration; held START rejected. Ordinary firmware passes synthetic tests and target compile but no approved fan actuator is connected. Decide actual switching architecture and failure response after hazard assessment. |
| Hub auto-reset or fan internal recovery | Avoid an unexpected recovery where hazardous; preserve current stricter restart requirement | Fixed guards can reduce contact hazard but do not automatically waive the project's no-auto-restart requirement. Need actual OEM recovery behavior and reviewed detection/actuation, or an explicit justified requirement disposition. **OPEN**, not silently downgraded to ordinary inconvenience. |
| One fan fails while others run | Flag invalid test; determine whether a protection response is necessary | Port-1 tach is insufficient. For an attended trial, operator observation may flag operating disruption; whether thermal/other hazard requires independent detection must be decided from actual installation. No 4-fan diagnostic claim. |
| Controller hangs, contact fails, or speed/PWM signal is lost | Do not defeat any allocated protective function | Ordinary Opta/START/STOP/RESET are not protective controls. Review OEM PWM-loss behavior and required independence/reliability if a safety-related response is allocated. Software scan timing does not protect a frozen CPU. |

**Why PR1 is unspecified:** accessible-hazard consequences, installed fixed-guard proof, isolation arrangement, recovery behavior and required reliability are not yet settled; DC switching, fault response and feedback are also unspecified. Selecting a generic safety relay would not answer these questions or necessarily prevent an internal hub recovery. A qualified, documented hazard allocation can determine whether fixed guarding plus isolation and reviewed ordinary restart control is sufficient, or whether a separate protective path is required. The digital preparation must not guess either conclusion. Existing restart acceptance cases remain in force.

## Circuit and cable decisions now exposed

[Cable/interface schedule](CABLE_AND_INTERFACE_SCHEDULE.csv) lists 15 functions, known OEM endpoints and the **specific** missing conductor/protection/terminal facts. It intentionally contains UNKNOWN lengths and contact IDs, not fake terminal-to-terminal release instructions. Signal conductor acceptance at the Opta is not cable ampacity approval. Factory fan cables remain unmodified; a distribution connector/terminal assembly must be selected before adding an Opta branch.

The calculated voltage cases use ASSUMED copper resistivity 0.0175 Ω·mm²/m at 20°C, coefficient 0.00393/°C, round-trip length and an ASSUMED 0.05 Ω aggregate contact resistance. They are not a certified cable table. Larger conductor area reduces voltage drop but does not demonstrate fault clearing or compatible termination. Obtain actual installed length/resistance/contact limits and temperature before choosing a gauge.

**Next circuit closure dependencies, in order:**

1. Mechanical fixed-guard/access decision supplies the hazard allocation; retain or explicitly disposition every restart case.
2. OEM startup/recovery and current-time data supplies the source/branch/protection assessment. Existing enquiries remain pending; this batch sends nothing.
3. Select rated distribution, isolation/actuation/protection and actual conductors from those facts; add real envelopes to E05 before releasing the panel.
4. A competent reviewer approves the exact schematic, terminations, isolation/bonding and commissioning methods; unpowered exact-part fit and controlled dummy-load testing precede fan commissioning.

This is not a demand for an arbitrary extra safety relay or a request to outsource the design unprepared: calculations, failure counterexamples, interface allocation and executable screens are ready for those exact decisions.

## Reproduce and evidence

Run from repository root with existing Python:

```
python scripts/analysis/test_d01_electrical_release_batch.py
python scripts/analysis/d01_electrical_release_batch.py
```

Generated JSON records hashes of retained E01, Opta integration and real board-build records; 24 power, 36 cable and 8 input cases are **synthetic/analytic**, not bench evidence. Input rejection tests and analytic cases are in the adjacent test script. Run the existing target/host firmware tools separately for firmware evidence; this batch does not flash any device. No OEM drawings/models are redistributed.

Primary sources checked 5 October 2026:

- [Arduino Opta datasheet](https://docs.arduino.cc/resources/datasheets/AFX00001-AFX00002-AFX00003-datasheet.pdf), modified 1 October 2026, sections 3.5/4.2/5.2. Supply/input/wire facts are used; relay minimum-load wording also deserves verification before any future dummy-lamp selection because its stated power and illustrative voltage/current are not arithmetically equivalent. Default relays remain disabled.
- [Schneider 2026 Digest section19](https://www.se.com/us/en/download/document/0100CT2401-SEC-19/) and [current ambiguous FAQ](https://www.se.com/us/en/faqs/FA100572/). No numeric contact release.
- [Noctua NV-PS1](https://www.noctua.at/en/products/nv-ps1/specifications), [NA-FH1 specifications](https://www.noctua.at/en/products/na-fh1/specifications) and [hub recovery/monitoring functions](https://www.noctua.at/en/products/na-fh1/features). No stock/price/India conformity claim.
- [Littelfuse MINI 32 V data](https://www.littelfuse.com/assetdocs/littelfuse-datasheet-297-mini32v?assetguid=42c9dd21-a88e-4328-8e67-2f832444faf1), retained E02 exact candidate screen. Candidate timing values are not installation approval.

**Closed digitally:** integrated source-versus-fan-path budgets; tolerance-aware voltage screening; explicit fuse counterexample; ordinary-input and 15-function cable allocation; hazard/recovery dependencies. **Not closed:** rated circuit, contact qualification, actual harness, protection or commissioning.
