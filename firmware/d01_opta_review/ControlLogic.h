// D01 ordinary operational control ONLY. Not a safety controller.
#pragma once
#include <stdint.h>

struct ControlLogic {
  bool powered=false, run=false, trip=false, startArmed=false, resetArmed=false;
  bool step(bool power, bool permit, bool start, bool stop, bool reset) {
    if (!power) { powered=run=startArmed=resetArmed=false; return false; }
    if (!powered) {
      powered=true; run=startArmed=resetArmed=false;
      if (!permit) trip=true;
      return false;
    }
    if (!permit) { trip=true; run=startArmed=resetArmed=false; return false; }
    if (stop) { run=startArmed=false; resetArmed=!reset; return false; }
    if (trip) {
      run=startArmed=false;
      if (reset && resetArmed) { trip=false; resetArmed=false; }
      else if (!reset) resetArmed=true;
      return false;
    }
    if (reset) { run=startArmed=false; return false; }
    if (!start) startArmed=true;
    else if (startArmed) { run=true; startArmed=false; }
    return run;
  }
};

// Initial HIGH stays HIGH: prevents a held boot-time button looking released.
// Both edges must remain stable for this illustrative 25 ms debounce interval.
struct Debounce {
  bool initialized=false, stable=false, candidate=false;
  uint32_t changed=0;
  bool update(bool raw, uint32_t now) {
    if (!initialized) { initialized=true; stable=candidate=raw; changed=now; }
    if (raw!=candidate) { candidate=raw; changed=now; }
    if (uint32_t(now-changed)>=25) stable=candidate;
    return stable;
  }
};
