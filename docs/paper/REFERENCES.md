# AQI Tower — Reference Material

Updated: 3 October 2026

This file lists the sources behind the conference paper (`AQI_Tower_IEEE_Paper.docx`) and the project work it summarises. Part A matches the numbered references in the paper. Part B lists the source documents archived inside this repository. Part C lists the main external sources cited in the engineering documents.

Related lists that already exist:

- `docs/build/SOURCES_AND_TOOLS.md`: sources and tool choices for the physical build planning.
- `reports/AQI_TOWER_STAKEHOLDER_REPORT_SOURCES.md`: maps each number in the stakeholder report to its result file and JSON key.

Paywalled papers and standards are not stored in the repository. Use the DOI or ISBN to get them through the college library. Check every DOI and page number against the publisher page before submission.

## A. Paper references

| # | Reference | Where to get it | Used for |
|---|---|---|---|
| [1] | World Health Organization, *WHO Global Air Quality Guidelines: Particulate Matter (PM2.5 and PM10), Ozone, Nitrogen Dioxide, Sulfur Dioxide and Carbon Monoxide*, Geneva, 2021. | ISBN 978-92-4-003422-8, free at who.int | PM2.5 guideline of 5 µg/m³ (introduction) |
| [2] | R. J. Shaughnessy and R. G. Sextro, "What is an effective portable air cleaning device? A review," *J. Occup. Environ. Hyg.*, vol. 3, no. 4, pp. 169–181, 2006. | DOI 10.1080/15459620600580129 | Purifier effectiveness depends on airflow and efficiency |
| [3] | U.S. EPA, *Guide to Air Cleaners in the Home*, 2nd ed., EPA 402-F-08-004, 2018. | https://www.epa.gov/sites/default/files/2018-07/documents/guide_to_air_cleaners_in_the_home_2nd_edition.pdf | CADR meaning; particle vs gas cleaning |
| [4] | M. Grieves and J. Vickers, "Digital twin: Mitigating unpredictable, undesirable emergent behavior in complex systems," in *Transdisciplinary Perspectives on Complex Systems*, Springer, 2017, pp. 85–113. | DOI 10.1007/978-3-319-38756-7_4 | Digital twin prototype definition |
| [5] | W. Kritzinger et al., "Digital twin in manufacturing: A categorical literature review and classification," *IFAC-PapersOnLine*, vol. 51, no. 11, pp. 1016–1022, 2018. | DOI 10.1016/j.ifacol.2018.08.474 (open access) | Digital model / shadow / twin classes |
| [6] | F. Tao, H. Zhang, A. Liu and A. Y. C. Nee, "Digital twin in industry: State-of-the-art," *IEEE Trans. Ind. Informat.*, vol. 15, no. 4, pp. 2405–2415, 2019. | DOI 10.1109/TII.2018.2873186 | Survey of industrial digital twins |
| [7] | H. G. Weller, G. Tabor, H. Jasak and C. Fureby, "A tensorial approach to computational continuum mechanics using object-oriented techniques," *Computers in Physics*, vol. 12, no. 6, pp. 620–631, 1998. | DOI 10.1063/1.168744 | OpenFOAM reference paper |
| [8] | B. E. Launder and D. B. Spalding, "The numerical computation of turbulent flows," *Comput. Methods Appl. Mech. Eng.*, vol. 3, no. 2, pp. 269–289, 1974. | DOI 10.1016/0045-7825(74)90029-2 | Standard k–ε turbulence model |
| [9] | W. C. Hinds, *Aerosol Technology*, 2nd ed., Wiley, 1999. | ISBN 978-0-471-19410-1 (library) | Particle capture gap at 0.1–1 µm; water spray rejection |
| [10] | EN 1822-1:2019, *High efficiency air filters (EPA, HEPA and ULPA) – Part 1*. CEN, 2019. | Paid standard (BIS/CEN member bodies) | HEPA classification at MPPS |
| [11] | Tempest Brisa open-source air purifier (CC0). | https://github.com/obife29/Tempest-Brisa-Open-Source; archived copy in `data/prototype_d01/sources/` | Precedent for the D01 PC-fan filter box |
| [12] | J. Ahrens, B. Geveci and C. Law, "ParaView: An end-user tool for large data visualization," in *The Visualization Handbook*, Elsevier, 2005, pp. 717–731. | ISBN 978-0-12-387582-2 (library) | pvpython export tool |
| [13] | three.js JavaScript 3D library, r167. | https://threejs.org | Web viewer |
| [14] | FreeCAD 1.1. | https://www.freecad.org | Parametric CAD |
| [15] | Systemair, KVO duct fan technical data sheet. | `data/fans/Systemair_Fans_KVO_Data_sheet_Eng.pdf` (in repo) | Fan curve used in the CFD |

## B. Source documents archived in this repository

These are the actual files the calculations used. OEM documents are kept for traceability only; they are not licensed for redistribution.

