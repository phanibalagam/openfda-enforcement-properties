# A15 Run 5 - label v2: LABEL v2 NOT FIT FOR USE

- **Label v2** (full text in section 0, written to `RUN5-RULES-PRESAMPLE.md` before any sample was drawn; rule-text SHA-256 `85f19758a6c8c1f2...`): COMPOUNDED-v2 = the compound stem OR a pharmacy/apothecary named (retail CVS and Good Neighbor excluded) OR outsourcing/503B OR an infusion pharmacy OR one of ten named preparers; BULK-v2 = substance terms (API, active pharmaceutical ingredient, drug substance, raw material, intermediate) OR "for (prescription) compounding / manufacturing use" OR kg/drum/bulk only when no finished-dosage-form word is present.
- **W1** pooled precision 98.33% (needs >= 85), lower Wilson 94.13% (needs > 70): **PASS**
- **W2** largest precision gap 5.0 pp; pairs breaching (> 20 pp AND non-overlapping 95% intervals): none: **PASS**
- **W3** largest miss-rate gap 32.5 pp; pairs breaching: E1-E3, E2-E3: **FAIL**
- **W4** highest era miss rate 40.0% (needs every era <= 25); eras breaching: E1, E2: **FAIL**
- **VERDICT: LABEL v2 NOT FIT FOR USE.** Criteria pre-registered in the run 5 brief; not adjusted.
- Precision by era: E1 100.0% (40/40, CI 91.24-100.0); E2 100.0% (40/40, CI 91.24-100.0); E3 95.0% (38/40, CI 83.5-98.62).
- Miss rate by era: E1 40.0% (16/40, CI 26.35-55.4); E2 32.5% (13/40, CI 20.08-47.98); E3 7.5% (3/40, CI 2.58-19.86).
- **Decomposition: NOT RUN.** The brief makes Part D conditional on v2 passing Part C. The fallback stands: the paper ships its first three findings with attribution reported as attempted and unresolved.

- Fresh samples: 507 records hand-read in runs 2-4 excluded; overlap with the 240 run 5 records = 0. Data SHA-256 `c6eb46526a3ad521...`, 17,975 records, confirmed first. Run 2 parser and v1 label imported, digests checked.
- No model, nothing fitted, no paper writing. `run5_label_v2.py` -> `run5_results.json`; marks in `run5_marks.json`.

---

## 0. Label v2 rule text (verbatim; identical to the pre-sample snapshot)

```
LABEL v2 = COMPOUNDED-v2 OR BULK-v2, applied to product_description (case-insensitive unless stated).

COMPOUNDED-v2 fires if ANY of:
  P1  the run 3 stem: compound, compounded, compounding, compounder, compounds.
  P2  the word pharmacy, pharmacies or apothecary, UNLESS the only such mention is in "CVS Pharmacy"
      or "Good Neighbor Pharmacy" (retail chains that appear in read records as distributors of
      finished OTC products). Implemented as: P2 matches after those two phrases are removed.
  P3  outsourcing, outsource, outsources, or the token 503B.
  P4  "home infusion", or "infusion" followed by pharmacy, service(s), options, center, centre,
      care, LLC or Inc.
  P5  one of ten preparer names that runs 3 and 4 showed to be compounders or outsourcing
      facilities: PharMEDium, SCA Pharmaceuticals, Avella, AnazaoHealth, US Specialty Formulations,
      Pharmakon, Qualgen, Belmar, GenoGenix, KRS Global Biotechnology.

BULK-v2 fires if ANY of:
  B1  the run 3 substance terms: "active pharmaceutical ingredient", the uppercase token API or APIs
      (case-sensitive), "drug substance", "raw material", "intermediate".
  B2  "for compounding", "for Rx compounding", "for prescription compounding", "for manufacturing use".
  B3  a kilogram quantity, the word drum(s), or the word bulk, ONLY IF the text contains none of
      these finished-dosage-form indicators: "pharmacy bulk package", tablet(s), caplet(s),
      capsule(s), softgel(s), syrup, spray, lotion, cream, ointment, towelette(s), wipe(s),
      sanitizer, injection, injectable, vial(s), syringe(s), suppositor-, drops.

LABEL v1 (run 3, unchanged, imported) = the run 3 compounding stem OR the run 3 bulk rule.

Provenance of each change. P2-P5 come from the run 4 Part B misses (pharmacies, infusion
pharmacies and outsourcing facilities named without the stem) and from run 3/4 records that name
the preparer. B2 comes from run 4 Part A (APIs sold "for prescription compounding") and Part B E2 #36
("For Manufacturing Use Only"). The B3 exclusion list comes from the nine run 4 E3 errors (bulk
containers of tablets, a bulk spray, drummed sanitizer, bulk towelettes, a pharmacy bulk package).
No record outside the run 2, run 3 and run 4 samples was read to write these rules.
Known limits carried in: P5 is a firm list and will not generalize beyond those firms; a raw
material in grams with no substance term (run 4 B E1 #23) is still missed; a retail botanical
sold by the kilogram (run 4 A E2 #38) is still flagged.
```

The script refuses to run if this text differs from `RUN5-RULES-PRESAMPLE.md`, which was written by `run5_label_v2.py --rules-only` before any run 5 sample was drawn. Year = year of `report_date`. Eras E1 2013-2016, E2 2017-2021, E3 2022-2026. Seeds A E1 51001, E2 51002, E3 51003; B E1 52001, E2 52002, E3 52003. Excluded: every record hand-marked in run 3 (240) and run 4 (240) and the 30 run 2 precision records, 507 distinct ids in all (29 of the run 2 records were not already in runs 3-4); overlap of the run 5 samples with them: 0. Employer-boundary replacements in quoted text: 2.

## A. Precision of label v2

Correct = the item really is a compounded preparation, bulk substance, API, raw material or intermediate.

| Era | v2-flagged records (fresh) | Correct | Precision % | Wilson 95% | Kind: compounded / bulk / both | Sub-rule: correct of fired |
|---|---|---|---|---|---|---|
| E1 | 3,058 | 40 / 40 | 100.0 | 91.24-100.0 | 33 / 7 / 0 | B1 7/7, B3 7/7, P1 22/22, P2 26/26, P5 4/4 |
| E2 | 1,837 | 40 / 40 | 100.0 | 91.24-100.0 | 37 / 3 / 0 | B1 1/1, B2 2/2, B3 2/2, P1 22/22, P2 19/19, P3 1/1, P4 1/1, P5 10/10 |
| E3 | 842 | 38 / 40 | 95.0 | 83.5-98.62 | 36 / 2 / 0 | B2 1/1, B3 2/4, P1 5/5, P2 24/24, P3 3/3, P4 3/3, P5 3/3 |
| pooled | | 118 / 120 | 98.33 | 94.13-99.54 | | |

### A-E1 (seed 51001)

