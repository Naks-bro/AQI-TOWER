// HOST TEST SHIM ONLY, kept outside the sketch; not real board pin numbers.
#pragma once
#include <stdint.h>
#include <initializer_list>
constexpr int LOW=0,HIGH=1,INPUT=0,OUTPUT=1;
constexpr int D0=0,D1=1,D2=2,D3=3,A0=10,A1=11,A2=12,A3=13,A4=14;
constexpr int LED_D0=20,LED_D1=21,LED_D2=22,LED_D3=23;
extern int hostInputs[32],hostOutputs[32];
extern uint32_t hostTime;
inline void pinMode(int,int) {}
inline void digitalWrite(int p,int v) { hostOutputs[p]=v; }
inline int digitalRead(int p) { return hostInputs[p]; }
inline uint32_t millis() { return hostTime; }
