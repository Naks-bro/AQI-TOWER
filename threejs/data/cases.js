/**
 * Case registry — AQI Tower simulation database.
 *
 * All values are EXACT from JSON result files. Rounded only for display.
 * Sources noted per field. DO NOT invent or round values silently.
 *
 * Convergence status definitions used here:
 *   CONVERGED          — all four internal criteria passed (residuals, mass, flow_stability, fan_closure)
 *   PARTIALLY_CONVERGED— mass + flow_stability + fan_closure passed; residuals criterion NOT met
 *   POST_PROCESSED     — frozen field from a converged/partially-converged case used for post-processing
 */

export const CASES = {

  GEO_C: {
    case_id:       'GEO_C',
    display_name:  'GEO_C — Empty Tower',
    geometry:      'GEO_C (riser_inner_x=260 mm, riser_top_z=1850 mm, two-step turn)',
    solver:        'OpenFOAM SIMPLEC, k-ε RNG, KVO 250 fan curve BC',
    phase:         'Phase 8',
    status:        'CONVERGED',
    caveats:       'Empty tower (no filter resistance). All four convergence criteria passed at iteration 926. DESIGN EXPERIMENT PARAMETER — NOT PRODUCT REQUIREMENT.',

    // From results/GEOMETRY_OPTIMIZATION/GEO_C/metrics.json (exact values)
    final_iteration:      926,
    cell_count:           63780,
    Q_m3_h:               1496.0549912644801,
    Q_m3_s:               0.4155708309068,
    fan_static_Pa:        3.500308699874432,
    peak_speed_m_s:       5.619945049285889,
    mean_speed_m_s:       1.5437583723550312,
    mass_imbalance_pct:   7.397751584759326e-6,
    riser_reverse_pct:    15.881727631610348,
    riser_entry_CoV:      0.23440535597556758,
    criteria: { residuals: true, mass: true, flow_stability: true, fan_closure: true },
    source:        'results/GEOMETRY_OPTIMIZATION/GEO_C/metrics.json',
    validation:    'SIMULATION ONLY — NOT PHYSICALLY VALIDATED',
  },

  GEO_C_CONFIRM: {
    case_id:       'GEO_C_CONFIRM',
    display_name:  'GEO_C Confirmation Run',
    geometry:      'GEO_C (identical mesh to GEO_C)',
    solver:        'OpenFOAM SIMPLEC, k-ε RNG, KVO 250 fan curve BC',
    phase:         'Phase 8',
    status:        'CONVERGED',
    caveats:       'Confirmation run on the same mesh and setup as GEO_C. Metrics are identical to GEO_C (same residuals, flow, fan operating point). Confirms result reproducibility.',

    // From results/GEOMETRY_OPTIMIZATION/GEO_C_CONFIRM/metrics.json (exact, identical to GEO_C)
    final_iteration:      926,
    cell_count:           63780,
    Q_m3_h:               1496.0549912644801,
    Q_m3_s:               0.4155708309068,
    fan_static_Pa:        3.500308699874432,
    peak_speed_m_s:       5.619945049285889,
    mean_speed_m_s:       1.5437583723550312,
    mass_imbalance_pct:   7.397751584759326e-6,
    riser_reverse_pct:    15.881727631610348,
    riser_entry_CoV:      0.23440535597556758,
    criteria: { residuals: true, mass: true, flow_stability: true, fan_closure: true },
    source:        'results/GEOMETRY_OPTIMIZATION/GEO_C_CONFIRM/metrics.json',
    validation:    'SIMULATION ONLY — NOT PHYSICALLY VALIDATED',
  },

  CASE_M_SEALED: {
    case_id:       'CASE_M_SEALED',
    display_name:  'CASE_M_SEALED — GEO_C + H13 HEPA + Sealed Bypass',
    geometry:      'GEO_C with bypassSeal baffle at z=0.850 m (x=0.260–0.305 m, y=0.150–0.650 m)',
    solver:        'OpenFOAM SIMPLEC, k-ε RNG, H13 HEPA porous baffle (resistance multiplier=1.0)',
    phase:         'Phase 10B',
    status:        'PARTIALLY_CONVERGED',
    caveats:       'Ran 5000 iterations; stopped at RANS residual plateau (same as all GEO_C-geometry cases). Integrated quantities (Q, bypass, filter ΔP) are stable in final iterations. PARTIAL NON-CONVERGED RANS. Single-point calibrated H13 resistance. Not validated on physical hardware.',

    // From results/FILTER_H13/bypass_analysis_sealed.json (exact values)
    final_iteration:            5000,
    Q_m3_h:                     1332.205242935976,
    Q_m3_s:                     0.37005701192666,
    filter_flow_m3_h:           1332.2052416041201,
    bypass_flow_m3_h:           1.3318560254660383e-6,
    bypass_fraction:            9.997378480619545e-10,
    effective_filtered_fraction: 0.9999999990002622,
    filter_delta_P_Pa:          111.18113437173315,
    filter_face_velocity_mean:  1.0524943445867463,
    filter_face_velocity_min:   0.813450330212173,
    filter_face_velocity_max:   1.1724754064604663,
    filter_face_velocity_CoV:   0.10028334378174394,
    resistance_multiplier:      1.0,
    source:        'results/FILTER_H13/bypass_analysis_sealed.json',
    validation:    'SIMULATION ONLY — NOT PHYSICALLY VALIDATED. Filter resistance is a single-point approximation. η(d_p) not applied.',
  },

  PARTICLE_PHASE12B: {
    case_id:       'PARTICLE_PHASE12B',
    display_name:  'Phase 12B — Particle Tracking (CASE_M_SEALED)',
    geometry:      'GEO_C + CASE_M_SEALED (frozen velocity field, timestep 5000)',
    solver:        'pvpython: equilibrium-slip Euler integration, dt=0.004 s, KDTree nearest-neighbour',
    phase:         'Phase 12B',
    status:        'POST_PROCESSED',
    caveats:       'One-way coupled, non-reacting, dilute. No turbulent dispersion. Equilibrium-slip only (Stokes + Cunningham settling). Frozen RANS field (partially non-converged). FILTER ARRIVAL ≠ FILTER CAPTURE. η(d_p) not available. Mass-flow-weighted seeding not applied.',

    // From results/PARTICLE_CFD/particle_arrival_fractions.json (exact values)
    n_seeds:            224,
    n_seed_candidates:  324,
    seed_x_m:           0.010,
    dt_s:               0.004,
    max_time_s:         6.0,
    rho_p_kg_m3:        1200.0,

    // Per-size summary (exact from JSON)
    sizes: {
      '0p3um': {
        label: '0.3 µm', dp_um: 0.3,
        cunningham_cc:          1.567526959757806,
        tau_p_us:               0.5225089865859354,
        v_settle_mm_s:          0.005125813158408025,
        stokes_number:          5.225089865859353e-6,
        n_filter_arrival:       139,
        n_frame_deposit:        14,
        n_wall_deposit:         71,
        n_recirculation:        0,
        filter_arrival_fraction: 0.6205357142857143,
        frame_deposit_fraction:  0.0625,
        wall_deposit_fraction:   0.3169642857142857,
      },
      '1um': {
        label: '1 µm', dp_um: 1.0,
        cunningham_cc:          1.1659366915083549,
        tau_p_us:               4.318284042623536,
        v_settle_mm_s:          0.042362366458136895,
        stokes_number:          4.318284042623536e-5,
        n_filter_arrival:       139,
        n_frame_deposit:        14,
        n_wall_deposit:         71,
        n_recirculation:        0,
        filter_arrival_fraction: 0.6205357142857143,
        frame_deposit_fraction:  0.0625,
        wall_deposit_fraction:   0.3169642857142857,
      },
      '2p5um': {
        label: '2.5 µm', dp_um: 2.5,
        cunningham_cc:          1.0663696000189187,
        tau_p_us:               24.684481481919416,
        v_settle_mm_s:          0.2421547633376295,
        stokes_number:          0.0002468448148191942,
        n_filter_arrival:       139,
        n_frame_deposit:        14,
        n_wall_deposit:         71,
        n_recirculation:        0,
        filter_arrival_fraction: 0.6205357142857143,
        frame_deposit_fraction:  0.0625,
        wall_deposit_fraction:   0.3169642857142857,
      },
      '10um': {
        label: '10 µm', dp_um: 10.0,
        cunningham_cc:          1.0165924,
        tau_p_us:               376.51570370370365,
        v_settle_mm_s:          3.693619053333333,
        stokes_number:          0.003765157037037037,
        n_filter_arrival:       137,
        n_frame_deposit:        17,
        n_wall_deposit:         70,
        n_recirculation:        0,
        filter_arrival_fraction: 0.6116071428571429,
        frame_deposit_fraction:  0.07589285714285714,
        wall_deposit_fraction:   0.3125,
      },
    },

    trajectory_status: 'NOT EXPORTED — run tools/export_particle_trajectories.py to generate trajectory coordinates',
    source:     'results/PARTICLE_CFD/particle_arrival_fractions.json',
    script:     'scripts/simulation/phase12b_particle_tracking.py',
    validation: 'SIMULATION POST-PROCESSING ONLY. Not physically validated.',
  },

  // Earlier geometry variants — included for completeness
  GEO_A: {
    case_id: 'GEO_A', display_name: 'GEO_A (geometry variant)',
    status: 'PARTIALLY_CONVERGED',
    Q_m3_h: 1492.2644536996559, fan_static_Pa: 6.079173412495927,
    riser_reverse_pct: 17.294301727999354,
    criteria: { residuals: false, mass: true, flow_stability: true, fan_closure: true },
    source: 'results/GEOMETRY_OPTIMIZATION/GEO_A/metrics.json',
    validation: 'SIMULATION ONLY',
  },
  GEO_B: {
    case_id: 'GEO_B', display_name: 'GEO_B (geometry variant)',
    status: 'CONVERGED',
    Q_m3_h: 1486.018878227406, fan_static_Pa: 10.32829979002746,
    riser_reverse_pct: 25.2649685848618,
    criteria: { residuals: true, mass: true, flow_stability: true, fan_closure: true },
    source: 'results/GEOMETRY_OPTIMIZATION/GEO_B/metrics.json',
    validation: 'SIMULATION ONLY',
  },
};

// Active case for current viewer state
export const ACTIVE_CASE        = 'GEO_C';
export const ACTIVE_FILTER_CASE = 'CASE_M_SEALED';
export const ACTIVE_PARTICLE    = 'PARTICLE_PHASE12B';