| # | Record | Year | Sub-rules | v1 flags too | NDC | Mark | Full product_description |
|---|---|---|---|---|---|---|---|
| 1 | D-676-2015#6773 | 2015 | B1+B3 | yes | no | correct (bulk) | Floxuridine active pharmaceutical ingredient packaged in varying grams or kg in bags or drums, Attix Pharmaceuticals, 184 Front Street East, Unit 801, Toronto, Ontario M5A 4N3, Canada |
| 2 | D-789-2015#8574 | 2015 | B1+B3 | yes | no | correct (bulk) | Methyl 5-Aminolevulinate Hydrochloride active pharmaceutical ingredient packaged in varying grams or kg in bags or drums, Attix Pharmaceuticals, 184 Front Street East, Unit 801, Toronto, Ontario M5A 4N3, Canada |
| 3 | D-189-2014#5993 | 2013 | P1+P2 | yes | no | correct (compounded) | Lipotropic 50ml w/o methionine, Main Street Compounding Pharmacy, 126 East Main Street, Newbern, TN 38059, 888-658-6200 |
| 4 | D-1826-2015#6628 | 2015 | P5 | no | yes | correct (compounded) - outsourcing-facility admixture; carries an NDC | PHENYLephrine HCl, 20 mg added to 250 mL 0.9% Sodium Chloride Injection USP (80 mcg per mL), packaged in 250 ml bags, Rx only, PharMEDium Services, LLC, 12620 W. Airport Blvd., Sugar Land, TX 77478, NDC# 61553-156-50 |
| 5 | D-770-2015#9596 | 2015 | B1+B3 | yes | no | correct (bulk) | Losartan Potassium active pharmaceutical ingredient packaged in varying grams or kg in bags or drums, Attix Pharmaceuticals, 184 Front Street East, Unit 801, Toronto, Ontario M5A 4N3, Canada |
| 6 | D-634-2013#5771 | 2013 | P1+P2 | yes | no | correct (compounded) | Acetylcysteine 2 % Solution, Clinical Specialties Compounding Pharmacy, 318 Baston Road, Augusta, GA 30907 |
| 7 | D-0052-2017#8664 | 2016 | P5 | no | no | correct (compounded) | HYDROmorphone HCl, 1 mg per mL, in 0.9% Sodium Chloride, 1 mL Total Volume in a syringe, For IV Use, Rx only, PharMEDium, Product code 2T6165 |
| 8 | D-1757-2015#2324 | 2015 | P1+P2 | yes | no | correct (compounded) | Testosterone Cypionate 40 mg/ml (10 ml Sesame Oil), Injection, Multi-Dose Vial, Sterile, Room Temperature, The Compounding Pharmacy of America, Knoxville, TN |
| 9 | D-029-2014#7543 | 2013 | P1+P2 | yes | no | correct (compounded) | Adenosine Monophosphate, 50mg/ml 30ml, Main Street Compounding Pharmacy, 126 East Main Street, Newbern, TN 38059, 888-658-6200 |
| 10 | D-0004-2017#9806 | 2016 | P2 | no | no | correct (compounded) | Tri-Mix 18/1/10 (Papaverine 18mg, Phentolamine 1 mg, Prostaglandin 10 mcg/mL) packaged in 2.5 mL sterile vials, IM, Rx, The Apothecary Shoppe, Jenks, OK |
| 11 | D-046-2014#5828 | 2013 | P1+P2 | yes | no | correct (compounded) | B-12 mixture, Main Street Compounding Pharmacy, 126 East Main Street, Newbern, TN 38059, 888-658-6200 |
| 12 | D-554-2015#6349 | 2015 | B1+B3 | yes | no | correct (bulk) | Cabergoline active pharmaceutical ingredient packaged in varying grams or kg in bags or drums, Attix Pharmaceuticals, 184 Front Street East, Unit 801, Toronto, Ontario M5A 4N3, Canada |
| 13 | D-724-2013#4328 | 2013 | P1+P2 | yes | no | correct (compounded) | Disodium EDTA Injection, compounded by Olympia Pharmacy, Orlando, FL |
| 14 | D-1106-2015#4024 | 2015 | P1+P2 | yes | no | correct (compounded) | SODIUM TETRADECYL SULFATE (STERILE WATER) (30ML) 3.5% INJECTABLE, Advanced Compounding Pharmacy, 7225 Fulton Ave., North Hollywood, CA 91605 |
| 15 | D-1090-2016#7167 | 2016 | P1+P2 | yes | no | correct (compounded) | All citalopram Products, Rx Only, Compounded by RELIABLE DRUG/RELIABLE COMPOUNDING PHARMACY, 801 Irving St., SAN FRANCISCO, CA 94122. |
| 16 | D-0167-2015#7591 | 2014 | P2 | no | no | correct (compounded) | Tri-mix T50, 8.825 mg/0.29 mg/2.95 mcg/mL (papaverine, phentolamine mesylate, alprostadil) injectable packaged in a clear glass injectable vial, Martin Avenue Pharmacy, 1247 Rickert Dr, Naperville, IL. |
| 17 | D-860-2013#5221 | 2013 | P1+P2 | yes | no | correct (compounded) | Bacteriostatic Water for Injection, compounded by Pallimed Solutions Pharmacy, Woburn, MA |
| 18 | D-298-2014#8750 | 2013 | P1+P2 | yes | no | correct (compounded) | Testosterone Pellet 87.5mg, Main Street Compounding Pharmacy, 126 East Main Street, Newbern, TN 38059, 888-658-6200 |
| 19 | D-1254-2016#3639 | 2016 | P2 | no | no | correct (compounded) | HCL 2MG/ML (PF), 5ML Vials, MEDAUS PHARMACY |
| 20 | D-876-2013#5186 | 2013 | P1+P2 | yes | no | correct (compounded) | Testosterone Cypionate/Testosterone Enanthate Injection, compounded by Pallimed Solutions Pharmacy, Woburn, MA |
| 21 | D-1126-2016#9986 | 2016 | P1+P2 | yes | no | correct (compounded) | All ketamine and amitriptyline Products, Rx Only, Compounded by RELIABLE DRUG/RELIABLE COMPOUNDING PHARMACY, 801 Irving St., SAN FRANCISCO, CA 94122. |
| 22 | D-1031-2015#9053 | 2015 | P2 | no | no | correct (compounded) | Spironolactone 5 mg/mL Susp, Health Innov Pharmacy, 295 Pinehurst Ave, Southern Pines, NC 28387, (910) 246-5155 |
| 23 | D-0029-2017#6621 | 2016 | P5 | no | no | correct (compounded) | ePHEDrine Sulfate, 5 mg per mL, 25 mg per 5 mL, in 0.9% Sodium Chloride, Preservative Free, 5 mL Total Volume in a syringe, For IV Use, Rx only, PharMEDium, Product code 2R3301. |
| 24 | D-448-2015#9692 | 2015 | P1 | yes | no | correct (compounded) | Olathe Medical Center (KS) NICU TPN Starter: Ingredients per 80 ml, Trophamine 3g Dextrose 10%, Additives: Calcium Gluconate 250mg, compound vol: 250 ml, sterile injectable, Rx only, compounded drug, IV infusion bag packaged in a corrugated box, each container is lined with a polystyrene insert; CAPS, Allentown, PA. |
| 25 | D-1053-2013#6063 | 2013 | P2 | no | no | correct (compounded) | Magnesium Chl 200 mg/mL PF, 100 mL, Medaus Pharmacy 1-800-526-9183 |
| 26 | D-0126-2015#8895 | 2014 | P2 | no | no | correct (compounded) | Quad mix, 18 mg/0.2 mg/10 mcg/0.02 mg/mL (papaverine, phentolamine mesylate, alprostadil, atropine) injectable packaged in a clear glass injectable vial, Martin Avenue Pharmacy, 1247 Rickert Dr, Naperville, IL. |
| 27 | D-1535-2015#3475 | 2015 | P1+P2 | yes | no | correct (compounded) | Hyaluronic Acid Sodium 32 mg/ml + Lidocaine HCl 3 mg/ml Injection, ml Syringe, Sterile, Room Temperature, The Compounding Pharmacy of America, Knoxville, TN |
| 28 | D-918-2013#3726 | 2013 | P1+P2 | yes | no | correct (compounded) | Avastin, (0.05 ml, 1.25 mg/0.05ml), single unit dose syringes, Clinical Specialties Compounding Pharmacy, Augusta, GA |
| 29 | D-0065-2017#7351 | 2016 | P5 | no | no | correct (compounded) | lidocaine HCl, 2%, 40 mg per 2 mL, 2 mL Total Volume in a syringe, Rx only, PharMEDium, Product code 2R3112. |
| 30 | D-1397-2015#9175 | 2015 | P1 | yes | no | correct (compounded) | Glycerin (v/v) 72% Injection, 25 mL vial, Rx only, Liberty Drug Compound Center, 195 Main St., PO Box 267, Chatham, NJ 07928. |
| 31 | D-551-2013#13829 | 2013 | P1 | yes | no | correct (compounded) | Baclofen 1,000 mcg/mL Injectable, 20 mL and 40 mL vial, Compounded by The Compounding Shop, St. Petersburg, FL |
| 32 | D-1776-2015#3109 | 2015 | P1+P2 | yes | no | correct (compounded) | Tri-Mix (30/1/10) Injectable, The Compounding Pharmacy of America, Knoxville, TN |
| 33 | D-609-2015#7893 | 2015 | B1+B3 | yes | no | correct (bulk) | Dacarbazine active pharmaceutical ingredient packaged in varying grams or kg in bags or drums, Attix Pharmaceuticals, 184 Front Street East, Unit 801, Toronto, Ontario M5A 4N3, Canada |
| 34 | D-0122-2015#7693 | 2014 | P2 | no | no | correct (compounded) | Polyhexamethylene biguanide 0.02% opthalmic solution packaged in an opaque squeeze bottle eye dropper, Martin Avenue Pharmacy, 1247 Rickert Dr, Naperville, IL. |
| 35 | D-0501-2016#1614 | 2015 | P1+P2 | yes | no | correct (compounded) | TRI-EST Capsules, Rx, compounded by Life Science Pharmacy Inc., Harriman, NY |
| 36 | D-277-2013#3538 | 2013 | P1+P2 | yes | no | correct (compounded) | Progesterone in Olive Oil Injectable Balanced Solutions, Compounding Pharmacy a division ofAxium Healthcare Pharmacy, Inc., Lake Mary, FL 32746 |
| 37 | D-1672-2015#3166 | 2015 | P1+P2 | yes | no | correct (compounded) | Hydromorphone 35 mg/ml + Bupivacaine 10 mg/ml + Baclofen 1,500 mcg/ml + Clonidine 200 mcg/ml Intrathecal Solution, Sterile-Preservative Free, The Compounding Pharmacy of America, Knoxville, TN |
| 38 | D-522-2015#8028 | 2015 | B1+B3 | yes | no | correct (bulk) | Anastrozole active pharmaceutical ingredient packaged in varying grams or kg in bags or drums, Attix Pharmaceuticals, 184 Front Street East, Unit 801, Toronto, Ontario M5A 4N3, Canada |
| 39 | D-1736-2015#2797 | 2015 | P1+P2 | yes | no | correct (compounded) | Morphine 30 mg/ml Solution, Sterile-Preservative Free, The Compounding Pharmacy of America, Knoxville, TN |
| 40 | D-906-2015#6405 | 2015 | B1+B3 | yes | no | correct (bulk) | Sulfanilamide active pharmaceutical ingredient packaged in varying grams or kg in bags or drums, Attix Pharmaceuticals, 184 Front Street East, Unit 801, Toronto, Ontario M5A 4N3, Canada |

### A-E2 (seed 51002)

