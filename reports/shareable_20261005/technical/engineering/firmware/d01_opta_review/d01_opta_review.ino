// BENCH REVIEW ONLY. Default configuration never closes any relay.
// Do not use this sketch to control fans or implement protective functions.
#include <Arduino.h>
#include <initializer_list>
#include "ControlLogic.h"

#ifndef AQI_BENCH_LAMP_OUTPUT_ENABLED
#define AQI_BENCH_LAMP_OUTPUT_ENABLED 0
#endif

ControlLogic control;
Debounce startButton, resetButton;
uint32_t lastScan=0;
bool scanInitialized=false;

void setup() {
  // OEM mapping: output1=D0 ... output4=D3; I1=A0 ... I5=A4.
  for (int relay : {D0,D1,D2,D3}) {
    digitalWrite(relay,LOW);
    pinMode(relay,OUTPUT);
  }
  for (int input : {A0,A1,A2,A3,A4}) pinMode(input,INPUT);
  for (int led : {LED_D0,LED_D1,LED_D2,LED_D3}) {
    digitalWrite(led,LOW); pinMode(led,OUTPUT);
  }
  // No networking, retained RUN bit, USB start command or wait for Serial.
}

void loop() {
  const uint32_t now=millis();
  const uint32_t elapsed=uint32_t(now-lastScan);
  if (scanInitialized && elapsed<5) return;
  // A returned long scan inhibits operation; this does not protect a frozen CPU.
  const bool scanFault=scanInitialized && elapsed>100;
  scanInitialized=true; lastScan=now;
  const bool start=startButton.update(digitalRead(A0)==HIGH,now);
  const bool stopHealthy=digitalRead(A1)==HIGH; // bench NC STOP loop
  const bool reset=resetButton.update(digitalRead(A2)==HIGH,now);
  const bool benchPermit=digitalRead(A3)==HIGH;
  const bool sourcePresent=digitalRead(A4)==HIGH; // DIGITAL, never analogRead
  const bool request=control.step(sourcePresent,benchPermit&&!scanFault,start,!stopHealthy,reset);
  digitalWrite(LED_D0,request?HIGH:LOW); // RUN REQUESTED, not fan-running proof
  digitalWrite(LED_D1,control.trip?HIGH:LOW);
  digitalWrite(LED_D2,sourcePresent?HIGH:LOW); // not proof of isolation
  digitalWrite(LED_D3,LOW);
  // Enabling this is only for a reviewed, fused low-voltage dummy-lamp bench.
  digitalWrite(D0,(AQI_BENCH_LAMP_OUTPUT_ENABLED && request)?HIGH:LOW);
  digitalWrite(D1,LOW); digitalWrite(D2,LOW); digitalWrite(D3,LOW);
}
