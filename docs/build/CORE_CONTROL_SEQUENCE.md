# Fan/filter core — operating and fault plan R00

3 October 2026. PRELIMINARY FUNCTIONAL DESIGN: NOT RELEASED FOR WIRING OR ENERGIZING.

## In simple words

Press START to run the tower and STOP to stop it. After a power cut or a protective trip, it must not restart by itself. For filter changes, switch off, isolate and lock off the electrical supply; a stopped fan or a zero-speed setting is not proof that it is safe to touch.

The first prototype uses local controls and an OEM-compatible manual speed setting. The laptop records measurements only. No app, automatic PM-based speed changes, remote start or custom safety PCB is proposed for this first build.

## Evidence labels

- FACT / user basis: indoor trial first; college/NGO funding only; ENTC review optional. The assistant prepares this design, with qualified physical review/assembly/testing before use.
- DETECTED: historical AC fan data and a different S&P EC comparison candidate exist. Neither gives an approved wiring design for a selected delivered unit.
- RECOMMENDATION: the behavior below is the design requirement to implement and verify, not a description of installed hardware.
- UNKNOWN: exact fan SKU, delivered manual, supply conditions, motor protection/reset behavior, switching architecture, coast-down time, access arrangement and component ratings.
- Physical implementation and tests: NOT DONE. All six overall build gates remain open.

See the [functional visual](CORE_ELECTRICAL_FUNCTIONS.svg). It has no terminal numbers, conductor sizes or device ratings. It is a starting point for E01/E02, not their release.

## Proposed operating sequence

| State | Meaning | Transition requirement |
|---|---|---|
| ISOLATED | Maintenance isolation established and verified by the competent person | Restore only after work complete, covers/guards secured and tools removed |
| OFF / NOT READY | Supply may be present; start inhibited | Resolve missing permissives; OFF is not safe-access permission |
| READY | Verified permissives available; no run request | Fresh local START action, after START has been released |
| RUN REQUESTED | Reviewed controls request fan operation | Confirm actual operation separately; command is not rotation proof |
| STOPPING | Run request removed; fan may coast | Do not allow hazardous access based on a timer guessed in software |
| TRIPPED | Protective condition latched; start inhibited | Resolve cause, verify permissives, deliberate RESET, then a separate fresh START |

Power restoration leads to OFF, not RUN REQUESTED. Closing a door, clearing a fault or pressing RESET alone must not start the fan. A START button held during restoration/reset must be released before a new start is accepted. STOP or a protective inhibit takes priority over START.

These are acceptance requirements for the reviewed hardware architecture. A Python script, laptop, microcontroller or ordinary relay diagram is not their safety implementation. Protective function selection, diagnostic coverage and required reliability remain a qualified risk-assessment task.

## Cause and effect

| Event | Required response / operator action | Unresolved implementation |
|---|---|---|
| Supply lost and restored | Run request cleared; fresh local start required | Undervoltage/restart prevention and OEM internal restart behavior |
| Local STOP | Remove run request; indicate stopping if appropriate | OEM-approved stop method and actual run-down |
| Service access opened or protective permissive lost | Inhibit start; initiate reviewed protective response | Which doors expose hazards; interlock/guard locking and response architecture |
| Guard closed again | Remain stopped; deliberate reset if protective trip, then fresh start | No automatic restart from door closure |
| OEM thermal/motor protection operates | Preserve OEM protection; stop/inhibit through reviewed arrangement; investigate cause | Exposed contacts/status, internal auto-reset and external trip detection UNKNOWN |
| Protective input missing, broken or inconsistent | Do not treat UNKNOWN as permission to run | Detection, fail-safe behavior and fault tolerance must be designed, not assumed |
| Speed command lost/disconnected | Behavior must be resolved and verified before release | Do not assume 0 V, open circuit or communication loss means stopped |
| Fan fails to respond to run request | Operator stops test; inspect only under isolation | Actual run feedback and detection timeout UNKNOWN; no invented RPM terminal |
| Filter pressure rises | Record and flag only against an approved maintenance threshold | No inherited 80/100/111 Pa automatic trip; use filter limits and measured duty |
| PM sensor/logger/USB connection fails | Mark measurement invalid; suspend performance-data trial | Logger failure must not disable independent protection; no automatic safety action claimed |
| Emergency stop, if required by risk assessment | Reviewed protective stopping; reset must not restart | Need, location, stop category and reset architecture UNKNOWN |