| # | Record | Year | Sub-rules | v1 flags too | NDC | Mark | Full product_description |
|---|---|---|---|---|---|---|---|
| 1 | D-0403-2017#7542 | 2017 | P1+P2 | yes | no | correct (compounded) | Testosterone Cypionate/Anastrozole Injectable, 200 mg/1 mg/mL, 10 mL vial, Compounded by Wells Pharmacy, Ocala, FL |
| 2 | D-0679-2018#2211 | 2018 | P2 | no | no | correct (compounded) | Estradiol 40 mg (SD) pellets in amber vial, Rx only, Partell Specialty Pharmacy, 5835 S. Eastern Ave. #101, Las Vegas, NV 89119 (702) 791-3800. |
| 3 | D-0837-2017#2983 | 2017 | P5 | no | no | correct (compounded) | Esmolol HCl all strengths, all dosage forms and all packaging, Rx Only, Avella of Houston, Houston, TX 77054 |
| 4 | D-1033-2017#7219 | 2017 | P5 | no | yes | correct (compounded) | Potassium Chloride 40 meq Added to Sodium Chloride 0.9% 250 mL, Rx only, SCA Pharmaceuticals 8821 Knoedl Ct Little Rock, AR 72205 ---- NDC# 70004-0833-40 |
| 5 | D-0373-2017#7046 | 2017 | P1+P2 | yes | no | correct (compounded) | MIC/B-COMP+LIDO 20 mg/40 mg/50 mg/10 mg/mL Injectable, 30 mL vial, Compounded by Wells Pharmacy, Ocala, FL |
| 6 | D-0728-2017#1598 | 2017 | P1+P2 | yes | no | correct (compounded) | HYDROXO-B12 5ML PBF MDV (CALIF) 10MG/ML INJ, Injection, 10mg/mL, RX only, 5mL Glass/Multiple Dose vial, Prepared by Key Compounding Pharmacy |
| 7 | D-0045-2018#9571 | 2017 | P1+P5 | yes | yes | correct (compounded) | Oxytocin 30 units added to 1000 mL Lactated Ringer's USP in 1000 mL bag Rx Only, Compounded by PharMEDium Services, LLC. 12620 W. Airport Blvd. #130 Sugar Land, TX 77478, NDC# 71019-243-04 |
| 8 | D-1414-2019#10718 | 2019 | P2 | no | yes | correct (compounded) | Dexamethasone Sodium Phosphate Preservative Free Sterile Solution for INJ, 24mg/mL, 1mL Sterile Single-Use Syringe, Rx only, Premier Pharmacy Labs, 8265 Commercial Way, Weeki Wachee, FL 34613, NDC: 69623-252-10, barcode 0 69623 25210 4. |
| 9 | D-0755-2017#3003 | 2017 | P1+P2 | yes | no | correct (compounded) | QUAD MIX 50/30/1/0.2 5ML MDV (CALIF) MCG/MG/MG/MG/ML INJ, Injection, 50mcg/30mg/1mg/0.2mg/mL, Rx only, 5 mL Glass/Multiple Dose vial, Prepared by Key Compounding Pharmacy |
| 10 | D-1256-2019#11200 | 2019 | P1 | yes | no | correct (compounded) | HCG (CHORIONIC GONADOTROPIN 1000 IU/ML PEP 25 mg/mL) inj 5 mL multidose vial compounded. Customceutical Compounding 4611 E. Shea Blvd. Bldg 3 180, Phoenix, AZ 85028 Ph. 480 516 0272 |
| 11 | D-0181-2018#7346 | 2018 | P5 | no | no | correct (compounded) | Hydroxocobalamin 1 mg/mL 30 mL Vial For IM Use, Rx Only, KRS Global Biotechnology, 791 Park of Commerce Blvd, Boca Raton, FL 33487. |
| 12 | D-0934-2018#4386 | 2018 | P2+P5 | no | yes | correct (compounded) | HEPARIN 25,000 Units in 5% Dextrose (Heparin Sodium, USP 25,000 Units, 5% Dextrose Inj., USP 250 mL) Volume: 255 mL. Single dose bag. Avella Specialty Pharmacy, 24416 N 19th Avenue, Pheonix AZ 85085. NDC 42852-729-25 |
| 13 | D-0128-2022#12497 | 2021 | P1+P2 | yes | no | correct (compounded) | MIC 20/40/50 /B COMPLEX +CHROM/CARN 25/25MG/ML+LIDO 20/40/50/25/25MG/ML+LIDO INJECTABLE, Rx only, Talon Compounding Pharmacy, 2950 Thousand Oaks Drive Ste 25, San Antonio, Texas 78247 |
| 14 | D-0277-2020#11733 | 2019 | P1 | yes | no | correct (compounded) | S-MIC 25/50/50MG/ML CYANO 1MG/ML MDV SOLN, RX Only, 30ml glass vial, Red Mountain Compounding Rx. |
| 15 | D-0715-2017#2522 | 2017 | P1+P2 | yes | no | correct (compounded) | DMSO 6.25% OPHTH., 6.25%, Rx only, 15 mL plastic/Multiple Dose bottle, Prepared by Key Compounding Pharmacy |
| 16 | D-0095-2020#11376 | 2019 | P5 | no | yes | correct (compounded) | Sermorelin, 3 mg/GHRP6, 3 mg/GHRP2, 3 mg/Vial, For SC Use, Vial-Lyophilized, Rx Only, KRS Global Biotechnology 791 Park of Commerce Blvd, Boca Raton, FL 33487. NDC 3321673816 |
| 17 | D-0255-2020#11827 | 2019 | P1 | yes | no | correct (compounded) | S-VIT B COMPLEX (1/3/5/6/12A) MDV INJ 100/2/2/100/1MG/ML, 30 ML glass vial. Red Mountain Compounding Rx |
| 18 | D-0116-2022#13061 | 2021 | P1+P2 | yes | no | correct (compounded) | GOAL-GLUTAMINE 75MG/ORNITHINE 75MG/ARGININE 150MG/LYSINE 150MG+LIDOCAINE 10MG/ML 75MG/75MG/150MG/150MG/10MG/ML INJECTABLE, Rx only, Talon Compounding Pharmacy, 2950 Thousand Oaks Drive Ste 25, San Antonio, Texas 78247 |
| 19 | D-0127-2019#10466 | 2018 | B1+B3 | yes | no | correct (bulk) | Irbesartan Bulk Active Pharmaceutical Ingredient. |
| 20 | D-0666-2018#2681 | 2018 | P2 | no | no | correct (compounded) | Testosterone 40 mg pellet packaged in amber vial, Rx only, Partell Specialty Pharmacy, 5835 S. Eastern Ave. #101, Las Vegas, NV 89119 (702) 791-3800 |
| 21 | D-0267-2020#11605 | 2019 | P1 | yes | no | correct (compounded) | S-HYDROXOCOBA 5000MCG/ML INJ, 30ML glass vial, Red Mountain Compounding Rx |
| 22 | D-0658-2018#1755 | 2018 | P2 | no | no | correct (compounded) | TM #4 (ALP 20/PAPAV/PHENT 2), 3 mL amber vial, Rx only, Partell Specialty Pharmacy, 5835 S. Eastern Ave. #101, Las Vegas, NV 89119 (702) 791-3800 |
| 23 | D-0028-2022#12535 | 2021 | P1 | yes | no | correct (compounded) | Calcium Chloride, 100 mg/mL MDV INJ, Rx only, Red Mountain Compounding Rx |
| 24 | D-1811-2019#15029 | 2019 | P4 | no | no | correct (compounded) - patient dose syringe of a commercial biologic prepared by an infusion pharmacy | RomiPLOStim 700 MCG/ 1.4 ML SQ SYR, Rx Only, Infusion Options, Inc. 5924 13the Ave, Brooklyn, NY 11219-4934, 718-283-7233 |
| 25 | D-0144-2022#13131 | 2021 | P1+P2 | yes | no | correct (compounded) | SERMORELIN ACETATE 6MG/IPAMORELIN 6MG - LYOPHILIZED 6MG/6MG VIAL, Rx only, Talon Compounding Pharmacy, 2950 Thousand Oaks Drive Ste 25, San Antonio, Texas 78247 |
| 26 | D-0045-2020#11651 | 2019 | P5 | no | yes | correct (compounded) | L-Carnitine 27 mL Fill in a 30 mL Vial, For Dilution Use Only, 2,025 mg/27 mL (75 mg/mL) Rx Only, KRS Global Biotechnology 791 Park of Commerce Blvd, Boca Raton, FL 33487. NDC 3321676396 |
| 27 | D-1163-2019#4735 | 2019 | P1+P2 | yes | no | correct (compounded) | Methylprednisolone 1% PF Ophthalmic, 3 mL Droppers, Anderson Compounding Pharmacy 310 Bluff City Hwy, Bristol, TN. |
| 28 | D-0660-2017#6854 | 2017 | P1+B2+B3 | yes | yes | correct (bulk) | Levonorgestrel Non-Micronized, USP, Bulk, Rx only, For Prescription Compounding, Manufactured by Qinhuangdao Zizhu Pharmaceutical Co., Ltd., Qinhuangdao 066004, China (NDC 44132-012-01), |
| 29 | D-1033-2019#11060 | 2019 | P5 | no | yes | correct (compounded) | Morphine Sulfate 30 mg/30 mL (1 mg/mL) Injectable Solution Morphine Sulfate 30 mg 0.9% Sodium Chloride QS 30 mL Sterile singe use syringe, NDC: 42852-241-63 Avella of Houston 9265 Kirby Dr., Houston, TX 77054 (877) 794-0404 |
| 30 | D-0976-2017#2163 | 2017 | P5 | no | yes | correct (compounded) | Potassium PHOSphate added to 250 mL 0.9% Sodium Chloride 10 mMol (14.67 mEq K+) Total Approximate Volume 254 mL, Rx only, SCA Pharmaceuticals, Little Rock, AR 72205, NDC 70004-0840-40 |
| 31 | D-0226-2019#1508 | 2018 | P5 | no | yes | correct (compounded) | Estradiol 12.5mg pellet, 1 count (NDC 69761-012-01), 6 count (NDC 69761-012-06), 12 count (NDC 69761-012-12), and 30 count (NDC 69761-012-30) vials, Rx Only, Qualgen, LLC, Edmond, OK 73013 |
| 32 | D-0198-2020#11845 | 2019 | P1 | yes | no | correct (compounded) | S-AMITRIPTYLINE 10MG/ML MDV INJ SOLN, 30ML, glass vial, Rx Only, Red Mountain Compounding RX |
| 33 | D-0481-2018#7273 | 2018 | P1+B2 | yes | yes | correct (bulk) | Cyclobenzaprine HCl USP for prescription compounding, packaged in a) 25g (NDC 58597-8011-4), b)100g (NDC 58597-8011-6); c) 500 g (NDC 58597-8011-7); d)1000g (NDC 58597-8011-8), RX only, packed by American Pharmaceutical Ingredients, LLC 6650 Highland Road, Waterford, MI 48327 |
| 34 | D-0138-2018#9712 | 2018 | P1+P3 | yes | yes | correct (compounded) | Fentanyl 2 mcg/mL and ropivacaine 0.2% in 0.9% Sodium Chloride 150 mL, 150 mL bag, This is a compounded injectable drug; Rx only; Hospital/office use only. SSM St. Clare Outsourcing Facility, Fenton, MO. --- NDC: 88883-4272-01 |
| 35 | D-0048-2022#12668 | 2021 | P1 | yes | no | correct (compounded) | TEST CYP/PROP/DECA-NAN 125MG/ML (80/10/10) IN SESAME OIL, Rx only, Red Mountain Compounding Rx |
| 36 | D-0670-2018#2223 | 2018 | P2 | no | no | correct (compounded) | Testosterone/Anastrozole 200 mg/20 mg pellets packaged in amber vial, Rx only, Partell Specialty Pharmacy, 5835 S. Eastern Ave. #101, Las Vegas, NV 89119 (702) 791-3800. |
| 37 | D-1186-2020#4910 | 2020 | P2 | no | no | correct (compounded) | Bi-Est (1:1) Progest/Test 0.5 mg/40 mg/10.5 mg/mL Cream 30 gm tube, Rx, The Medicine Shoppe Pharmacy, Port Charlotte, FL |
| 38 | D-1469-2019#5063 | 2019 | P2 | no | no | correct (compounded) | Testosterone Cypionate 150 mg/mL Sesame Oil Injection, 12 mL vial, Rx only, First Pharma Associates dba Riverpoint Pharmacy, Spokane, WA 99205, (509) 343- 6252. |
| 39 | D-0342-2017#9099 | 2017 | P1+P2 | yes | no | correct (compounded) | B-complex + Vit C 20 mg/mL Injectable, 30 mL vial, Compounded by Wells Pharmacy Network, LLC, Ocala, FL |
| 40 | D-0468-2019#10739 | 2019 | P1+P2 | yes | no | correct (compounded) | Nicotinamide Adenine Dinucleotide, 0.5 mg, injection, 10mL vial, Rx Only, Promise Pharmacy Compounding Specialists 31818 US Hwy 19N, Palm Harbor, FL 34684 |

### A-E3 (seed 51003)

