# D01 filter inquiry — ready to send, NOT SENT

**Superseded workflow:** the user declined supplier correspondence and requested internet-only preparation. Keep this as an unsent historical draft, not a task assigned to the user. See `D01_ONLINE_FILTER_OPTIONS.pdf` and `data/prototype_d01/online_filter_screen.json`. Dimensional erratum: the saved R01 CAD gasket is495.3mm outside/475.3mm inside; the490/470mm gasket description below was incorrect and must not be sent or used for fabrication. The cabinet aperture is470mm. Native CAD geometry was not changed.

3 October 2026. This asks for product information and a quotation, not an order or a manufacturing authorization.

**Suggested recipient route:** [Camfil India official contact](https://www.camfil.com/en-in/support-and-services/support/contact-locator). No stock, distributor relationship, price or delivery commitment has been verified. The user must approve sending or send this request directly. Do not enter personal details or submit a form without approval.

## Copyable inquiry

Subject: Two low-resistance particle filters for a student indoor air-cleaner prototype

Hello,

We are developing a custom indoor particle air-cleaner demonstrator and need two replaceable filters operating in parallel. Please recommend an exact product available for supply in India and provide a technical quotation. This is an inquiry, not an order.

- Quantity: two filters, plus a separately priced spare pair.
- Target grade: documented MERV13; please provide the exact classification/test report and any conditioned/discharged performance information. Do not describe F7 or an ISO16890 grade as automatically identical to MERV13.
- Current reference actual frame size: 495.3 x495.3 x44.45 mm. This is NOT a nominal20x20x2 inch dimension request. Please state actual dimensions and tolerances. A different size may be proposed, but cannot be ordered or fitted without revising our assembly.
- Each filter handles125–200 m3/h, with150 m3/h the first comparison duty. Total unit flow is twice the per-filter flow. Please provide pressure drop at125,150,175 and200 m3/h, or a supported curve spanning this interval, stating test conditions and whether pressure includes the complete frame/media assembly.
- Desired clean pressure drop:10 Pa or less at150 m3/h per filter, as a provisional engineering sourcing target. Our current assumed system model leaves only about14.5 Pa total allowance for each filter at that duty; it is not a certified operating margin or replacement limit. Please report actual data, not a promise to meet these figures.
- Please provide loading/resistance information, recommended replacement criteria, frame mass, permitted temperature/humidity, orientation, handling and whether cleaning is permitted. We will establish a system-specific replacement point; a catalogue final pressure must not be applied automatically to our low-pressure fans.
- Drawing needed: media opening, continuous flat sealing border on the cabinet-facing side, frame rigidity/clamping limitations and any integral gasket details. Our proposed cabinet opening is470 x470 mm with a10 mm wide gasket border (490 x490 mm outside); the retainer has a475 x475 mm opening. Please confirm what actually contacts the gasket/retainer. Do not modify a filter to our drawing without further approval.
- Please specify exact model/part/revision, country of manufacture, quantity available, lead time, minimum order, GST, freight and replacement-filter availability. Build city is not finalized: Pune, Hyderabad or Mumbai; please separate any destination-dependent charge.

Camfil AQ13 407051002 is a nominal-size lead from a US catalogue, not a required product or a confirmed India offering. A suitable India-supplied equivalent is welcome, with its own verified data. Please do not substitute another product silently.

Thank you.

## Research outcome / purchase hold

**No filter is selected or cleared for purchase.** The existing S&P990303 dimensional reference and CamfilAQ13 candidate still lack exact low-flow pressure and confirmed India supply. A newly checked India-listed EcoPleat ProSafe3GPPS-12242-F7 is287 x592 x48 mm, with a published950m3/h /75Pa rated point. It cannot be a direct replacement for the square D01 frame; one high-flow point does not establish resistance at150m3/h. It remains an alternative-format lead only. No CAD resize was made around it.

The AAF manufacturer brochure confirms a PREpleatM13 family and1/2/4-inch depths, but not the low-flow pressure and actual dimensional data needed here. An assertion of low resistance is not a numerical curve. No unverified product is promoted to the BOM based on that description.

**Useful conclusion:** public catalogue research has not closed the filter decision. A supplier response or measured exact filter is now needed; repeatedly searching the same catalogues is not progress. The inquiry above is ready, but has not been transmitted.

## Returned-data checker

`scripts/analysis/d01_filter_offer_check.py` accepts a CSV with headers `per_filter_flow_m3h,pressure_Pa`, a source reference and an exact part identifier. It checks the supplied curve at the D01 comparison duties, never extrapolates, rejects invalid/duplicate/decreasing points and preserves existing output files. Use separate clean and loaded curves. Ten synthetic tests exercise the arithmetic and refusal rules; none are physical measurements.

Example command (replace placeholders with real files/evidence):

```powershell
& '<existing Python executable>' scripts/analysis/d01_filter_offer_check.py '<supplier_curve.csv>' --part '<exact part and revision>' --source '<manufacturer document and date>' --output '<new_result.json>'
```

An arithmetic result within the assumed allowance is not a purchase approval, actual-fit check, efficiency verification or performance guarantee. The aqi-build-review skill required these boundaries and comparison at the same per-filter flow.

## Sources checked 2026-10-03

- [India EcoPleat ProSafe catalogue](https://www.camfil.com/en-in/products/general-ventilation-filters/panel-filters/ecopleat/ecopleat-prosafe-_-66818): indexed regional product table; direct retrieval intermittent. Confirm current revision with supplier. This is a catalogue lead, not a live-stock observation.
- [AAF official pleated-filter brochure](https://aafterms.aafintl.com/-/media/files/aaf/commercial-and-industrial/us-products/pleated-filters/pleat_panel-brochure-afp-1-102b.pdf), page5, locally archived `data/prototype_d01/sources/AAF_pleated_brochure.pdf`; family-level information only.
- Earlier archived S&P and CamfilAQ13 documents and numeric fan evidence are indexed in the adjacent README. OEM documents do not confer an open-source design licence.