A door switch alone does not prove safe access while the impeller coasts. Determine whether fixed guarding, guard locking or another validated arrangement is required. Motor protection may reset internally: do not assume it supplies an external trip contact or prevents restart. That behavior must be addressed for the selected unit.

## Controls and indicators to design

Local START, STOP and deliberate trip RESET are proposed functions, not selected parts. Include a separately identifiable lockable service isolator. Emergency-stop provision is a risk-assessment decision, not silently equated with normal STOP.

- Label a command indication **RUN REQUESTED**, not **FAN RUNNING**, unless actual operation feedback is verified.
- A power lamp can indicate its monitored point only; a dark lamp never proves isolation.
- Keep the speed reference separate from restart permission and service isolation.
- Keep monitoring powered separately from fan control where practical; define every supply affected by maintenance isolation. Avoid backfeed through USB or separately powered equipment.
- Keep protective-earth continuity independent of controls; never switch or fuse PE. Determine actual fan class and bonding requirements from the supplied unit and the enclosure design.

## Electrical interfaces — not a terminal schedule

The [interface register](CORE_ELECTRICAL_INTERFACES.csv) lists functions and missing evidence. All physical terminal IDs, sizes and ratings remain UNKNOWN. It must not be used as assembly instructions.

E01: source, isolation, protection and branch single-line from verified site inputs.
E02: selected fan/OEM controller plus reviewed stop/restart/protective circuits.
E03: exact terminal-to-terminal and cable schedule after E01/E02 review.
E04: enclosure layout, segregation, bonding, glands and service access.
E05: cable/protection/switching selection using actual supply fault conditions, motor inrush/leakage and installation environment—not nominal watts alone.
E06: physical commissioning procedure with reviewer-approved methods and recorded results.

## Proposed commissioning witness cases

All are NOT EXECUTED. Qualified personnel must choose safe test methods; do not induce live faults or defeat guards. Some cases can be verified by document/design review plus controlled simulations rather than deliberately damaging equipment.

| Case | Acceptance to demonstrate |
|---|---|
| C01 | Inspection confirms approved components, guards, terminations and segregation |
| C02 | Applicable bonding, insulation, polarity and protection tests recorded |
| C03 | Power applied with no START: no run request / unintended movement |
| C04 | Normal start, OEM speed adjustment and stop operate as approved |
| C05 | Power interruption/restoration does not automatically restart |
| C06 | START held through power restoration cannot automatically restart |
| C07 | Simultaneous START/STOP resolves to stop |
| C08 | Access protective function prevents start and gives the approved stopping response |
| C09 | Closing access alone or RESET alone does not restart |
| C10 | START held through reset requires release and a new deliberate action |
| C11 | OEM trip/reset behavior cannot create unintended restart |
| C12 | Specified protective input faults have the reviewed response |
| C13 | Speed-command loss behavior matches approved design |
| C14 | Logger/USB failure cannot defeat protection; data marked invalid |
| C15 | Service isolation covers identified supplies; run-down/access and restoration verified |

Do not record PASS until there is a dated result, exact assembly revision, method, instrument details where applicable, reviewer/operator and evidence reference. This checklist does not establish compliance or replace risk assessment.

## Sources checked 3 October 2026

- [S&P TD-SILENT ECOWATT family installation manual](https://statics.solerpalau.com/media/import/documentation/H13-TD-SILENT-ECOWATT-NOTICE.pdf): family reference found, not the confirmed supplied-unit manual. Variants differ; obtain the actual article/revision before using any diagram. No terminal assignment or protection rating copied into this pack. A subsequent fetch timed out; no new local manual archive is claimed.
- [HSE machinery safety introduction](https://www.hse.gov.uk/work-equipment-machinery/introduction.htm): used for general guarding, safe maintenance isolation, competent work and restart-risk review. UK guidance, not an Indian compliance determination.

Next release input: exact fan and matching OEM instructions **plus** actual site/supply facts. Prepare rated E01–E05 from those inputs and obtain qualified review before assembly; do not choose a fan solely to finish the circuit. The [fan-duty comparison](FAN_DUTY_DECISION.md) still has loaded-duty limitations.