| # | Record | Year | Sub-rules | v1 flags too | NDC | Mark | Full product_description |
|---|---|---|---|---|---|---|---|
| 1 | D-1072-2023#14345 | 2023 | P2 | no | yes | correct (compounded) - central admixture pharmacy (outsourcing); carries an NDC | fentaNYL 2 mcg/mL and bupivacaine 0.125% PF in 0.9% sodium chloride / Total Volume = 250 mL, Total fentaNYL 500 mcg/250 mL, bag, Rx only, Central Admixture Pharmacy Services, Inc., 7935 Dunbrook Road, Suite C, San Diego, CA 92126, NDC 71286-2082-2 |
| 2 | D-0954-2023#14389 | 2023 | P2 | no | yes | correct (compounded) | EPINEPHrine 4mg/250mL added to 0.9% sodium chloride, IV Bag, RX only, Central Admixture Pharmacy Services, Inc., 2200 South 43rd Avenue, Phoenix, AZ 85043, NDC: 72196-8093-1. |
| 3 | D-1023-2023#15151 | 2023 | P2 | no | yes | correct (compounded) | CARDIOPLEGIA SOLUTION, 7.5 mEq K, Reperfusate 4:1, low potassium, IV Bag, total volume = 238.75 mL, Rx only, Central Admixture Pharmacy Services, Inc., 2200 South 43rd Avenue, Pheonix, AZ 85043, NDC: 72196-0007-1 |
| 4 | D-1022-2023#14369 | 2023 | P2 | no | yes | correct (compounded) | CARDIOPLEGIA SOLUTION, 15 mEq K, Reperfusate 4:1, low potassium, IV Bag, total volume = 477.5mL, Rx only, Central Admixture Pharmacy Services, Inc., 2200 South 43rd Avenue, Pheonix, AZ 85043, NDC: 72196-0008-1 |
| 5 | D-0042-2026#16745 | 2025 | P5 | no | no | correct (compounded) | B12 Hydroxocobalamin for Injection, all strengths and presentations, GenoGenix, LLC, 2840 NW 2nd Ave Ste 204 Boca Raton, FL 33431-6692. |
| 6 | D-0997-2023#15180 | 2023 | P2 | no | yes | correct (compounded) | Neonatal TPN Starter Bag, Amino Acids (Trophamine) 3%/Dextrose 10%, total volume = 250mL, IV Bag, Rx only, Central Admixture Pharmacy Services, Inc., 2200 South 43rd Avenue, Pheonix, AZ 85043, NDC: 72196-0404-1 |
| 7 | D-0742-2023#14570 | 2023 | P2 | no | yes | correct (compounded) | EPINEPHrine added to 0.9% sodium chloride, 4 mg/250 mL* (16 mcg/mL), 250 mL per bag, Rx only, Central Admixture Pharmacy Services, Inc., 6580 Snowdrift Rd., Ste 100, Allentown, PA 18106, NDC 71285-8093-1. |
| 8 | D-0132-2026#15184 | 2025 | P3 | no | yes | correct (compounded) | Testosterone / Triamcinolone Acetonide Pellet (37.5MG/7.5MCG), 1 PELLET (STERILE) FOR SUBCUTANEOUS INSERTION, RX ONLY, FarmaKeio Outsourcing, 920 S Kimball Ave, Ste 100, Southlake, TX 76092. NDC 73693-0380-01 |
| 9 | D-1013-2023#15360 | 2023 | P2 | no | yes | correct (compounded) | oxyTOCIN, 40 units added to 0.9% sodium chloride 1000 mL, IV Bag, Rx Only, Rx only, Central Admixture Pharmacy Services, Inc., 2200 South 43rd Avenue, Pheonix, AZ 85043, NDC: 72196-8069-1 |
| 10 | D-0309-2023#15844 | 2023 | P2+P4 | no | no | correct (compounded) | MYCAMINE 100MG IN NS 100ML, antifungal, Rx Only, use with a homepump, Sentara Home Infusion Pharmacy Services, 535 Independence Pkwy, Ste 300, Chesapeake, VA 23320 |
| 11 | D-0223-2023#13539 | 2023 | P2 | no | no | correct (compounded) | MITOMYCIN 0.2MG/ML (1ML DROPTAINER) OPH SOLUTION; MITOMYCIN 0.2MG/ML (1ML VIAL) OPH SOLUTION, Rx Only, Pharmacy Innovations, 2936 W 17th St., Erie, PA. |
| 12 | D-0659-2022#12731 | 2022 | P2 | no | no | correct (compounded) | Hydromorphone HCl 0.1 mg/mL Infusion in 1000 mL bags, Rx only, Family Pharmacy of Statesville, Inc. |
| 13 | D-0745-2023#801 | 2023 | P2 | no | yes | correct (compounded) | NORepinephrine added to 0.9% sodium chloride, 4 mg/250 mL* (16 mcg/mL), 250 mL per bag, Rx only, Central Admixture Pharmacy Services, Inc., 6580 Snowdrift Rd., Ste 100, Allentown, PA 18106, NDC 71285-8097-1. |
| 14 | D-0830-2022#12754 | 2022 | P5 | no | yes | correct (compounded) | Fentanyl 2mcg/ml and Bupivacaine 0.125% in 0.9% Sodium Chloride 100 mL bags, Rx only, SCA Pharmaceuticals Windsor, CT 06095, NDC 70004-0231-32 |
| 15 | D-0089-2026#15781 | 2025 | P5 | no | no | correct (compounded) | Epithalon for Injection, 20mg, all presentations, GenoGenix, LLC, 2840 NW 2nd Ave Ste 204 Boca Raton, FL 33431-6692 manufactured for Extension Health. |
| 16 | D-0047-2023#13169 | 2022 | P1 | yes | no | correct (compounded) | PAPAVERINE HCL STOCK SOLUTION 30MG/ML SOLUTION, 10 mL vial, Rx only, Vital Care Compounder, 115 S. 40th Ave., Hattiesburg, MS 39402 |
| 17 | D-0185-2023#13678 | 2023 | P2 | no | no | correct (compounded) | Dutasteride 0.1% (1.5ML VIAL) Injectable, Rx Only, Pharmacy Innovations, 2936 W 17th St., Erie, PA. |
| 18 | D-0531-2022#14959 | 2022 | B3 | yes | yes | incorrect (bulk-finished) - finished dosage form in a bulk container: the B3 finished-form exclusion did not fire because the description names no dosage-form word (acetaminophen / antacid in a "Bulk Container"); carries an NDC | APAP 325 mg (Acetaminophen 325 mg) Bulk Container, ULTRAtab Laboratories, Inc., Highland, NY NDC 62959-200-00 |
| 19 | D-1280-2022#13816 | 2022 | P3 | no | yes | correct (compounded) | Anticoagulant Sodium Citrate Solution, USP 4%, 200 mg/5 mL (40 mg/mL) syringe, packaged in 5 x 5 mL Pre-Filled Syringes per carton, 6 x 5 Syringe Carton per case, Rx Only, Nephron 503B outsourcing facility, 4500 12th St. Extension, West Columbia, SC 29172, NDC: 69374-906-05 |
| 20 | D-0499-2025#778 | 2025 | P1 | yes | yes | correct (compounded) | BUPIVAcaine HCL Sterile injection, USP w/EPINEPHRINE 1:200,000, 50 mg/10mL, 0.5%, (5mg/mL), 10 mL Sterile Single-Dose Vial, Rx Only, For Nerve Block, Caudal & Epidural Anesthesia Only, Warning: Contains Sulfites, For Office Use Only, Compounded Drug by: Medivant Healthcare, 158 S. Kyrene Rd., Chandler, AZ, 85226, NDC 81483-0036-0. |
| 21 | D-0673-2023#15754 | 2023 | P2 | no | yes | correct (compounded) | Cardioplegia Solution, Modified St Thomas Formula, HIGH POTASSIUM, 122 mEq K, packaged in 1000 mL per bag, Rx only, Central Admixture Pharmacy Services, Inc., Lehigh Valley, 6580 Snowdrift Road, Allentown, PA 18106, NDC 71285-0209-1. |
| 22 | D-0693-2023#15430 | 2023 | P2 | no | yes | correct (compounded) | Neonatal TPN Starter Bag, Amino Acids (Trophamine) 4%/Dextrose 10% with CALCIUM and HEPARIN, packaged in 250 mL per bag, Rx only, Central Admixture Pharmacy Services, Inc., Lehigh Valley, 6580 Snowdrift Road, Allentown, PA 18106, NDC 71285-0422-1. |
| 23 | D-0543-2022#14805 | 2022 | B3 | yes | yes | incorrect (bulk-finished) - finished dosage form in a bulk container: the B3 finished-form exclusion did not fire because the description names no dosage-form word (acetaminophen / antacid in a "Bulk Container"); carries an NDC | Nutralox Peppermint Antacid (Calcium Carbonate 420 mg) Bulk Container, ULTRAtab Laboratories, Inc., Highland, NY NDC 62959-312-00 |
| 24 | D-0012-2024#15344 | 2023 | P2 | no | yes | correct (compounded) | fentaNYL in 0.9% sodium chloride, 1,000 mcg/100 mL, (10 mcg/mL), 100 mL bag, Rx only, CAPS, Central Admixture Pharmacy Services, Inc., 7935 Dunbrook Road, Suite C, San Diego, CA 92126, NDC 71286-2071-4 |
| 25 | D-1544-2022#12968 | 2022 | P1 | yes | yes | correct (compounded) | oxyTOCIN 30 Units/500 mL (0.06 Units/mL) added to 0.9% Sodium Chloride, Injection for IV Use, High Alert, This is a Compounded Product for Institutional or Office Use Only, Not for Resale, QuVa PHARMA 519 Route 173, Bloomsbury, NJ 08804, Total volume: 500 mL bag, NDC: 70092-1068-07. |
| 26 | D-0763-2026#65 | 2026 | P1+B2+B3 | yes | yes | correct (bulk) | SILDENAFIL CITRATE USP, 1.00KG, 1.00KG-bag Net Wt. Rx only " For Prescription Compounding Only", Shoolin Pharma Chem LLP, Block/Survey no 408, B/H Ratnamani Tubes, Near Maruti Inox, Indrad, Kadi, Mahesania, Gujarat, 382715, India, (CAS NO. 171599-83-0) NDC 85702-001-08. |
| 27 | D-0547-2023#13323 | 2023 | B3 | yes | no | correct (bulk) - excipient raw material in a 20 kg bulk container | Avicel DG, MCC/Dibasic Calcium Phosphate, Net Content/Gross Weight 20.0 KG / 21.1 KG bulk container, Manufactured by: DuPont Nutrition USA, Inc., 1301 Ogletown Road, Newark, DE 19711, USA; Manufactured in USA; Headquarters: DuPont Nutrition Biosciences ApS, Langebrogade 1, Copenhagen, Denmark. |
| 28 | D-0753-2023#15703 | 2023 | P2 | no | yes | correct (compounded) | Lidocaine 2% HCl Inj, 500mL bag, Rx only, Central Admixture Pharmacy Services, 6580 Snowdrift Road, Allentown, PA 18106, NDC 71285-8091-1, code 7128580911. |
| 29 | D-0008-2024#14521 | 2023 | P2 | no | yes | correct (compounded) | rocuronium, 50 mg/5 mL, (10 mg/mL), 5 mL Syringe, Rx only, Central Admixture Pharmacy Services, Inc., 7935 Dunbrook Road, Suite C, San Diego, CA 92126, NDC: 71286-6010-1 |
| 30 | D-0040-2024#15290 | 2023 | P1 | yes | yes | correct (compounded) | Epinephrine-Lidocaine HCl (0.25mg/mL and 7.5mg/mL) 1mL Single Use Intraocular injection Preservative Free NDC 71384-640-01 Not for resale. Office use only. Lot: 23APR018 Date Compounded: 24APR2023 Expires on: 17APR2024. In case of adverse event contact: www.fda.gov/medwatch or (800)-FDA-1088 Imprimis NJOF, LLC. 1705 Route 46 West, Unit 6B, Ledgewood, NJ, 07852 (844) 446-6979 |
| 31 | D-1034-2023#15204 | 2023 | P2 | no | yes | correct (compounded) | CARDIOPLEGIA SOLUTION, 70 mEq K, Induction 8:1, non-enriched, High Potassium, IV Bag, Total Volume = 300 mL, RX only, Central Admixture Pharmacy Services, Inc., 2200 South 43rd Avenue, Pheonix, AZ 85043, NDC: 72196-0214-1 |
| 32 | D-0958-2022#13604 | 2022 | P3 | no | yes | correct (compounded) | Hydromorphone HCl Injection, USP, 6 mg/30 mL (0.2 mg/mL), 30 mL Pre-Filled Syringe, 5 x 30 mL Pre-Filled Syringes, 6 x 5 Syringe Carton, Rx Only, Nephron 503B outsourcing facility, 4500 12th St. Extension, West Columbia, SC 29172, NDC: 69374-529-30 |
| 33 | D-0203-2023#14067 | 2023 | P2 | no | no | correct (compounded) | Edetate Calcium Disodium 400MG/ML (30ML vial) Injectable, Rx Only, Pharmacy Innovations, 2936 W 17th St., Erie, PA. |
| 34 | D-0658-2023#15401 | 2023 | P2 | no | yes | correct (compounded) | Cardioplegia Solution, Induction 4:1, High Potassium, 60 mEq K, packaged in 830 mL per bag, Rx only, Central Admixture Pharmacy Services, Inc., Lehigh Valley, 6580 Snowdrift Road, Allentown, PA 18106, NDC 71285-0100-1. |
| 35 | D-1522-2022#1104 | 2022 | P4 | no | no | correct (compounded) | TEST CYP (Grapeseed) 200 MG/ML Injectable, 10 ML vial, Rx only, Carolina Infusion LLC, 95 Bees Creek Road, Ridgeland, SC 29936. |
| 36 | D-0010-2024#15271 | 2023 | P2 | no | yes | correct (compounded) | fentaNYL in 0.9% sodium chloride, 100 mcg/10 mL, (10 mcg/mL), 10 mL Syringe, Rx only, Central Admixture Pharmacy Services, Inc., 7935 Dunbrook Road, Suite C, San Diego, CA 92126, NDC: 71286-2071-2 |
| 37 | D-0698-2023#14449 | 2023 | P2 | no | yes | correct (compounded) | Neonatal PN Starter Bag, Amino Acids (Trophamine) 3.5%/Dextrose 10% with low calcium and HEPARIN, packaged in 250 mL per bag, Rx only, Central Admixture Pharmacy Services, Inc., 6580 Snowdrift Rd., Ste 100 Allentown, PA 18106, NDC 71285-0429-1. |
| 38 | D-1044-2023#14499 | 2023 | P2 | no | yes | correct (compounded) | HYDROmorphone in 0.9% sodium chloride, 6 mg/30 mL, (0.2 mg/mL), 30 mL Syringe, Rx only, CAPS, Central Admixture Pharmacy Services, Inc., 7935 Dunbrook Road, Suite C, San Diego, CA 92126, NDC: 71286-2010-1 |
| 39 | D-1518-2022#5159 | 2022 | P4 | no | no | correct (compounded) | Sermorelin Acetate 1 MG/ML Injectable, 9 ML syringes, Carolina Infusion LLC, 95 Bees Creek Road, Ridgeland, SC 29936. |
| 40 | D-0014-2024#15083 | 2023 | P2 | no | yes | correct (compounded) | fentaNYL in 0.9% sodium chloride, 5,000 mcg/250 mL, (20 mcg/mL), 250 mL Bag, Rx only, Central Admixture Pharmacy Services, Inc., 7935 Dunbrook Road, Suite C, San Diego, CA 92126, NDC 71286-2074-1 |

