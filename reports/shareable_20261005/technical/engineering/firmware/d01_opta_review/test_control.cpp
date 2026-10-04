#include <cassert>
#include <iostream>
#include <stdint.h>
#include "ControlLogic.h"
#include "test_support/Arduino.h"
int hostInputs[32]={},hostOutputs[32]={};
uint32_t hostTime=0;
#include "d01_opta_review.ino"

int main() {
  int checks=0;
  auto check=[&](bool v){ assert(v); ++checks; };
  ControlLogic m;
  check(!m.step(true,true,true,false,false));
  check(!m.step(true,true,true,false,false));
  m.step(true,true,false,false,false);
  check(m.step(true,true,true,false,false));
  check(!m.step(true,true,true,true,false));
  check(!m.step(true,true,true,false,false));
  m.step(true,true,false,false,false);m.step(true,true,true,false,false);
  check(!m.step(false,true,false,false,false));
  check(!m.step(true,true,true,false,false));
  m.step(true,true,false,false,false);m.step(true,true,true,false,false);
  check(!m.step(true,false,false,false,false)&&m.trip);
  check(!m.step(true,true,false,false,false)&&m.trip);
  check(!m.step(true,true,true,false,true)&&!m.trip);
  check(!m.step(true,true,true,false,false));
  m.step(true,true,false,false,false);
  check(m.step(true,true,true,false,false));
  m.step(true,false,false,false,true);
  check(!m.step(true,true,false,false,true)&&m.trip);
  m.step(true,true,false,false,false);m.step(true,true,false,false,true);
  check(!m.trip&&!m.run);
  int cases=0;
  for (int state=0;state<32;++state) for(int input=0;input<32;++input) {
    ControlLogic s;
    s.powered=state&1;s.run=state&2;s.trip=state&4;s.startArmed=state&8;s.resetArmed=state&16;
    bool p=input&1,permit=input&2,start=input&4,stop=input&8,reset=input&16;
    bool oldPowered=s.powered,oldTrip=s.trip;
    bool out=s.step(p,permit,start,stop,reset);
    if(!p||!permit||stop||reset||!oldPowered||oldTrip) check(!out);
    ++cases;
  }
  Debounce button;
  check(button.update(true,0)); // held START cannot get a fake boot release
  check(button.update(false,1));check(button.update(false,25));
  check(!button.update(false,26));
  check(!button.update(true,27));check(!button.update(true,51));
  check(button.update(true,52));
  Debounce wrap;wrap.update(false,UINT32_MAX-10);
  wrap.update(true,UINT32_MAX-5);check(wrap.update(true,20));
  // Actual .ino executes against the host shim. No Opta hardware is implied.
  setup();
  for (int p:{D0,D1,D2,D3}) check(hostOutputs[p]==LOW);
  hostInputs[A1]=hostInputs[A3]=hostInputs[A4]=HIGH;
  hostInputs[A0]=HIGH;loop();
  hostTime=30;loop();check(!control.run);
  hostInputs[A0]=LOW;hostTime=35;loop();hostTime=65;loop();
  hostInputs[A0]=HIGH;hostTime=70;loop();hostTime=100;loop();
  check(control.run&&hostOutputs[LED_D0]==HIGH);
  check(hostOutputs[D0]==LOW); // shipped build NEVER closes the fan contact
  hostInputs[A1]=LOW;hostTime=105;loop();check(!control.run);
  hostInputs[A1]=HIGH;hostTime=110;loop();check(!control.run);
  hostTime=300;loop();check(control.trip&&!control.run); // long scan -> latched inhibit
  hostInputs[A4]=LOW;hostTime=305;loop();check(!control.powered&&!control.run);
  std::cout << "{\"host_assertions\":" << checks << ",\"exhaustive_one_step_cases\":" << cases
            << ",\"target_board_compiled\":false,\"physical_tests\":0,\"relay_output_enabled_by_default\":false}" << std::endl;
}
