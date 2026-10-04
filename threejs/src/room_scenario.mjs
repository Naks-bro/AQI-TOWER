// Ideal indoor particle mass balance, NOT a rating of D01 or a CFD solver.
export function roomScenario(area, height, cadr, reduction, minutes) {
  if ([area,height,cadr,reduction,minutes].some(x=>typeof x!=='number'||!Number.isFinite(x)) || area<=0 || height<=0 || cadr<0 || reduction<=0 || reduction>=1 || minutes<0) throw new RangeError('Invalid room scenario');
  const volume=area*height, rate=cadr/volume;
  return {volume,rate,remaining:Math.exp(-rate*minutes/60),
    targetMinutes:cadr===0?null:-Math.log1p(-reduction)/rate*60,
    requiredCadr30:volume*(-Math.log1p(-reduction))*2};
}