## B. Miss rate of label v2

Population: records with no NDC from either source that v2 does not flag. missed = in fact a compounded or bulk item.

| Era | Unflagged no-NDC records (fresh) | Missed | Miss rate % | Wilson 95% | Kind: compounded / bulk / both |
|---|---|---|---|---|---|
| E1 | 980 | 16 / 40 | 40.0 | 26.35-55.4 | 16 / 0 / 0 |
| E2 | 1,477 | 13 / 40 | 32.5 | 20.08-47.98 | 13 / 0 / 0 |
| E3 | 677 | 3 / 40 | 7.5 | 2.58-19.86 | 3 / 0 / 0 |

### B-E1 (seed 52001)

| # | Record | Year | Mark | Full product_description |
|---|---|---|---|---|
| 1 | D-337-2013#4079 | 2013 | not | Mojo nights SUPREME Capsules, 1000 mg, Male Sexual Enhancer, supplied in 1 count blister packs, UPC 610585435915; Distributed By: Mojo Health, Pompano Beach, FL |
| 2 | D-372-2013#3071 | 2013 | missed (compounded) - compounding pharmacy product line, "all strengths and all presentations" | Hydrochloric Acid Injection, all strengths and all presentations including a) Hydrochloric Acid 0.6%, b) Hydrochloric Acid 2%, c) Hydrochloric Acid Injection 0.06% 30 mL, d) Hydrochloric Acid 2 mg/mL Injection 30 mL vial, Rx only, Green Valley Drugs, 1850 Whitney Mesa, #180, Henderson, NV 89014. |
| 3 | D-1442-2014#14836 | 2014 | not | ChloraPrep With Tint, 2% w/v chlorhexidine gluconate (CHG) and 70% v/v isopropyl alcohol (IPA), 26 mL APPLICATOR, Hi-Lite Orange. Rx Only. CareFusion, El Paso, TX 79912. NDC: 054365-400-13. |
| 4 | D-376-2014#6385 | 2013 | not | Evil Root 1200 mg, supplied in 6 capsules per bottle, Manufacturer: Tibet Shengyang Health Medicine Co.,Ltd. Address: No. 98, Min zu Road, Lhasa |
| 5 | D-355-2014#6062 | 2013 | not | I love my BFF Justice, Watermelon anti bac, Ethyl Alcohol, Net Wt. 1 fl oz, Distr by Tween Brands New Albany, OH 43054 Toronto, ON L6T 3R5 |
| 6 | D-0462-2016#4368 | 2015 | missed (compounded) | Testosterone CYP Inj 200 mg/mL, Rx, Western Drug Inc. 106 E. Main Street, Springerville, Arizona 85938 |
| 7 | D-0802-2016#7202 | 2016 | missed (compounded) - non-commercial three-drug erectile-dysfunction injection | Formula 2 (Papaverine 9 mg, Phentolamine 1 mg, Atropine 0.1 mg, PGE 10 mcg/mL) Injection, 5 mL vials, Rx only, Meditech Laboratories, Inc., 3200 Polaris Ave., Suite 27, Las Vegas, NV 89102. |
| 8 | D-0318-2015#4153 | 2014 | not | sulfur8(R) medicated anti-dandruff conditioner, dandruff treatment for Braids, spray, Active Ingredient: Salicylic Acid, 2%, 12 FL OZ (356ml) spray bottle, OTC, Made in the U.S.A. J. Strickland & Co., OLIVE BRANCH, MS 38654 UPC: 0 7561044510 7 |
| 9 | D-1417-2014#2577 | 2014 | missed (compounded) | Diphenhydramine (Alcohol Base) 25 mg / 0.5 mL Solution, 30 mL bottle, Rx only, MD Custom Rx, 19035 W. Capitol Dr., Ste. 105, Brookfield, WI 53045 |
| 10 | D-0483-2016#3351 | 2015 | missed (compounded) | Quad Mix Strong Inj, Rx, Western Drug Inc. 106 E. Main Street, Springerville, Arizona 85938 |
| 11 | D-148-2013#1937 | 2013 | not | SLIM XTREME Herbal Slimming Capsule, supplied in 30-count bottles. Another Product Forumulated and Distributed By: Globe All Wellness, LLC Hollywood, FL 33020 www.diet66.com Inquires Call 877.842.9873 |
| 12 | D-758-2014#2009 | 2014 | not | NeoCitran (acetaminophen 1000 mg, pseudoephedrine hydrochloride 60 mg, dextromethorphan hydrobromide 30 mg, chlorpheniramine maleate 4 mg) powder packets, Natural Source Cherry flavor, 10-count single dose pouches per carton, [REDACTED] Consumer Health Canada, Inc., Mississauga, ON, labeled as a) NeoCitran Ultra Strength Total Flu 7 Symptom Relief (UPC 0 58478 47365 9) and b) NeoCitran Extra Strength Sore Throat & Cough (UPC 0 58478 47365 9). |
| 13 | D-1126-2014#3520 | 2014 | not - no preparer named; papaverine 30 mg/mL is also a commercial product | Papaverine 1nj 30mg/ml |
| 14 | D-1224-2014#6130 | 2014 | not | Black Ant, 4600 mg x 4. Product is packaged in a small green box with gold lettering on the front, the back side of the box contains mostly foreign character. Within the box there are four (4) capsules individually wrapped in black and red plastic with white lettering. UPC 4026666142546 (product numbers may possibly vary for same product identification and same product packaging). |
| 15 | D-1464-2014#3304 | 2014 | missed (compounded) - pharmacy-prepared admixture with an Rx number and discard-after date | Desferal 2 gm/8 mL Sterile Water, Trinity Care Solutions, 202-C SW 17th Street, Ocala, FL 34471-5138, For Parenteral Use Only, Rx # 27767, Discard After 05/23/14 |
| 16 | D-0407-2016#4077 | 2015 | missed (compounded) | Glutathione 200 mg/mL SVN Injection, Rx, Western Drug Inc. 106 E. Main Street, Springerville, Arizona 85938 |
| 17 | D-621-2013#3058 | 2013 | not | INK-EEZE Tattoo Numbing Spray, 2 oz. (59 mL), Active Ingredients: Lidocaine HCl 5% Topical Anesthetic, Distributed by: Indelicare, LLC 914 Tourmaline Drive, Newbury Park, CA 91320, (800) 611-7720, www.inkeeze.com |
| 18 | D-0989-2015#9536 | 2015 | not | SWOLL-250 SUPER MASS BUILDER QUAD STACK (18-Methylestr-4-en-3-one-17b-ol 15mg, 6-a-Chloro-androst-4-en-17b-ol-3-one 15mg, 13-ethyl-3-methoxy-gona-2,5(10)-diene-17-one 15mg, 2,17a-dimethyl-5a-androsta-1-en-17b-ol-3-one 3 mg), Capsules, 90 count bottle, Manufactured for: Wyked Labs LLC, Winter Park, FL 32789 |
| 19 | D-1248-2014#5688 | 2014 | not | RezzRX capsules, Single Blister Pack and 20 count bottle, Distributed By: Fossil Fuel Products, LLC Atlanta, GA 30309 |
| 20 | D-408-2013#3926 | 2013 | missed (compounded) | Sodium Chloride Injection, all strengths and all presentations including a) Bacteriostatic Sodium Chloride 0.9% 30 mL, b) Sodium Chloride 23.4% 30 mL PF, and c) Sodium Chloride 23.4% 50 mL, Rx only, Green Valley Drugs, 1850 Whitney Mesa, #180, Henderson, NV 89014. |
| 21 | D-015-2014#2995 | 2013 | not | Affirm XL Nutritional Supplement, 1 and 10 count blister packs and single pill packs, Manufactured by Dongseo Biopharm Corp., Yongin City, Kyonggi do, Korea, distributed by: Affirm XL, LLC, Ladera Ranch, CA |
| 22 | D-0042-2015#3491 | 2014 | not | Ciprofloxacin 500 mg tablets, 20 count bottle, Rx only, Packaged by Aidarex Pharmacecuticals LLC, MFG: Unique Pharmaceutical Laboratories, Mumbai, India |
| 23 | D-0776-2016#4087 | 2016 | not | Oxygen, Compressed USP (Gaseous, Medical Oxygen, Aluminum Cylinders), Packaged in a) M6-Tanks, b) D-Tanks, and c) E-Tanks, Rx Only. Medical Park Homecare, 139 SE Katherine Ave., Bartlesville, OK 74006. |
| 24 | D-1101-2014#3241 | 2014 | not - "Bladder Instillation" with no other text; cannot be judged | Bladder Instillation |
| 25 | D-0414-2016#4373 | 2015 | missed (compounded) | Methylcobalamin Injection 1000 mcg/mL, 10000 mcg/mL, Rx, Western Drug Inc. 106 E. Main Street, Springerville, Arizona 85938 |
| 26 | D-1139-2016#7312 | 2016 | not | Asset extreme+PLUS Capsules, 500 mg, 30-count bottles, Distributed by Descor, LLC www.assetcapsules4u.com www.allnaturalbeelievers.com |
| 27 | D-456-2013#7793 | 2013 | missed (compounded) - syringes with a 90-day expiration, the beyond-use form of pharmacy-compounded injections | Papaverine Inj 30mg/ml Syr, 5mlsyr, 10mlsyr,10x0.95mlsyr Penile Injection, 90 day expiration, |
| 28 | D-0322-2015#3589 | 2014 | not | Eye Drops Industrial Strength (Polyethylene glycol 400 1%, Tetrahydrozoline HCl 0.05%), 0.5 FL OZ (15 mL) Bottles, Over the Counter. Labeled: a) Manufactured for: Petragon, Inc., Edwardsville, KS 66111; b) SWIFT, Distributed by Swift First Aid, Inc., Valencia, Calif. 91355, UPC: 6 69635 24082 5; c) Xpect First aid, Manufactured for Cintas First Aid & Safety, Mason, OH 45040; d) ZEE, Distributed by ZEE MEDICAL, INC., Irvine, CA 92606, UPC: 6 90689 00609 9. |
| 29 | D-1463-2014#3301 | 2014 | missed (compounded) - pharmacy-prepared admixture with an Rx number and discard-after date | Unasyn (ampicillin/sulbactam) 1.5 gm/100 mL 0.9%NS, Trinity Care Solutions, 202-C SW 17th Street, Ocala, FL 34471-5138, For Parenteral Use Only, Rx # 29082, Discard After 05/19/14 |
| 30 | D-0229-2016#9793 | 2015 | not | MIRACLE ROCK 48 capsules, packaged in 2 x 2-count blisters, 4-count capsules per carton, Manufactured Exclusively For: The One Minute Miracle Inc., UPC 0911312397354. |
| 31 | D-363-2013#4248 | 2013 | missed (compounded) | ED Mix Injections, all strengths and all presentations including a) ED mix TM -at 2, b) ED-Mix BI-Mix 10 30 mL, c) ED-Mix BI-Mix 9 30 mL; d) ED-Mix BI-Mix-3-30, e) ED-Mix PGE 80-30, f) ED-Mix SB4 30 mL, g) Ed-Mix ST 9E, h) ED-Mix ST-1, i) ED-MIX T106, j) ED-MIX-PGE-150 30 mL, k) ED-MIX-PGE-40-30, l) ED-MIX-ST 9A, m) ED-MIX-ST 9D, n) ED-MIX-ST-9B, o) ED-MIX-T 101, p) ED-MIX-T105, Rx only, Green Valley Drugs, 1850 Whitney Mesa, #180, Henderson, NV 89014. |
| 32 | D-0352-2016#6440 | 2015 | missed (compounded) | Glucosamine HCL Injectable, 200mg/mL, 30mL vial, Rx only, Downing Labs, LLC 4001 McEwen Rd, Suite 110, Dallas TX, 754244, 1-800-914-7435 |
| 33 | D-0644-2016#6482 | 2016 | missed (compounded) - home-infusion admixture | MYCAMINE (micafungin sodium) 150MG, Packaged in 150ML Homepumps, Rx Only. SENTARA HOME HEALTH SENTARA RX, 535 Independence Pkwy ste.300, Chesapeake, VA 23320-5176. |
| 34 | D-0979-2015#4521 | 2015 | not | AMPD GOLD Bee Pollen capsules, 350 mg, 60-count bottle, Signature, 1027 Highway 70 W, Suite 227, Garner, NC 27529, UPC 8 52175 00418 1. |
| 35 | D-383-2013#4069 | 2013 | missed (compounded) | Magnesium Chloride Injection, all strengths and all presentations including a) Magnesium Chloride 200 mg/50 mL and b) Magnesium Chloride 200 mg/mL 50 mL, Rx only, Green Valley Drugs, 1850 Whitney Mesa, #180, Henderson, NV 89014. |
| 36 | D-1042-2016#8763 | 2016 | not | VERMOX Tablets 500 mg, 1-count box, UPC 501109900596 |
| 37 | D-1316-2014#5315 | 2014 | not | Laroscorbine Platinium (vitamin C/collagen) injectable I.V. solution, 1 gm/0.35 gm, 5 mL ampoules, packaged in 10-count ampoules per box, Laboratories Roche Nicholas S.A., F-74240 Gaillard, - Tel.: 04 50 87 70 70, Fabricant : Produits Roche, 52, Bld du Parc, 92521 Neulilly -sur-Seine Cedex, barcode *3421357* |
| 38 | D-818-2013#5739 | 2013 | not | Oxygen, Compressed USP UN1072 Medical Gas supplied in a) 682 litres and b)165 litres cylinders, Rx only, Oklahoma Respiratory Care 800.262.9857, Norman, OK 73071 |
| 39 | D-1047-2013#5667 | 2013 | missed (compounded) - office-use syringe prepared by a pharmacy laboratory | Epinephrine 1:1,000 (1mg/mL) Sterile Solution for injection, Preservative Free/Sulfite Free, 1-mL Single-Use Syringe, Sterile Solution For Office Use Only, JCB Laboratories, Wichita, KS. |
| 40 | D-0898-2016#6650 | 2016 | not | Happy Passengers, packaged in BIG BOX (30 small boxes / 1 capsule per box / 30 capsules), Distributed by: R Thomas Marketing, LLC, Bronx, NY 10467 |

