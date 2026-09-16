/**
 * GEO_C tower engineering configuration.
 *
 * Coordinate mapping — CAD (x=flow-direction, y=depth, z=vertical)
 * to Three.js (x=flow-direction, y=vertical, z=depth):
 *   THREE_x = CAD_x − 0.350
 *   THREE_y = CAD_z − 0.925
 *   THREE_z = CAD_y − 0.400
 *
 * Sources:
 *   Geometry  — cad/parametric/PHASE8_GEOMETRY_AUDIT.json
 *   CFD zones — results/GEOMETRY_OPTIMIZATION/GEO_C/metrics.json
 *   Filter     — results/FILTER_H13/bypass_analysis_sealed.json
 *   Particles  — results/PARTICLE_CFD/particle_arrival_fractions.json
 */

export const TOWER = {
  label: 'AQI Tower — GEO_C',
  cad_file: 'cad/parametric/AQI_Tower_ConceptA_GEO_C.FCStd',
  cad_sha256: 'baec2027a16a7ab14a02662b8a39bbd5b7168770d9405e7382b93da9babd2a7b',
  cad_note: 'DESIGN EXPERIMENT PARAMETER — NOT PRODUCT REQUIREMENT',

  enclosure: {
    // Overall bounding box; Three.js centre = (0,0,0)
    center: [0, 0, 0],
    size:   [0.700, 1.850, 0.800],   // x (flow), y (vertical), z (depth)
    source: 'CAD',
    layer:  'enclosure',
  },

  zones: {
    DIRTY_PLENUM: {
      label:   'Dirty Plenum',
      source:  'CAD',
      // CAD: x=[0,0.130], z=[0,0.850], y=[0,0.800]
      center:  [-0.285, -0.500, 0],
      size:    [0.130, 0.850, 0.800],
      color:   0x8b4513,
      opacity: 0.12,
      layer:   'structure',
      info: {
        description:     'Pre-filter air chamber receiving inlet air.',
        cfd_speed_mean:  '0.997 m/s (CFD volume mean, CASE_M_SEALED)',
        cfd_volume:      '0.0588 m³',
        source_cfd:      'results/GEOMETRY_OPTIMIZATION/GEO_C/metrics.json',
      },
    },

    HEPA_FILTER: {
      label:   'HEPA Filter — Freudenberg SF13-B-0593×0593×292',
      source:  'ENGINEERING',
      // Physical dims: 593×593×292 mm (width × height × depth in flow direction)
      // Centre in flow: CAD x≈0.130–0.422 m → THREE_x≈−0.074
      // Face centred in cross-section: CAD z≈0.500, y≈0.400
      center:  [-0.074, -0.425, 0],
      size:    [0.292, 0.593, 0.593],
      color:   0x4a9eff,
      opacity: 0.55,
      layer:   'filter',
      info: {
        product:            'Freudenberg SF13-B-0593×0593×292',
        grade:              'H13 HEPA',
        size_mm:            '593 × 593 × 292 mm (gross)',
        face_velocity_cfd:  '1.053 m/s mean (CFD CASE_M_SEALED)',
        delta_P_cfd:        '111.2 Pa (single-point calibrated CFD model)',
        bypass_sealed:      '~0% (bypassSeal baffle applied)',
        status:             'SELECTED RESEARCH COMPONENT / NOT PHYSICALLY VALIDATED',
        warning:            'CFD ΔP is a single-point APPROXIMATION. Filter not validated at this operating point.',
        source_cfd:         'results/FILTER_H13/bypass_analysis_sealed.json',
      },
    },

    CLEAN_PLENUM: {
      label:   'Clean Plenum',
      source:  'CAD',
      // CAD: x=[0.422,0.500], z=[0,0.450], y=[0,0.800]
      center:  [0.111, -0.700, 0],
      size:    [0.078, 0.450, 0.800],
      color:   0x20a060,
      opacity: 0.10,
      layer:   'structure',
      info: {
        description:    'Post-filter plenum; air turns upward toward riser.',
        cfd_speed_mean: '1.060 m/s (CFD volume mean)',
        cfd_volume:     '0.0756 m³',
        source_cfd:     'results/GEOMETRY_OPTIMIZATION/GEO_C/metrics.json',
      },
    },

    TURN_STEP_01: {
      label:   'Turn Step 1',
      source:  'CAD',
      // CAD: x=[0.500,0.590], z=[0.450,0.850], y=[0.150,0.650]
      center:  [0.195, -0.275, 0],
      size:    [0.090, 0.400, 0.500],
      color:   0x2080c0,
      opacity: 0.12,
      layer:   'structure',
      info: {
        description:    'First step of two-step turning chamber. Redirects horizontal flow upward.',
        cad_x_mm:       '500–590 mm',
        cad_z_mm:       '450–850 mm',
        cfd_speed_mean: '1.461 m/s (CFD volume mean)',
        source_cfd:     'results/GEOMETRY_OPTIMIZATION/GEO_C/metrics.json',
      },
    },

    TURN_STEP_02: {
      label:   'Turn Step 2',
      source:  'CAD',
      // CAD: x=[0.590,0.690], z=[0.650,0.850], y=[0.150,0.650]
      center:  [0.290, -0.175, 0],
      size:    [0.100, 0.200, 0.500],
      color:   0x2080c0,
      opacity: 0.12,
      layer:   'structure',
      info: {
        description:    'Second turning step; completes flow redirection into vertical clean riser.',
        cad_x_mm:       '590–690 mm',
        cad_z_mm:       '650–850 mm',
        cfd_speed_mean: '1.053 m/s (CFD volume mean)',
        source_cfd:     'results/GEOMETRY_OPTIMIZATION/GEO_C/metrics.json',
      },
    },

    CLEAN_RISER: {
      label:   'Clean Riser',
      source:  'CAD',
      // CAD: x=[0.260,0.690], z=[0.850,1.850], y=[0.150,0.650]
      center:  [0.125, 0.425, 0],
      size:    [0.430, 1.000, 0.500],
      color:   0x20c070,
      opacity: 0.10,
      layer:   'structure',
      info: {
        description:    'Vertical clean air column; air rises to fan after filtration.',
        cfd_speed_mean: '2.046 m/s (CFD volume mean)',
        riser_inner_x:  '260 mm (CAD parameter)',
        riser_top_z:    '1850 mm (CAD parameter)',
        cfd_volume:     '0.215 m³',
        source_cfd:     'results/GEOMETRY_OPTIMIZATION/GEO_C/metrics.json',
      },
    },

    FAN_KVO250: {
      label:   'Fan — Systemair KVO 250',
      source:  'SCHEMATIC',
      // Cylinder placeholder at top of riser; CAD z≈1.70 m
      center:  [0.125, 0.750, 0],
      size:    [0.150, 0.150, 0.250],   // not used (cylinder overrides)
      color:   0xe0c040,
      opacity: 0.75,
      layer:   'fan',
      isCylinder: true,
      cylinderRadius: 0.125,
      cylinderHeight: 0.150,
      info: {
        product:   'Systemair KVO 250',
        type:      'Centrifugal inline fan, 250 mm',
        cfd_Q:     '1332.2 m³/h (CASE_M_SEALED operating point)',
        status:    'CURRENT CFD FAN CANDIDATE',
        warning:   'Fan geometry shown SCHEMATICALLY. Mounting and duct connection not finalised.',
        source_cfd:'results/CFD_V01_FAN/metrics.json',
      },
    },

    CARBON_STAGE: {
      label:   'Carbon Stage (Provisional)',
      source:  'SCHEMATIC',
      // Upstream of HEPA — schematic placeholder, NOT in CFD model
      center:  [-0.250, -0.425, 0],
      size:    [0.055, 0.593, 0.593],
      color:   0xc07830,
      opacity: 0.18,
      layer:   'schematic',
      info: {
        media:       'Calgon Carbon OVC 4×8 (research control)',
        grade:       'Coconut-shell GAC, 4×8 US mesh, steam-activated',
        bed_design:  'NOT FROZEN — placeholder only',
        status:      'PLANNED — BED DESIGN NOT FROZEN',
        warning:     'SCHEMATIC ONLY. Not in any CFD model. Bed depth, orientation, and column geometry are undecided.',
        procurement: 'RFQ pending — see docs/PHASE17B_OVC4X8_RFQ.md',
      },
    },

    WATER_STAGE: {
      label:   'Water Stage (Concept)',
      source:  'SCHEMATIC',
      // Ghost concept zone upstream of carbon
      center:  [-0.310, -0.425, 0],
      size:    [0.055, 0.593, 0.593],
      color:   0xa050c0,
      opacity: 0.08,
      layer:   'schematic',
      info: {
        description: 'Water-based cleaning stage — concept ghost only.',
        status:      'CONCEPT — FEASIBILITY NOT YET DECIDED',
        warning:     'CONCEPT GHOST. No engineering basis. Not in any model. Purely a placeholder.',
      },
    },
  },

  inlet: {
    // Left face opening — CAD x=0, z=[0,0.45], y=[0,0.8]
    center: [-0.350, -0.700, 0],
    planeH: 0.800,
    planeW: 0.450,
    color:  0x20d060,
    layer:  'airflow',
    label:  'Air Inlet',
    source: 'CAD',
  },

  outlet: {
    // Right face — CAD x=0.690, z=[1.60,1.85], y=[0.15,0.65]
    center: [0.340, 0.800, 0],
    planeH: 0.500,
    planeW: 0.250,
    color:  0xff6040,
    layer:  'airflow',
    label:  'Air Outlet (Fan Discharge)',
    source: 'SCHEMATIC',
  },
};

export const CFD_RESULTS = {
  case:    'CASE_M_SEALED',
  source:  'results/FILTER_H13/bypass_analysis_sealed.json',
  status:  'SIMULATED — PARTIAL NON-CONVERGED RANS (SIMPLEC, Phase 10B / 12B)',
  warning: 'All values are simulation results from an unvalidated model.',

  airflow_m3_h:              1332.2,
  airflow_m3_s:              0.37006,
  filter_delta_P_Pa:         111.2,
  filter_face_velocity_m_s:  1.053,
  bypass_fraction:           9.997e-10,

  particle: {
    model:   'Phase 12B: equilibrium-slip, 224 seeds, Euler dt=4 ms',
    warning: 'FILTER ARRIVAL FRACTION — NOT FILTER CAPTURE EFFICIENCY.',
    sizes: {
      '0.3 µm':  { filter_arrival: 0.6205, wall_deposit: 0.3170 },
      '1 µm':    { filter_arrival: 0.6205, wall_deposit: 0.3170 },
      '2.5 µm':  { filter_arrival: 0.6205, wall_deposit: 0.3170 },
      '10 µm':   { filter_arrival: 0.6116, wall_deposit: 0.3125 },
    },
  },
};
