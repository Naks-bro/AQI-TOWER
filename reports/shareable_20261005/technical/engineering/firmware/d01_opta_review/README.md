# D01 Opta ordinary-control bench candidate

**Not safety-rated. Not released for wiring, fan operation or energization.**

This is implemented C++ ordinary START/STOP/RESET logic on a specific proposed controller, Arduino Opta Lite AFX00003. It is not a replacement for the open PR1 protective circuit. No new controller has been purchased or installed. On 5 October 2026, the user authorized the isolated Arduino CLI/core installation: the default sketch compiles for the real Opta board target. Flashing and physical tests are NOT DONE.

## What the code does

- Boot, loss of the sensed source and power restoration clear RUN; held START cannot start it until released and pressed again.
- STOP has priority. A missing bench permission latches TRIP; recovery needs RESET and then a separate fresh START.
- START/RESET have an ASSUMED25 ms debounce; STOP and permission are not delayed by that debounce. Polling is nominal5 ms. A returned scan gap over ASSUMED100 ms latches an inhibit; a frozen CPU is NOT protected by this check.
- By default **all four relay commands stay LOW**, even when RUN REQUESTED is true. LEDs show requests only. The shipped sketch must never drive a fan.
- `AQI_BENCH_LAMP_OUTPUT_ENABLED=1` is solely for a reviewed, fused, low-voltage dummy-load bench. It is NOT permission to connect the tower. Output1 contact minimum-load constraints apply to the chosen dummy lamp.
- No networking, retained RUN bit, remote START or blocking wait for a USB connection.

## OEM-supported proposed input mapping

| Terminal | Arduino identifier | Proposed ordinary bench function |
|---|---|---|
| I1 | A0 | START, normally-open momentary contact |
| I2 | A1 | STOP loop, normally closed / HIGH when healthy |
| I3 | A2 | RESET, normally-open momentary contact |
| I4 | A3 | Bench permission contact; NOT a safety input |
| I5 | A4 | Unswitched12 V source-presence indication, DIGITAL mode only |
| Output1 | D0 | Disabled by default; proposed dummy-lamp contact only |

OEM terminals use their printed `+`, `-`, `I1`–`I8` and numbered output-pair labels. We do not invent COM/NO terminal identifiers. Determine actual polarity, compatible harness, source-side protection and physical terminations from the drawing and qualified bench review. Never connect12 V to an analog-mode input; OEM analog range is0–10 V, while digital range is0–24 V. A digital HIGH threshold is not precision undervoltage protection. No fan tach inputs are connected here.

Run `python scripts/analysis/test_d01_opta_host.py` from the repository or packaged engineering root with an already-installed host `g++`. It compiles the actual core and sketch against a clearly labelled GPIO shim and writes `OPTA_HOST_CHECKS.json`. This is not an Opta target build. The separate real-board build is recorded in `OPTA_BOARD_BUILD.json`; review and hardware tests are still required before bench use.

Board-build preparation: desktop tests and their Arduino shim live outside the sketch in `firmware/tests/d01_opta/`. Arduino otherwise compiles sketch-root `.cpp` files, which would bring in the test `main()` and duplicate sketch definitions. The host runner checks this layout.

DETECTED build toolchain: Arduino CLI 1.5.1 and official `arduino:mbed_opta@4.6.0`, installed only in Git-ignored `.tools/arduino/`. CLI archive SHA256 was checked against the official release checksums. No system PATH changes or hardware uploads. The default `arduino:mbed_opta:opta` target (M7 / 2 MB M7 flash split / no signing) compiled with all compiler warnings enabled: 128,464 bytes program storage and 59,232 bytes dynamic memory, no warnings reported. This proves compilation/linking, not correct operation on hardware. The dummy-lamp-enabled variant is NOT compiled or released by this check.

Reproduce on this computer: `python scripts/analysis/compile_d01_opta.py`. The script never installs or uploads; it uses the isolated existing toolchain. On another computer, install the same official versions and configure the local `.tools/arduino/arduino-cli.yaml` directories first. Evidence: [board build record](../../reports/prototype_d01/electrical_package/OPTA_BOARD_BUILD.json). Binaries/toolchain remain local, not included in the technical ZIP. Official [CLI installation instructions](https://docs.arduino.cc/arduino-cli/installation/) and [Arduino core](https://github.com/arduino/ArduinoCore-mbed) checked 5 October 2026.

## Candidate integration and unresolved protection

VERIFIED OEM: Opta Lite12–24 V supply, at12 V maximum2 W; IP20. The drawing shows70 x88.8 mm front dimensions and56.8 mm depth plus4.3 mm projection. It does not fit the current40 mm deep reservation in a normal DIN orientation. RECOMMENDATION: a separate low-voltage bench/control enclosure, not a new tower CAD branch. Hammond1554XA2GY300 x200 x120 mm is a verified enclosure candidate only; mounting plate, DIN rail, buttons, cable entries, clearances and cooling are not released. A drilled enclosure does not inherit the stock ingress rating.

The controller adds0.167 A at its maximum published12 V consumption. Fans plus controller alone demand1.567 A /18.8 W, leaving0.433 A before hub, speed-controller, input and other loads/startup. This is arithmetic, not sufficient supply proof.

The firmware cannot detect an internal fan reset with power still present, hub recovery while RUN remains true, welded contacts, a frozen MCU, safe standstill or actual guard access. Opta is ordinary control, not a safety PLC. Existing project restart/protection requirements stay OPEN and unchanged. An appropriately reviewed independent protective system must act independently of this firmware where required. Do not bridge PR1 to make this candidate run.

Primary sources checked5 October2026:

- [Arduino collective datasheet](https://docs.arduino.cc/resources/datasheets/AFX00001-AFX00002-AFX00003-datasheet.pdf), revision shown1 October2026; electrical/physical data, not complete-device approval.
- [Arduino pinout, Lite on page3](https://docs.arduino.cc/resources/pinouts/AFX00001-AFX00002-AFX00003-full-pinout.pdf). The OEM sheet is CC BY-SA4.0; linked, not republished or traced. This project's drawing is original; identifiers and technical facts are used as references.
- [Arduino official Opta mapping example](https://docs.arduino.cc/tutorials/opta/getting-started-with-interrupts). This sketch polls; it does not use that example's code.
- [Hammond exact enclosure](https://www.hammfg.com/part/1554XA2GY). Shipping weight is not installed net weight. No price or India stock claimed.

Next release evidence: accepted hazard allocation and independent protection, exact physical harness and source fault/time behavior, assessed enclosure/controls/retention, board compilation and unpowered inspection, followed by qualified dummy-load commissioning. No fan or energized live fault testing is authorized by these files.