### B-E2 (seed 52002)

| # | Record | Year | Mark | Full product_description |
|---|---|---|---|---|
| 1 | D-1406-2019#11056 | 2019 | missed (compounded) - radiopharmaceutical kit from a nuclear-pharmacy compounder; judgment from the firm and product | Sn-Pyrophosphate Kit, 11.9 mg sodium pyrophosphate, Not for Direct Injection, Store at Room Temperature, Synthetopes, Inc. |
| 2 | D-0508-2020#11874 | 2019 | missed (compounded) | Budesonide 0.4mg, 3ML Vial, For Inhalation Only, Conversio Health, San Luis Obispo, CA 93401. |
| 3 | D-0719-2018#8150 | 2018 | missed (compounded) - compounding pharmacy; NOTE run 4 marked LIPO-PLEX from the same firm "not" (run 4 B E2 #17); that run 4 mark looks wrong in hindsight and is not changed | HYDROXOCOBALAMIN Injectable-30 mL MDV. Coastal Meds LLC 1759 Medical Park Dr., Ste C Bioloxi, MS 39532 |
| 4 | D-0676-2021#13044 | 2021 | not | Goose Creek Hand Sanitizer aloe Champagne Bubbles, Anti-Bacterial Spray, 3.38 FL. OZ. (100 mL), Goose Creek www.GooseCreekCandle.com, 1498 S. Wallace Wilkinson Blvd., Liberty, KY 42539, UPC 8 18489 01334 9 |
| 5 | D-0256-2021#12933 | 2021 | not | OPTIMUS LUBRICANTS Instant Hand Sanitizer, (alcohol 70% v/v) 275 Gal (1040 L) tank with spout dispenser, Made in Mexico, Liq-E, S.A. DE C.V., Puerto Tampico No. 345 Col. La Fe San Nicolas de Los Garza, Nuevo Leon, Mexico. C.P. 66477.; UPC # 7 501799 118981 |
| 6 | D-0555-2018#1551 | 2018 | not | GERMANY BLACK GOLD tablets, 2800 mg, 8-count bottle, labeling is in foreign language |
| 7 | D-0072-2022#13266 | 2021 | not | ZEE+ painaid ESF Extra-Strength Formula (Acetaminophen 250 mg, Aspirin 250 mg (NSAID), Caffeine 65 mg) tablets, 2 Tablets per/package, Packaged in a) 50-count packages/carton, b) 125-count packages/carton, PA-ESF 1414Z, Dist. by: Zee Medical Distributors, LLC Mason, OH 45040 (Shipping Label) |
| 8 | D-0684-2020#1886 | 2020 | missed (compounded) | BUP 15MG/CLON 400MCG/ FENT 6000MCG/ML INJ in 20 mL syringe Assurance Infusion (713) 533-8800 |
| 9 | D-0116-2021#12431 | 2020 | not | V-Klean Hand Sanitizer Gel Alcohol 70% packaged as a)8.5 fl oz (250 ml), UPC 7 16053 70499 3; b) 16.9 fl oz (500 ml), UPC 7 16053 70499 3; c) 33.8 fl. oz. (1000 ml) bottles: 716053704993; Manufactured by: Asiaticon S.A. de C.V. Conkar 62, Jardines del Ajusco. Tlalpan Cuidad de Mexico. 14200 ; |
| 10 | D-1589-2019#11528 | 2019 | not | Awake, 500 mg Capsules, 90-count bottles, Distributed by Herbal Doctor Remedies Alhambra, CA 91801-7081 USA, 1(800) 600-0808 |
| 11 | D-0925-2017#9520 | 2017 | not | Walgreens Daytime and Nighttime Cold & Flu, packaged in combo pack of two plastic 12FL OZ (355 mL) bottles connected by one paper sleeve, TOTAL 24 FL OZ (1.5 pt)(710 mL), OTC, Distributed by: Walgreen CO., 200 Wilmot Rd., Deerfield, IL 60015 |
| 12 | D-1094-2018#4809 | 2018 | missed (compounded) | Papav 300/Phent 5mg/10mL (Papaverine/Phentolamine) Injection,300 mg/5 mg/10 mL, 10 mL vial, Rx only, Ranier's Rx Laboratory, 1107 Lowry Avenue Suite A, Jeannette, PA 15644. |
| 13 | D-0657-2021#1306 | 2021 | not | Durisan Antimicrobial Solutions (benzalkonium chloride) Hand Sanitizing Wipes, 0.13%, 160-count canister; Sanit Technologies, LLC, 7810 25th Court East, Sarasota, Florida 34243, UPC 8 52379 00631 8. |
| 14 | D-1608-2019#11090 | 2019 | not | Lung Saver Capsules, Distributed by Herbal Doctor Remedies Alhambra, CA 91801-7081 USA, 1(800) 600-0808 |
| 15 | D-0434-2018#10243 | 2018 | not - no preparer named; cannot be judged | Midazolam HCl in 0.9% Sodium Chloride in all strengths, all doses, and all packaging. |
| 16 | D-0395-2019#10723 | 2019 | missed (compounded) - liquid HCG in a multi-dose vial is not a commercial form | HCG liquid, 1000u/ml, RX, glass vial, various |
| 17 | D-0283-2018#5169 | 2018 | not | Medline General Purpose Tray, Sterile, Single Use Only. Packaged in USA for Medline Industries, Inc., Mundelein, IL 60060 |
| 18 | D-0079-2021#12271 | 2020 | not | Modesa INSTANT HAND SANITIZER with Moisturizers and Aloe Vera (ethyl alcohol 70% v/v) 8 fl oz (237 mL) bottle, Distributed by: Midwood brands, LLC 10611 Monroe RD. Mathews, NC 28105 Made in Mexico UPC 3 2251 38042 6 |
| 19 | D-0253-2021#13178 | 2021 | not | OPTIMUS LUBRICANTS Instant Hand Sanitizer, (ethyl alcohol 70%) 8.5 Fl. Oz. (250 mL) bottle, Made in Mexico, Liq-E, S.A. DE C.V., Puerto Tampico No. 345 Col. La Fe San Nicolas de Los Garza, Nuevo Leon, Mexico. C.P. 66477. UPC # 7 501799 115621 |
| 20 | D-0714-2021#13144 | 2021 | missed (compounded) | SUFENTANIL-BUPIVACAINE-BACLOFEN PF 25MCG-12.5MG-750MCG/ML INJECTABLE 41 mL syringe, Rx only, Med Shop Total Care 470 East Loop 281 Longview, TX 75605 |
| 21 | D-1310-2019#13613 | 2019 | not | ANTIBACTERIAL Foaming Hand Wash With Moisturizers labeled as Antibacterial Foaming Soap, ACTIVE:P.C.M.X, packaged in a) 18 oz bottles, 12/18 oz bottles per case, 5063-432-02; b) 1 gallon bottles, 4/1 gallon bottles per case, 5063-420-03; c) Options Systems Antibacterial Foaming Hand Wash with .3% PCMX, packaged in 1000mL pouches, 6/1000ML pouches per case, 5063-OS1000; d) INOFOAM Antibacterial Foaming Hand Wash with .3% PCMX, packaged in 1000mL pouches, 6-1000ml pouches per case, 5063-FL1000, Inopak LTD., 24 Executive Parkway, Ringwood, NJ 07456. |
| 22 | D-0635-2021#12506 | 2021 | not | maXXzen Platinum 12000 capsule, 1-count blister card (UPC 7 18122 04072 8), Distributed by: Maxx Inc, Los Angeles, CA 90028 |
| 23 | D-1476-2020#5524 | 2020 | not | Tasty Drops, Hemp Oil Extract, Vanilla, 500MG CBD, 1 FL. OZ (30ML) bottles, Dist by: Tasty Hemp Oil, Jenison, MI, UPC 6 96305 29082 8 |
| 24 | D-0163-2021#12508 | 2020 | not | UVT World Gel Hand Sanitizer 70% Alcohol Content, 33.9 FL OZ (1LT), Distributed By UVT World Newport Beach, CA 92660 www.uvt.world Produced By: Simex Logistics S.A. de C.V. Salvatierra No. 101 Fraccionamiento El Puente Celaya, Guanajuato, Mexico Barcode: 7 00306 88677 2 |
| 25 | D-0528-2017#7484 | 2017 | missed (compounded) | MINOXADIL all strength including 2%, 5% and MINOXIDIL / RETINOIC ACID 5% / 0.025, Synergy RX, 4901 Morena Blvd # 504-A San Diego, CA 92117 (855) 792-6676 |
| 26 | D-1115-2020#12092 | 2020 | not | De-Fibroidin, 500mg Capsules, 90-count bottles, Distributed by Herbal Doctor Remedies Alhambra, CA 91801-7081 USA, 1(800) 600-0808 |
| 27 | D-0836-2021#15031 | 2021 | not | Neutrogena Ultra Sheer body mist sunscreen BROAD SPECTRUM SPF 30, Avobenzone (3%), Homosalate (8%), Octisalate (5%), Octocrylene (8%), Net Wt. 5.0 OZ (141 g) aerosol can, Distributed by: [REDACTED] CONSUMER, INC. Skillman, NY 08858 UPC 0 86800 10038 6 |
| 28 | D-1405-2019#11033 | 2019 | missed (compounded) - same firm and product type as #1 | Sn-Tetrofosmin Kit 5.0 mL, Thaw and Vent before use, Not for Direct Injection, Store Frozen, Synthetopes, Inc. |
| 29 | D-1117-2017#1621 | 2017 | not | CaverFlo Natural Herbal Coffee, 25 g, supplied in boxes of 10 packets, manufacture for Caverflo Texas Trading -- UPC: 9555671709987 |
| 30 | D-1609-2019#11366 | 2019 | not | Lung Tonic EX Capsules, Distributed by Herbal Doctor Remedies Alhambra, CA 91801-7081 USA, 1(800) 600-0808 |
| 31 | D-1147-2020#11887 | 2020 | not | Pain Away, 500mg Capsules, 90-count bottles, Distributed by Herbal Doctor Remedies Alhambra, CA 91801-7081 USA, 1(800) 600-0808 |
| 32 | D-1151-2020#12169 | 2020 | not | Pimples Off Solution 60 ML, Distributed by Herbal Doctor Remedies Alhambra, CA 91801-7081 USA, 1(800) 600- 0808 |
| 33 | D-0687-2020#4443 | 2020 | missed (compounded) | BUP 17MG/MORP 22MG/ML INJ in 20 mL syringe Assurance Infusion (713) 533-8800 |
| 34 | D-1557-2020#12281 | 2020 | not | UltraCruz Hand Sanitizing Gel Antimicrobial (70% Isopropyl Alcohol), packaged in 3 Fluid Oz./89 mL bottes, Manufactured By Santa Cruz Biotechnology, Inc. 10410 Finnell St. Dallas, TX 75220 |
| 35 | D-0563-2017#8877 | 2017 | missed (compounded) - non-commercial four-ingredient cream | MALEK'S MAGIC (retinoic acid 0.05%, hydroquinone 6%, kojic acid 3%, hydrocortisone 1%), Rx only, Synergy RX, 4901 Morena Blvd # 504-A San Diego, CA 92117 (855) 792-6676 |
| 36 | D-0925-2019#10875 | 2019 | not | NET Remedies #9 Homeopathic Preparation, Oral Liquid, 57 mL, Manufacturer: King Bio Inc. U.S.A., Supplier: NET (Australia) Pty LTD 428 Hume Street, Toowoomba QLD 4350, Australia |
| 37 | D-0817-2020#12031 | 2020 | missed (compounded) - non-commercial sustained-release T3/T4 combination | T3/T4 SR 9 mcg/38 mcg capsule |
| 38 | D-1159-2020#12138 | 2020 | not | Skin Lift, Distributed by Herbal Doctor Remedies Alhambra, CA 91801-7081 USA, 1(800) 600-0808 |
| 39 | D-0739-2020#1803 | 2020 | missed (compounded) | HYDROM 1MG/MORP 20MG/SUF 100MCG/ML INJ in 20 mL syringe Assurance Infusion (713) 533-8800 |
| 40 | D-0316-2018#5222 | 2018 | not | Medline Abdominal Surgery II Pack-LF, Sterile, Single Use Only. Packaged in USA for Medline Industries, Inc., Northfield, IL 60093 |