| Folder | Files | What they support |
|---|---|---|
| `data/fans/` | `Systemair_Fans_KVO_Data_sheet_Eng.pdf`, `KVO_datasheet_page1–4.png`, `systemair_KVO_250.json`, ebm-papst curve JSON files | KVO 250 fan curve (6 points) and alternative fan candidates |
| `data/fans/sources/` | `SP_TD_SILENT_ECOWATT_review_2026-10-02.pdf` | Soler & Palau comparison fan (fan duty decision) |
| `data/filters/` | `freudenberg_SF13B_593x593x292.json`, `HEPA_EFFICIENCY_EVIDENCE.md`, `biochar_candidates.json` | H13 HEPA rated point (300 Pa at 2.84 m/s), efficiency evidence audit, carbon media candidates |
| `data/prototype_d01/sources/` | `ARCTIC_P14_Max_Spec.pdf`, `ARCTIC_P14_Max_2D_20250124.pdf`, `ARCTIC_140mm_mounting_template.pdf`, `SP_MERV13_0303.pdf`, `Camfil_AQ13_2025.pdf`, `AAF_pleated_brochure.pdf`, `CEC_filter_pressure_223260.pdf`, `MeanWell_GST60A.pdf`, `Brisa_CC0_reference.dxf`, `Brisa_LICENSE.txt` | D01 fans, filters, power supply and the open-source precedent. `ARCTIC_P14_Max_PQ.pdf` is a failed HTML download and is not evidence |
| `data/hardware/sources/` | `Southco_C5_review_2026-10-02.pdf`, `Rogers_PORON_4701_40_review_2026-10-02.pdf` | HEPA service hatch latch and gasket screening |
| `data/monitoring/sources/` | `SPS30_review_2026-10-03.pdf`, `SDP8xx_digital_review_2026-10-03.pdf`, `TSI_8380_review_2026-10-03.pdf` | PM sensor, differential pressure sensor and flow hood for indoor tests |

## C. Main external sources cited in the engineering documents

### Standards and official guidance

- U.S. EPA, air cleaners and air filters in the home: https://www.epa.gov/indoor-air-quality-iaq/air-cleaners-and-air-filters-home
- WHO, types of air pollutants: https://www.who.int/teams/environment-climate-change-and-health/air-quality-and-health/health-impacts/types-of-pollutants
- ISO 16000-3 (formaldehyde sampling, DNPH method): https://www.iso.org/standard/81864.html
- ISO 10121-1 (gas-phase filter media test): https://standards.iteh.ai/catalog/standards/iso/beb61744-b460-4b88-b0a8-09bccbf182ea/iso-10121-1-2014
- ASHRAE 145.1 addendum (loose granular media test): https://www.ashrae.org/file%20library/technical%20resources/standards%20and%20guidelines/standards%20addenda/145_1_2015_a_20230228.pdf
- IEC 60335-2-65:2023 (air-cleaner appliance safety, scope only): https://webstore.iec.ch/en/publication/70378
- U.S. EPA TO-11A (formaldehyde by DNPH/HPLC): https://www.epa.gov/sites/default/files/2019-11/documents/to-11ar.pdf
- U.S. EPA Air Pollution Control Cost Manual, carbon adsorbers: https://www.epa.gov/sites/default/files/2018-10/documents/final_carbonadsorberschapter_7thedition.pdf
- OSHA formaldehyde method 52: https://www.osha.gov/sites/default/files/methods/osha-52.pdf
- NIOSH pocket guide, formaldehyde: https://www.cdc.gov/niosh/npg/npgd0293.html
- Health Canada, indoor air quality guidance: https://www.canada.ca/en/health-canada/services/publications/healthy-living/guidance-indoor-air-quality-professionals.html
- CPWD HVAC Specification 2024 (India): https://www.cpwd.gov.in/Publication/HVAC_Specification_2024.pdf
- NIST TN 1738, wind loads: https://www.nist.gov/publications/assessment-methods-determining-wind-loads-nist-tn-1738

### Fan and airflow engineering

- AMCA, "Straightening out fan curves": https://www.amca.org/educate/articles-and-technical-papers/amca-inmotion-articles/straightening-out-fan-curves.html
- AMCA, system effect: https://www.amca.org/educate/articles-and-technical-papers/amca-inmotion-articles/mitigating-system-effect-to-optimize-fan-performance-efficiency.html
- OpenFOAM 14 for Ubuntu: https://openfoam.org/download/14-ubuntu/
- Systemair fan instructions: https://shop.systemair.com/upload/assets/202341_FANS_INSTRUCTIONS_CE__A016_.PDF
- Soler & Palau TD-SILENT ECOWATT: https://statics.solerpalau.com/media/import/documentation/EN_TD-SILENT-ECOWATT.pdf
- ARCTIC P14 Max product page: https://www.arctic.de/en/P14-Max-Black/ACFAN00287A

### Carbon and formaldehyde research

- Calgon Carbon OVC 4×8 data sheet: https://www.calgoncarbon.com/app/uploads/DS-OVC4x815-EIN-E2.pdf
- Calgon Carbon FORMASORB: https://www.calgoncarbon.com/app/uploads/FORMASORB.pdf
- Research paper, DOI 10.1016/j.cej.2023.141979 (*Chemical Engineering Journal*, 2023)
- Research paper, DOI 10.1016/j.seppur.2016.06.029 (*Separation and Purification Technology*, 2016)
- Sensirion SFA30 laboratory testing guide: https://sensirion.com/media/documents/BA78378E/65F015E2/GAS_AN_SFA30_Laboratory_Testing_Guide_D1.pdf
- European Biochar Certificate guidelines: https://www.european-biochar.org/media/doc/2/wbc_1_1.pdf

### Measurement instruments

- TSI AccuBalance 8380 flow hood: https://tsi.com/getmedia/b057b3f8-c6c6-425f-ac69-c62a0dfb907e/8715-8380_AccuBalance_US_5001431?ext=.pdf
- Sensirion SDP810 (Tanotis India listing): https://www.tanotis.com/products/sensirion-sdp810-500pa-pressure-sensor-differential-500-pa-500-pa-2-7-v-5-5-v-sip

Every other URL cited in the project is in the individual documents under `docs/` and `docs/build/`. Search them for `https://`.
