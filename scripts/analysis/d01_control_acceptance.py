"""Offline requirements model only. Never deploy this as a safety controller."""
from dataclasses import dataclass
from itertools import product

@dataclass
class Model:
    powered: bool = False
    run: bool = False
    trip: bool = False
    start_armed: bool = False
    reset_armed: bool = False

    def step(self, power=True, permit=True, start=False, stop=False, reset=False):
        # permit represents a VERIFIED protective condition, not a sensor implementation.
        if power is not True:
            self.powered = self.run = self.start_armed = self.reset_armed = False
            return False
        if not self.powered:
            self.powered = True
            self.run = self.start_armed = self.reset_armed = False
            if permit is not True:
                self.trip = True
            return False
        if permit is not True:
            self.trip = True
            self.run = self.start_armed = self.reset_armed = False
            return False
        if stop:
            self.run = self.start_armed = False
            self.reset_armed = not reset
            return False
        if self.trip:
            self.run = self.start_armed = False
            if reset and self.reset_armed:
                self.trip = False
                self.reset_armed = False
            elif not reset:
                self.reset_armed = True
            return False
        if reset:
            self.run = self.start_armed = False
            return False
        if not start:
            self.start_armed = True
        elif self.start_armed:
            self.run = True
            self.start_armed = False
        return self.run

def tests():
    results = []
    def check(name, condition):
        assert condition, name
        results.append(name)
    m = Model()
    check('Power-on with held START inhibited', not m.step(start=True))
    check('Held START remains inhibited', not m.step(start=True))
    m.step(); check('Fresh START accepted', m.step(start=True))
    check('STOP overrides START', not m.step(start=True, stop=True))
    check('Held START after STOP inhibited', not m.step(start=True))
    m.step(); m.step(start=True)
    check('Power loss clears run', not m.step(power=False))
    check('Restore does not run', not m.step(start=True))
    m.step(); m.step(start=True)
    check('Unknown permissive trips', not m.step(permit=None) and m.trip)
    check('Closing access does not restart', not m.step() and m.trip)
    check('RESET alone does not restart', not m.step(reset=True, start=True) and not m.trip)
    check('START held through reset inhibited', not m.step(start=True))
    m.step(); check('Separate fresh START after reset accepted', m.step(start=True))
    m.step(permit=False, reset=True)
    check('Held RESET cannot clear trip on recovery', not m.step(reset=True) and m.trip)
    m.step(); m.step(reset=True)
    check('Fresh RESET clears trip but stays off', not m.run and not m.trip)
    count = 0
    for powered, run, trip, armed, reset_armed in product((False, True), repeat=5):
        for power, permit, start, stop, reset in product((False, True), repeat=5):
            x = Model(powered, run, trip, armed, reset_armed)
            out = x.step(power, permit, start, stop, reset)
            if not power or not permit or stop or reset or not powered or trip:
                assert not out
            count += 1
    return {'status':'PASS - abstract software only', 'named_checks':results,
            'exhaustive_one_step_cases':count,
            'limitations':'No physical sensing, timing, contacts, diagnostic coverage or safety integrity modeled.'}

if __name__ == '__main__':
    import json
    print(json.dumps(tests(), indent=2))