### B-E3 (seed 52003)

| # | Record | Year | Mark | Full product_description |
|---|---|---|---|---|
| 1 | D-0300-2025#14305 | 2025 | not | SinuCleanse Premixed SALINE PACKETS (sodium bicarbonate USP 700 mg and sodium chloride USP 2300 mg) for Nasal Wash System, 60-count All Natural USP Grade Saline Packets, Net WT 0.1OZ (3g) each, Distributed by Ascent Consumer Products Inc., Melville, NY 11747, UPC 6 46011 00103 4 |
| 2 | D-0488-2023#13174 | 2023 | not - label: not. Parser observation only: "NDC 72570 122 35", an NDC written with spaces | Delsam Pharma's Artificial Eye Ointment (Mineral Oil 15%, White Petrolatum 83%), 3.5 grams (1/8 oz.) tube, Distributed By: Delsam Pharma Lic, Bronx, Newyork 10469, NDC 72570 122 35, UPC 3 72570 12235 3. |
| 3 | D-0274-2025#754 | 2025 | not | Walgreens, Acne Control Cleanser, 10% Benzoyl Peroxide/Acne Treatment, NET WT 5 OZ (142g) Distributed by: Walgreen CO, 200 Wilmont RD, Deerfield, IL, Made in Canada. UPC#: 1 9560203602 8 |
| 4 | D-0562-2022#13024 | 2022 | not | MAC DADDY RED Capsules, packaged in 10-count blisters per carton, ASIN B07TLDZLY2, UPC 742137 605191. |
| 5 | D-0620-2026#233 | 2026 | not | BEEKEEPER'S NATURALS Saline Nasal Spray, Sinus Congestion Rinse, Made with Propolis + Xylitol, 1 FL OZ (30 mL) per bottle, Manufactured For: Beekeeper's Naturals USA Inc., Covina, CA 91789. |
| 6 | D-1157-2022#1055 | 2022 | not | Artri King Reforzado con Ortiga Omega 3 Tablets, ORIGINAL, 100-count bottles, Melchor Ocampo No. 55 Local D, Delegacion Xochimilco, C.P. 16800, Mexico, D.F., UPC 7 501031 111190. |
| 7 | D-0663-2025#647 | 2025 | not | ARTISAN OF SKIN (Benzoyl Peroxide 10%) , 7 oz (201 g), Artisan of Skin Beverly Hills, CA 90210 |
| 8 | D-0474-2025#695 | 2025 | missed (compounded) - pre-filled syringe from a compounding clinic pharmacy | Methylcobalamin Injectable, 10mg/mL, pre-filled syringe, Thrive Health Solutions, 88 Inverness, Cir E, Suite A-204, Englewood, CO 80112 |
| 9 | D-0481-2025#672 | 2025 | missed (compounded) - compounded semaglutide/cyanocobalamin pre-filled syringe | Semaglutide/Cyanocobalamin Injectable, 5mg/1mg/mL, pre-filled syringe, Thrive Health Solutions, 88 Inverness, Cir E, Suite A-204, Englewood, CO 80112 |
| 10 | D-0776-2022#5210 | 2022 | missed (compounded) - same firm appears as an outsourcing facility in run 5 A-E3 #8 | BPC-157 2 mg/mL (5 mL) Injection, 5 mL vials, Rx Only, Farmakeio 1736 N Greenville Ave Richardson, TX 75081 |
| 11 | D-0641-2022#4752 | 2022 | not | All Over-The-Counter (OTC) drug products sold by Family Dollar retail stores located in Alabama, Arkansas, Louisiana, Mississippi, Missouri and Tennessee. |
| 12 | D-0631-2026#232 | 2026 | not | Circle K, triple antibiotic ointment, Bacitracin Zinc (400 units), Neomycin Sulfate (3.5 mg), Polymyxin-B Sulfate (5000 units), net wt. 0.5 oz (14.2g) tubes, Product manufactured for Lil' Drug Store Products, Inc., 9300 Earhart Lane SW, Cedar Rapids, IA 52404, Made in India, UPC 1 94283 65181 0. |
| 13 | D-0288-2024#14655 | 2024 | not | Omeza Lidocaine Lavage pain relief oil 10*2mL VIALS |
| 14 | D-0082-2023#12744 | 2022 | not - label: not. Parser observation only: "NDC# 66233712-01", a form outside the accepted shapes | Neuroquell, A Homeopathic Drug, Calendula Oil, packaged in1/8 Fl. oz. (3.5 g) bottles, Mfg. for/Dist. By Claire Ellen Topicals, P.O. Box 901 Westborough, MA 01581, USA, NDC# 66233712-01. |
| 15 | D-1126-2022#1229 | 2022 | not | Bacillinum Pulmo, Potency: 30C, 200C, Liquid Pellets, Rx only, Washington Homeopathic Products, 260 JR Hawvermale Way, Berkeley Springs, WV 25411 |
| 16 | D-0482-2022#12635 | 2022 | not - label: not. Parser observation only: "NDC 42961-111-832", a three-digit package segment | Backache & Muscle Relief (acetaminophen 250 mg, magnesium salicylate-tetrahydrate 290mg, caffeine 50 mg) 2 tablets per packet, Mfd. for First Aid Direct, Mason, OH 45040, NDC 42961-111-832 |
| 17 | D-0890-2022#4807 | 2022 | not | Higher Education Make Out Ready Vegan Lip Balm, SPF 15, Net Wt. 0.15 oz (4.25 g) per tube, Active Ingredients: Oxtinoxate (7.5%), Oxybenzone (3%); Distributed by: Higher Education Skincare, 1.833.251.0388 |
| 18 | D-0276-2025#14969 | 2025 | not | Kids by babyganics SPF 50 mineral sunscreen totally tropical (titanium dioxide 3/5%, zinc oxide 7.25%), packaged in 3 OZ spray bottles, Dist. by KAS Direct LLC, 1525 Howe St. Racine, WI 53403, UPC 813277019923 and UPC 813277019916 |
| 19 | D-0446-2023#4868 | 2023 | not | Alcolado Relampago (menthol 1%, camphor 1.5%), packaged in a) 7 fluid oz. (207 ml) and b) 16 fluid oz. (472 ml) bottles, Distributed by: The Larkspur Group Inc. South Norwalk, CT 06854 |
| 20 | D-0284-2026#509 | 2026 | not | LUCKY ICE, Cool Mouthwash, Alcohol Free, 16.9oz, 12CT, UPC: 808829108989 |
| 21 | D-0559-2022#12723 | 2022 | not | NaturesPlus Advanced Therapeutics Glucosamine Chondroitin MSM Ultra Rx- Joint Cream, 4 oz tubes, Manufactured for NaturesPlus 548 Broadhollow Road, Melville, NY 11747, USA |
| 22 | D-1176-2023#5231 | 2023 | not - label: not. Parser observation only: "NDC 82779-002", a product-level code | Humanrace Suncare, Ozone Body Protection Cream, Broad Spectrum Sunscreen SPF 30, packaged as a 148mL (5 fl oz.) bottle, PA ++++, 100% mineral, Active Ingredient: Zinc oxide 15%, Snow Mushroom, Squalene, Aloe, Dist. By: @Humanrace 2022 Beverly Hills, CA 90210, USA, NDC 82779-002 |
| 23 | D-1427-2022#1181 | 2022 | not | DULCOLAX 5 MG TABLET 25 CT distributed to specific Family Dollar Stores 04/30/2022 through 06/10/2022. |
| 24 | D-0067-2024#13522 | 2023 | not | ION*Sinus Spray, 1 fl oz/ 30 mL, Manufactured by: ION* Biome Charlottesville, VA |
| 25 | D-0092-2025#834 | 2024 | not | Compliance Dishwashing Liquid & Antibacterial Soap, PCMX 0.1%, Net Contents: 1 Gallon, 128 Ounces, 3.785 Liters, Royal Corporation, 10232 Palm Drive, Santa Fe Springs, CA 90670 |
| 26 | D-0844-2023#13492 | 2023 | not | Sodium Chloride Ophthalmic Ointment, USP, 5%, 3.5g tubes, Manufactured by: Akorn Inc., Lake Forest, IL 60045. ALL NDCs |
| 27 | D-1296-2022#13175 | 2022 | not | Ortiga mas Ajo Rey Reforzado con Omega 3, 6 y 9, is packaged in a carton containing 30 tablets (500 mg c/u) in a bottle and 60 capsules (400 mg c/u) in a bottle, Hecho en Mexico por: Omega Nutrition , Jorge Washington No. 108 Col. Las Americas, Hidalgo del Parral, Chihuahua. C.P. 33880, ASIN B084L2XM3Z, UPC 3166557819586 |
| 28 | D-0881-2023#14008 | 2023 | not | Arnica 7 Cream, net wt 2 oz (56.7g), Manufactured for: Brazmedics, LLC, New York, NY 10021 UPC 8 60208 00181 6 |
| 29 | D-0523-2024#1007 | 2024 | not | ALOE GATOR, (Octocrylene 8%, Octyl Methoxycinnamate 6%, Benzophone 3 6%, Octyl Salicylate 5%), Original Formula, SPF 40+, Broad Spectrum Protective Gel, Sport Performance, NET WT 1 OZ (28 g), Manufactured for AGS Brands. |
| 30 | D-0801-2023#13111 | 2023 | not | DOCU LIQUID (docusate sodium, 50 mg/5 mL), packaged in 473mL bottles and b)10mL Unit Dose cups, Distributed by: Akorn Operating Company, LLC., Gurnee, IL 60031. ALL NDCs |
| 31 | D-0633-2026#218 | 2026 | not | Rapidol, Triple Antibiotic First Aid Ointment, Bacitracin Zinc 400 units, Neomycin Sulfate 3.5 mg, Polymyxin-B Sulfate 5,000 units, net wt. 2oz (57g) tubes, Distributed by/por: Pharmadel LLC, New Castle, DE 19720, Made in India, UPC 8 10096 77162 9. |
| 32 | D-0508-2022#12529 | 2022 | not | Nutralox Mint Antacid (calcium carbonate 420mg) Chewable tablets, 2-count packets, Manufactured for: HARTHealth Seattle, WA 98124 |
| 33 | D-0810-2023#13506 | 2023 | not | Hydrocortisone and Acetic Acid Otic Solution, USP, 10 mL bottles, Rx Only, Distributed by: Akorn, Inc., Gurnee, IL 60031. ALL NDCs |
| 34 | D-1461-2022#1213 | 2022 | not | QP COUGH COLD TABLET 16 CT distributed to specific Family Dollar Stores 04/30/2022 through 06/10/2022. |
| 35 | D-1389-2022#1205 | 2022 | not | LIDOCAINE ARTHRITIS AND SPORT WNTGRN 16 FLOZ distributed to specific Family Dollar Stores 04/30/2022 through 06/10/2022. |
| 36 | D-0063-2025#14995 | 2024 | not | ABSORBINE jr ULTRA STRENGTH PAIN PATCH, Menthol 6.5%, 1 patch per box, Distributed By: Absorbine Jr. LLC, Chattanooga, TN 37402 UPC 8 89476 41318 3, UPC 8 89476 41336 7 |
| 37 | D-1104-2023#12808 | 2023 | not | All Over-The-Counter (OTC) drug products warehoused, salvaged, and sold by Inmar. |
| 38 | D-0831-2023#13368 | 2023 | not | Neomycin & Polymyxin B Sulfates, and Bacitracin Zinc Ophthalmic Ointment, 3.5 g tubes, Rx Only, Manufactured by: Akorn, Inc., Lake Forest, IL 60045. ALL NDCs |
| 39 | D-0158-2024#12833 | 2023 | not | THE ROCK, Male Sexual Performance Enhancement Capsules, 1200 mg, 1 count blister card, Distributed by Steele Productions: Hallandale, FL 33008 UPC 6 61799 95052 7 |
| 40 | D-1463-2022#5196 | 2022 | not | Maxim Instant Foam Hand Sanitizer (benzalkonium chloride 0.1%) packaged in a) 1 U.S. Gallon (3.78 Liters) drums UPC 7 61841 02502 6 and b) 55 U.S. Gallon drums (208 Liters) UPC 0 07 61841 02504 0, Midlab 140 Private Brand Way, Athens, TN 37303 |

