import assert from 'node:assert/strict';
import {roomScenario as s} from './src/room_scenario.mjs';
let checks=0;
function close(a,b){assert.ok(Math.abs(a-b)<1e-9);checks++;}
const a=s(25,2.8,150,.9,30);
close(a.volume,70);close(a.rate,150/70);close(a.targetMinutes,64.47238260383329);
close(a.remaining,Math.exp(-150/70*.5));close(a.requiredCadr30,322.3619130191664);
close(s(50,2.8,150,.9,30).targetMinutes,2*a.targetMinutes);
close(s(25,2.8,300,.9,30).targetMinutes,a.targetMinutes/2);
close(s(25,5.6,150,.9,30).targetMinutes,2*a.targetMinutes);
close(s(25,2.8,150,.9,a.targetMinutes).remaining,.1);
// CDC's perfect-mixing 2 ACH / 99% example ~138 min, adapted to effective clean air.
close(s(25,4,200,.99,0).targetMinutes,138.1551055796427);
assert.equal(s(25,2.8,0,.9,30).targetMinutes,null);checks++;
close(s(25,2.8,0,.9,30).remaining,1);
for(const inputs of [[0,3,150,.9,30],[25,-1,150,.9,30],[25,3,-1,.9,30],[25,3,150,1,30],[25,3,150,.9,-1],[NaN,3,150,.9,30],[25,3,Infinity,.9,30]]){assert.throws(()=>s(...inputs),RangeError);checks++;}
console.log(`PASS ${checks} synthetic room-model checks. Not measured D01 performance.`);
