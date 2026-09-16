/**
 * Engineering status definitions and component assignments.
 * Statuses are based on the current engineering record; see PHASE docs for provenance.
 */

export const STATUS = {
  SIMULATED: {
    id: 'SIMULATED',
    label: 'SIMULATED',
    cssClass: 's-sim',
    description: 'Derived from CFD simulation. Not measured on physical hardware.',
  },
  SELECTED_CANDIDATE: {
    id: 'SELECTED_CANDIDATE',
    label: 'SELECTED CANDIDATE',
    cssClass: 's-sel',
    description: 'Selected as research candidate. Not yet physically tested.',
  },
  RESEARCH_CONTROL: {
    id: 'RESEARCH_CONTROL',
    label: 'RESEARCH CONTROL',
    cssClass: 's-sel',
    description: 'Designated research control media for experimental comparison.',
  },
  PROVISIONAL: {
    id: 'PROVISIONAL',
    label: 'PROVISIONAL / SCHEMATIC',
    cssClass: 's-prov',
    description: 'Geometry or value is a placeholder. Design not frozen. Not in any validated model.',
  },
  CONCEPT: {
    id: 'CONCEPT',
    label: 'CONCEPT ONLY',
    cssClass: 's-con',
    description: 'Concept stage only. No engineering basis. Feasibility not assessed.',
  },
  EXPERIMENT_PENDING: {
    id: 'EXPERIMENT_PENDING',
    label: 'EXPERIMENT PENDING',
    cssClass: 's-pend',
    description: 'Experiment designed and ready; hardware not yet assembled. No measured data exists.',
  },
  NOT_VALIDATED: {
    id: 'NOT_VALIDATED',
    label: 'NOT PHYSICALLY VALIDATED',
    cssClass: 's-prov',
    description: 'Parameter selected but not confirmed by measurement on physical hardware.',
  },
};

export const COMPONENT_STATUS = {
  HEPA_FILTER: {
    status: STATUS.SELECTED_CANDIDATE,
    note:   'SELECTED RESEARCH COMPONENT / NOT PHYSICALLY VALIDATED',
    source: 'docs/PHASE16_CLEAN_AIR_TEST_PROTOCOL.md',
  },
  FAN_KVO250: {
    status: STATUS.SIMULATED,
    note:   'CURRENT CFD FAN CANDIDATE — Phase 9/10 fan-curve CFD',
    source: 'results/CFD_V01_FAN/metrics.json',
  },
  CARBON_STAGE: {
    status: STATUS.PROVISIONAL,
    note:   'PLANNED — BED DESIGN NOT FROZEN. RFQ in progress (OVC 4×8).',
    source: 'docs/PHASE17B_PROCUREMENT_TRACKER.md',
  },
  WATER_STAGE: {
    status: STATUS.CONCEPT,
    note:   'CONCEPT — FEASIBILITY NOT YET DECIDED',
    source: null,
  },
  PRESSURE_DROP: {
    status: STATUS.EXPERIMENT_PENDING,
    note:   'Phase 17A blocked on hardware procurement.',
    source: 'docs/PHASE17A_PRESSURE_DROP_RESULTS.md',
  },
};