## C. Pre-registered criteria, and what would breach each on this data

- W1: pooled 98.33% (118/120), Wilson 94.13-99.54. **PASS.** Breach: pooled precision below 85% (fewer than 102 of 120 correct), or a lower bound at or below 70%. Can fail.
- W2: era precisions E1 100.0%, E2 100.0%, E3 95.0%; intervals E1 91.24-100.0; E2 91.24-100.0; E3 83.5-98.62. **PASS.** Breach: two eras more than 20 pp apart with disjoint intervals; with n = 40 that needs roughly 39/40 against 30/40 or wider (for example 97.5% [87.1-99.6] against 70% [54.6-81.9]). Can fail.
- W3: era miss rates E1 40.0%, E2 32.5%, E3 7.5%; intervals E1 26.35-55.4; E2 20.08-47.98; E3 2.58-19.86. **FAIL.** Breach: two eras more than 20 pp apart with disjoint intervals, for example 2/40 against 14/40 (5% [1.4-16.5] against 35% [22.1-50.5]); run 4's 27/40 against 7/40 would have breached. Can fail, in either direction.
- W4: miss rates E1 40.0%, E2 32.5%, E3 7.5%. **FAIL.** Breach: any era above 25%, i.e. 11 or more of 40 missed. Can fail.
- **Verdict: LABEL v2 NOT FIT FOR USE.**

A note on W2 and W3: requiring BOTH a gap over 20 pp AND disjoint intervals makes them harder to breach than a gap alone at n = 40. They can still fail on plausible outcomes, as the examples show, so they are reported as tests, not as formalities.

## E. v1 against v2

All records in each era (not just samples).

| Era | Records | v1 flags | v2 flags | Both | v1 only | v2 only | v1-only records carrying an NDC | v2-only by sub-rule (P2 P3 P4 P5 B1 B2 B3) |
|---|---|---|---|---|---|---|---|---|
| E1 | 6,213 | 2,465 | 3,154 | 2,451 | 14 | 703 | 2 | 587 0 0 119 0 0 0 |
| E2 | 6,702 | 1,094 | 1,923 | 1,067 | 27 | 856 | 21 | 281 8 75 480 8 12 0 |
| E3 | 4,626 | 299 | 912 | 260 | 39 | 652 | 33 | 446 93 73 93 0 0 0 |

## F. What run 5 shows (no decomposition; Part D is conditional on a pass)

- **v2 fixed the precision defect.** Pooled precision rose to 98.33% and every era is at or above 95.0%. The two remaining errors are the run 4 defect in a form the B3 exclusion list did not anticipate: a finished product in a "Bulk Container" whose description names no dosage-form word.
- **v2 did not fix the recall defect.** Miss rates are 40.0, 32.5 and 7.5% (E1, E2, E3), against run 4's 67.5, 45.0 and 17.5% for v1 on a different sample. The misses still run high early and low late, the same direction as run 4, so a decomposition using v2 would still understate the early compounded share.
- **What the remaining misses have in common.** Every missed record names a preparer, but not in words a rule can separate from a manufacturer: a "Drug" store, a "Laboratories" or "Labs", a "Health Solutions", an "Rx" business name, an infusion firm named without a service word, or no firm at all with a non-commercial product form (a beyond-use date, an Rx number, a combination with no commercial equivalent). A reader recognizes them from the product plus the firm; the vocabulary does not. That is a finding about the source text, recorded here, not a proposal for a third label.
- **v1 against v2 (section E).** v2 flags more in every era and almost everything v1 flags; the additions come mainly from P2 (a named pharmacy) and P5 (named preparers), and in E3 also P3 and P4. Most v1-only records in E2 and E3 carry an NDC, consistent with the finished-bulk exclusion working as intended.
- **Consistency note on run 4.** Run 5 B-E2 #3 marks a hydroxocobalamin vial from a compounding pharmacy as missed; run 4 B-E2 #17 marked a product from the same firm "not". The run 4 mark looks wrong in hindsight. It is recorded, not changed: run 4 is closed.
- **Parser observation, for the limitations section only.** Four of the 40 E3 Part B records carry an NDC in a form the run 2 parser does not accept (spaced digits, a three-digit package segment, an unhyphenated labeler-product run, a product-level code). Run 3 measured 1 in 40 in the comparable E3 population. Run 3 is not reopened; this goes beside the dotted and product-level forms already listed.
- **Per the brief:** v2 fails and the run stops. No third label was built. The fallback applies: the paper ships its first three findings, with attribution reported as attempted and unresolved.

