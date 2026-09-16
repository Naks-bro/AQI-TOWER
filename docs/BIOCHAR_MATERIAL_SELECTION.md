# AQI Tower Phase 13 — Biochar Material Selection

**PHASE 13 — MATERIAL AND ADSORPTION EVIDENCE ONLY**  
**PHASE 13 HISTORICAL STATUS — TARGET GAS WAS NOT YET DEFINED**  
**PHASE 14 UPDATE — TARGET GAS: FORMALDEHYDE (HCHO); MATERIAL DECISION B**  
**BIOCHAR DATA STATUS: PARTIALLY READY**  
**No CFD run, CAD change, porous coefficient, or removal-performance claim**

## Purpose

The proposed carbon stage is intended for **pollutant-specific gas-phase adsorption**: selected volatile organic compounds (VOCs), organic vapors, or identified odor-causing gases. It is not a generic “AQI filter.” PM2.5 and PM10 remain particulate targets for the HEPA/prefilter system, not primary biochar targets.

An activated-carbon bed transfers gas molecules from air to a finite-capacity solid surface. Breakthrough occurs when the bed can no longer keep the downstream concentration below its selected limit. The US EPA therefore treats inlet/outlet VOC concentration, gas flow, temperature, relative humidity, pressure differential, and carbon activity as key performance indicators ([EPA carbon-adsorber guidance](https://www.epa.gov/air-emissions-monitoring-knowledge-base/monitoring-control-technique-activated-carbon-adsorber)).

### Material terms are not interchangeable

| Term | Meaning in this project | Engineering consequence |
|---|---|---|
| **BIOCHAR** | Biomass pyrolysis char without a demonstrated activation step for air adsorption | Properties can vary widely by feedstock and pyrolysis. It is not assumed to have activated-carbon pore structure or capacity. |
| **ACTIVATED CARBON** | Carbon intentionally activated by steam, CO₂, or a chemical route to develop adsorption pores | Can be an engineered granular or pelletized gas-phase medium if grade-specific data exist. |
| **ACTIVATED BIOCHAR** | Biomass-derived char given a documented post-activation or pore-development treatment | Research results apply only to that precursor and activation recipe. |
| **IMPREGNATED ADSORPTION MEDIA** | Activated carbon carrying reactive chemicals for a selected gas | Gas-specific chemistry, humidity response, heat release, compatibility, and disposal must be checked separately. |

The World Biochar Certificate defines biochar as biomass-derived porous carbon made by pyrolysis in low/no oxygen and notes that different applications require different quality characteristics ([WBC Guidelines v1.1](https://www.european-biochar.org/media/doc/2/wbc_1_1.pdf)). A peer-reviewed bamboo study likewise notes that ordinary biochar commonly has less-developed pore structure and that further physical or chemical activation produces material that is effectively activated carbon ([Rong et al., 2023](https://doi.org/10.1016/j.cej.2023.141979)).

## Candidate Materials

| Candidate | Required media distinction | Current evidence | Phase 13 role |
|---|---|---|---|
| Calgon Carbon OVC 4x8 | **C. Granulated activated carbon**, coconut shell, steam activated, non-impregnated | Manufacturer datasheet with particle specification and pressure-drop graph | **PRIMARY RESEARCH CANDIDATE** |
| Jacobi EcoSorb GX series | **C. Pelletized activated carbon**, exact grade not yet defined | Manufacturer family page; India plant/contact verified; no grade datasheet | **SECONDARY ALTERNATIVE**, conditional |
| Calgon Carbon FORMASORB | **E. Impregnated adsorption media**, coconut-shell activated carbon | Manufacturer datasheet; formaldehyde/aldehyde application; no pressure curve | **Phase 14 secondary formaldehyde-specific comparison**, conditional on exact-grade procurement and test evidence |
| SWP700 softwood-pellet biochar | **BIOCHAR**, no post-activation reported | Peer-reviewed benzene experiment | Research comparator only |
| RH550 rice-husk biochar | **A. Raw/research biochar**, no post-activation reported | Peer-reviewed MEK experiment | Research comparator only |
| R850 rice-husk activated carbon | **D. Activated biochar / biomass-derived activated carbon**, CO₂ activated | Peer-reviewed 16-VOC humidity experiment | Research comparator only |
| Bamboo BPGC | **D. Activated/modified biochar**, KOH-assisted catalytic graphitization | Peer-reviewed VOC and humidity results | Advanced research option, not procurement-ready |

## Pollutant Targets

**PHASE 14 SUPERSEDING DECISION: TARGET GAS — FORMALDEHYDE (HCHO / CH₂O, CAS 50-00-0).**

The Phase 13 statement that the target was not yet defined is retained as historical context. Phase 14 independently compared six candidates and froze HCHO. See [`PHASE14_FORMALDEHYDE_TARGET.md`](PHASE14_FORMALDEHYDE_TARGET.md) for concentrations, breakthrough definitions, safety, measurement, and experiment requirements.

The system requirement must name a compound or controlled mixture before adsorption performance can be designed. “VOC” is a class, not a single adsorbate. Evidence for benzene cannot be transferred to formaldehyde, MEK, H₂S, NO₂, ozone, or another gas.

Candidate target families for requirements work are:

- Non-polar organic vapors such as toluene or similar solvent vapors, for which non-impregnated microporous activated carbon may be relevant.
- Polar/small organic gases such as formaldehyde, which ordinary activated carbon may adsorb poorly and which can require specialized impregnated media. The EPA specifically identifies formaldehyde and methanol among compounds for which ordinary activated carbon can be less effective ([EPA Carbon Adsorbers chapter](https://www.epa.gov/sites/default/files/2018-10/documents/final_carbonadsorberschapter_7thedition.pdf)).
- Identified odor gases such as H₂S, mercaptans, or amines, which often require pollutant-specific impregnated or catalytic media rather than generic GAC.

NOx, SOx, CO, and ozone are not assigned to the carbon stage without species-specific evidence and an explicit requirement.

## Material Properties

| Candidate | Precursor and process | Surface area | Particle form | Bulk density | Pore information |
|---|---|---:|---|---:|---|
| OVC 4x8 | Coconut shell; high-temperature steam activation | NOT AVAILABLE | 4x8 US mesh, nominal range bounded by 4.75 and 2.36 mm screens | NOT AVAILABLE | High surface area/fine pores stated; no numeric distribution |
| FORMASORB | Coconut shell; steam activation plus impregnation | 1150 m²/g typical | 4x8 or 6x12 mesh | 600 kg/m³ typical | Numeric distribution NOT AVAILABLE |
| EcoSorb GX | Exact precursor/process NOT AVAILABLE | NOT AVAILABLE | Extruded pellet; diameter NOT AVAILABLE | NOT AVAILABLE | NOT AVAILABLE |
| SWP700 | Softwood pellets; pyrolysis at 700 °C | NOT AVAILABLE in accessible record | Final bed form NOT AVAILABLE | NOT AVAILABLE | NOT AVAILABLE |
| RH550 | Rice husk; pyrolysis at 550 °C | NOT AVAILABLE in accessible record | NOT AVAILABLE | NOT AVAILABLE | NOT AVAILABLE |
| R850 | Rice husk; carbonization + CO₂ activation at 850 °C | Numeric value NOT AVAILABLE in accessible record | NOT AVAILABLE | NOT AVAILABLE | Study identifies the highest surface/micropore area among its three samples |
| Bamboo BPGC | Bamboo; KOH-promoted nickel-catalyzed graphitization | 2181 m²/g | NOT AVAILABLE | NOT AVAILABLE | Micro-mesoporous; O/C = 0.038 |

Sources: [OVC 4x8 datasheet](https://www.calgoncarbon.com/app/uploads/DS-OVC4x815-EIN-E2.pdf), [FORMASORB datasheet](https://www.calgoncarbon.com/app/uploads/FORMASORB.pdf), [Jacobi product families](https://www.jacobi.net/products/), and the peer-reviewed papers recorded below.

## Adsorption Evidence

### Manufacturer/product evidence

- **OVC 4x8:** Calgon Carbon identifies it for vapor-phase VOC and odor removal and specifies carbon-tetrachloride activity of at least 60 wt%. That activity number is a standardized vapor-capacity indicator, not a removal percentage for the AQI Tower or for an unspecified VOC ([manufacturer datasheet](https://www.calgoncarbon.com/app/uploads/DS-OVC4x815-EIN-E2.pdf)). No compound-specific breakthrough curve was found.
- **FORMASORB:** the manufacturer identifies formaldehyde and other aldehydes as targets. The datasheet gives surface area, bulk density, mesh sizes, and a general gas-capacity specification, but no formaldehyde breakthrough capacity under tower conditions ([manufacturer datasheet](https://www.calgoncarbon.com/app/uploads/FORMASORB.pdf)).
- **EcoSorb GX:** Jacobi describes the GX series as extruded pellet carbon for general air treatment, but the public family page does not provide an exact grade or quantitative adsorption dataset ([Jacobi products](https://www.jacobi.net/products/)).

### Peer-reviewed experimental records

| Paper | Material and activation | Pollutant and test conditions | Reported result | Transfer limit |
|---|---|---|---|---|
| *Adsorption performance of standard biochar materials against volatile organic compounds in air: A case study using benzene and methyl ethyl ketone* — Kumar Vikrant, Ki-Hyun Kim, Wanxi Peng, Shengbo Ge, Yong Sik Ok (2020), DOI [10.1016/j.cej.2019.123943](https://doi.org/10.1016/j.cej.2019.123943) | 12 standard biochars from six feedstocks; 550 and 700 °C pyrolysis; no activation reported | Benzene and MEK at 1 Pa each; other mass, humidity, contact-time, and duration fields not available in the accessible record | Highest benzene capacity: SWP700, 2.9 mg/g. Highest MEK capacity: RH550, 43 mg/g. | Two specific gases and research chars; no packed-bed pressure loss or commercial specification |
| *Biochar for volatile organic compound (VOC) removal: Sorption performance and governing mechanisms* — Xueyang Zhang, Bin Gao, Yulin Zheng, Xin Hu, Anne Elise Creamer, Michael D. Annable, Yuncong Li (2017), DOI [10.1016/j.biortech.2017.09.025](https://doi.org/10.1016/j.biortech.2017.09.025) | 15 biochars, five feedstocks, pyrolyzed at 300/450/600 °C | Acetone, cyclohexane, toluene; gas-phase sorption; detailed concentration/mass/humidity unavailable in accessible abstract | Overall capacities 5.58–91.2 mg/g; both adsorption and partitioning mattered; performance retained through five sorption/desorption cycles | Wide variation demonstrates that “raw biochar” is not one reproducible medium |
| *Adsorption of volatile organic vapors by activated carbon derived from rice husk under various humidity conditions...* — Mei-Syue Li, Siang-Chen Wu, Yu-Huei Peng, Yang-Hsin Shih (2016), DOI [10.1016/j.seppur.2016.06.029](https://doi.org/10.1016/j.seppur.2016.06.029) | Rice-husk R850 activated carbon; carbonization then CO₂ activation at 1123 K | 16 VOCs by inverse gas chromatography at about 55% and 90% RH; mass/EBCT/duration unavailable in accessible record | log Kd reported as 4.0–6.1 at about 55% RH and decreased at 90% RH | Research sample, not a commercial packed bed; humidity effect is relevant but compound-specific values are needed |
| *Production of Activated Biochar Derived from Residual Biomass for Adsorption of Volatile Organic Compounds* — Elena David (2023), DOI [10.3390/ma16010389](https://doi.org/10.3390/ma16010389) | Rapeseed-cake and walnut-shell chars; KOH or H₂SO₄ treatment plus 800 °C; particles ≤1 mm | 1000 ppm toluene or acetone in N₂, 50 mL/min, about 20 °C, approximately 15 mg sample, 15 min; triplicate tests | Raw chars 16.76–26.65 mg/g; activated variants 51.28–166.72 mg/g depending on precursor/activation/VOC | Fine laboratory material; no bed pressure, humidity series, or commercial manufacturability demonstrated |
| *Bamboo-derived hydrophobic porous graphitized carbon for adsorption of volatile organic compounds* — Yang Rong, Cong Pan, Kexin Song, Jong Chol Nam, Feng Wu, Zhixiong You, Zhengping Hao, Jinjun Li, Zhongshen Zhang (2023), DOI [10.1016/j.cej.2023.141979](https://doi.org/10.1016/j.cej.2023.141979) | Bamboo-derived micro-mesoporous graphitized carbon, KOH-assisted nickel-catalyzed route | Toluene, cyclohexane, ethanol under dry and 80% RH conditions; accessible record does not provide flow, concentration, mass, EBCT, or duration | Dry capacities 6.7, 3.8, and 2.4 mmol/g; at 80% RH, toluene and cyclohexane retained 82% and 66% of dry capacity; ethanol uptake rose 33% | Advanced synthesis, no pressure-loss data, India supply, scale-up, or nickel-management plan |

Laboratory capacities are not guaranteed removal percentages. They cannot be transferred across gases, concentrations, relative humidities, flow rates, bed sizes, or media production routes.

## Pressure-Drop Evidence

Only OVC 4x8 currently has candidate-specific pressure-loss information:

- The official OVC datasheet contains a **typical pressure-drop graph** for 4x8 granular carbon at 70 °F and 15 psia, with loose/dense packing context. Calgon instructs designers to use dense-packed pressure loss because the bed settles in service ([OVC 4x8 datasheet](https://www.calgoncarbon.com/app/uploads/DS-OVC4x815-EIN-E2.pdf)).
- The graph is not tabulated. No points or coefficients were digitized in Phase 13.
- The plotted superficial-velocity range ends near 110 ft/min, approximately 0.56 m/s. If a carbon bed used the current 0.3516 m² filter-face area, the existing modelled face velocity would be 1.053 m/s—outside the graph range. Extrapolation is not defensible.
- OVC bulk density and bed void fraction are absent from the retrieved datasheet, preventing a fully parameterized Ergun model.

For FORMASORB, EcoSorb GX, SWP700, RH550, R850, and bamboo BPGC:

**NOT AVAILABLE — REQUIRES EXPERIMENT.**

The International Activated Carbon industry test method describes pressure drop as a function of gas velocity and reports it per unit bed length, using a packed column and multiple measured flow points ([industry test method](https://www.activatedcarbon.org/wp-content/uploads/2025/02/Test_method_for_Activated_Carbon_86.pdf)). This is the appropriate basis for the proposed bench test.

## Moisture Considerations

Humidity is a first-order design variable, not a footnote:

- EPA guidance states that water competes for activated-carbon adsorption sites and that high relative humidity can reduce capacity; small/polar VOCs can be especially difficult for ordinary carbon ([EPA Carbon Adsorbers chapter](https://www.epa.gov/sites/default/files/2018-10/documents/final_carbonadsorberschapter_7thedition.pdf)).
- The R850 rice-husk experiment observed lower adsorption coefficients when RH increased from approximately 55% to 90% ([Li et al., 2016](https://doi.org/10.1016/j.seppur.2016.06.029)).
- The bamboo BPGC study demonstrated better—but not complete—capacity retention for selected non-polar VOCs at 80% RH ([Rong et al., 2023](https://doi.org/10.1016/j.cej.2023.141979)).
- An impregnated medium may respond differently because water can participate in or inhibit its chemistry. No generic humidity correction is permitted.

If the proposed water stage is ever placed upstream of an adsorption bed, moisture carryover would require independent validation. No stage order is selected in Phase 13.

## Manufacturing Considerations

- **OVC 4x8 GAC:** controlled granule distribution, high hardness (97 minimum), low ash (3 wt% maximum), and thermal-reactivation statement support repeatable handling. A screen/support layer, dust containment, seal, and service cassette would still be required in a future design.
- **Pelletized activated carbon:** an exact Jacobi EcoSorb GX grade could offer consistent geometry, but no pressure-loss advantage is assumed until a datasheet or test confirms it.
- **Raw biochar:** feedstock identity and pyrolysis temperature are insufficient specifications. Batch quality would also require particle-size distribution, ash, volatiles, moisture, bulk density, surface area/pore distribution, dust generation, contaminants, and gas-specific breakthrough testing.
- **Activated/modified biochar:** KOH, acid, or nickel-assisted routes introduce washing, residual-chemical, wastewater, corrosion, worker-safety, and quality-control requirements. These are not suitable for informal student manufacture without institutional laboratory procedures.
- **Safety:** the OVC manufacturer warns that wet activated carbon can deplete oxygen in enclosed spaces. Carbon dust and combustible media require sealed handling, ventilation, ignition control, PPE, and appropriate supervision ([OVC safety statement](https://www.calgoncarbon.com/app/uploads/DS-OVC4x815-EIN-E2.pdf)).

## Availability

| Candidate | India status | Cost status |
|---|---|---|
| OVC 4x8 / FORMASORB | Kuraray lists activated carbon in India and identifies Calgon Carbon India LLP, but the exact grades, stock, MOQ, lead time, and reactivation service are **NOT CONFIRMED** ([Kuraray India product search](https://www.kuraray.com/in-en/products/search_name/), [Kuraray group entity list](https://www.kuraray.com/customer-privacy-notice/en/list_en.pdf)) | NO RELIABLE CURRENT PRICE — QUOTE REQUIRED |
| Jacobi EcoSorb GX | Jacobi operates an activated-carbon manufacturing plant and office in Coimbatore/Pollachi, but exact GX availability is **NOT CONFIRMED** ([Jacobi India contact](https://services.jacobi.net/contact/)) | NO RELIABLE CURRENT PRICE — QUOTE REQUIRED |
| Research biochars / activated biochars | No consistent air-treatment-grade Indian product matching the study recipes was verified | NOT AVAILABLE |

Do not treat generic e-commerce “activated charcoal” or soil biochar as an engineering substitute for a traceable air-treatment grade.

## Primary Candidate

### PRIMARY RESEARCH CANDIDATE

**Calgon Carbon OVC 4x8 — non-impregnated steam-activated coconut-shell GAC.**

Selection reasons:

1. Exact vapor-phase product identity and manufacturer datasheet.
2. Controlled 4x8 granule size and high hardness.
3. Official pressure-drop graph, including a dense-pack design instruction.
4. Suitable as a neutral benchmark before a pollutant-specific impregnated chemistry is selected.
5. Manufacturer states thermal reactivation is possible.

This is a **research selection only**. It is not final because target gas, product-specific breakthrough capacity, tower-range pressure loss, local lot availability, cost, bed depth, and safety/service arrangements remain unresolved.

## Alternative Candidate

### SECONDARY ALTERNATIVE

**Jacobi EcoSorb GX-series extruded activated carbon**, conditional on Jacobi Carbons India identifying an exact grade and providing:

- grade-specific precursor and activation route;
- pellet diameter and size distribution;
- surface area, bulk density, hardness, ash, and moisture;
- compound-specific adsorption/breakthrough data;
- pressure drop versus superficial velocity and bed depth;
- SDS, price, MOQ, lead time, and reactivation/disposal route.

**Phase 14 secondary comparison:** FORMASORB is now the formaldehyde-specific comparison material, conditional on exact-grade procurement, SDS, pressure testing, and matched HCHO breakthrough testing. It does not replace OVC 4×8 automatically.

## Data Gaps

1. **TARGET GAS RESOLVED IN PHASE 14: FORMALDEHYDE.** Final media suitability is still unknown until matched HCHO testing is complete.
2. Phase 14 now defines inlet concentrations, normalized outlet/breakthrough states, temperature, and RH. Real mixed-contaminant exposure and required service hours remain unknown.
3. No candidate has a product-specific breakthrough curve at AQI Tower conditions.
4. The OVC pressure graph is not tabulated and does not cover the existing 1.053 m/s face velocity.
5. Bulk density and void fraction are missing for OVC; exact properties are missing for EcoSorb GX.
6. Bed face area, depth, mass, packing procedure, and allowable pressure drop are requirements, not yet values.
7. India stock, exact grade, minimum order, lead time, price, sample availability, and spent-media service are unconfirmed.
8. Humidity sensitivity is unmeasured for the commercial candidates.
9. Dust release, ignition risk, off-gassing, contaminants, seal integrity, maintenance, and disposal are untested.
10. No adsorption percentage, service life, or integrated-system performance is established.

### Source-quality audit

| Evidence level | Sources used | Engineering use |
|---|---|---|
| A | OVC 4x8 and FORMASORB manufacturer datasheets | Product identity and listed physical/test properties only |
| B | Five peer-reviewed gas-phase adsorption studies | Mechanism, material-specific capacity, and humidity evidence under their stated experiments |
| C | EPA guidance, World Biochar Certificate, activated-carbon industry pressure-drop method, manufacturer family/contact pages | Definitions, test planning, safety, and availability channels |
| D | No D-level source used for a design value | Discovery only; excluded from engineering data |

Research stopped when each required evidence slot had either a primary/peer-reviewed source or an explicit gap. Additional generic supplier claims would not resolve the decisive missing items: named target gas, exact locally supplied grade, tower-range pressure loss, and matched-condition breakthrough data.
