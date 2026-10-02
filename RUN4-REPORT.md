> **NOTICE added 2026-10-02, after this report was written.**
>
> The decomposition reported below does not stand. It was computed on a label that failed its own
> pre-registered validation in run 5. It is not used in the manuscript, supports no conclusion,
> and must not be quoted. This report is published unaltered otherwise, as the record of what
> run 4 actually produced.

# A15 Run 4 - validating the NO-NDC-EXPECTED label: EXPLANATION DOES NOT STAND

- **V1 pooled precision 91.67% (needs >= 85), lower Wilson bound 85.34% (needs > 70): PASS**
- **V2 largest gap between era precisions 22.5 pp (needs <= 15): FAIL**
- **V3 E3 miss rate minus E1 miss rate -50.00 pp (needs <= +15): PASS**
- **VERDICT: EXPLANATION DOES NOT STAND.** Criteria pre-registered in the run 4 brief; not adjusted.
- **Decomposition, 2013 to 2026:** coverage 29.85% -> 82.92%, change +53.07 pp = composition +21.05 pp (39.7%) + within-group +37.88 pp (71.4%) + interaction -5.86 pp (-11.0%).
- **Decomposition, E1 to E3 (robustness):** 38.53% -> 75.59%, change +37.06 pp = composition +15.73 pp (42.5%) + within-group +24.40 pp (65.8%) + interaction -3.07 pp (-8.3%).
- Precision by era: E1 100.0% (40/40, CI 91.24-100.0); E2 97.5% (39/40, CI 87.12-99.56); E3 77.5% (31/40, CI 62.5-87.68). Miss rate by era: E1 67.5% (27/40, CI 52.02-79.92); E2 45.0% (18/40, CI 30.71-60.17); E3 17.5% (7/40, CI 8.75-31.95).
- Rules imported unchanged (run 2 parser `892aacebdeb522ad...`, run 3 label rules `2664f53f33943376...`, digests checked at run time). Data SHA-256 `c6eb46526a3ad52102a88b65727874c2e23c43300b27e704eada05960d755092`, 17,975 records, confirmed first.
- No model, nothing fitted, no paper writing. `run4_label_validation.py` -> `run4_results.json`; marks in `run4_marks.json`.

---

## 0. Design

Year = year of `report_date`, as in runs 1-3. Eras E1 2013-2016, E2 2017-2021, E3 2022-2026. NO-NDC-EXPECTED = the run 3 compounding rule (stem "compound": compounded, compounding, compounder, compounds) OR the run 3 bulk rule (the word "bulk"; "active pharmaceutical ingredient" or the uppercase token API; "drug substance", "raw material" or "intermediate"; a kilogram quantity or the word drum), both imported from `run3_parser_validation.py` unchanged. "NDC from either source" = an openfda product_ndc, or at least one code accepted by the run 2 parser. Samples: `random.Random(seed).sample(sorted(record indexes), 40)`; seeds A E1 41001, E2 41002, E3 41003; seeds B E1 42001, E2 42002, E3 42003. All 240 were drawn before any was read. Full descriptions are quoted, whitespace collapsed, with employer-boundary terms replaced by `[REDACTED]` (0 replacements). Wilson 95% intervals throughout.

## A. Precision of the label

Population: every record the composite label flags, whether or not it carries an NDC. Correct = the recalled item really is a compounded preparation, a bulk substance, an API, a raw material or an intermediate. Kind = compounded, bulk or both.

| Era | Flagged records (compounding rule / bulk rule) | Correct | Precision % | Wilson 95% | Correct by kind: compounded / bulk / both | Compounding-rule hits correct | Bulk-rule hits correct |
|---|---|---|---|---|---|---|---|
| E1 | 2,465 (1,947 / 526) | 40 / 40 | 100.0 | 91.24-100.0 | 36 / 4 / 0 | 36 / 36 | 4 / 4 |
| E2 | 1,094 (1,011 / 93) | 39 / 40 | 97.5 | 87.12-99.56 | 37 / 2 / 0 | 39 / 39 | 0 / 1 |
| E3 | 299 (215 / 95) | 31 / 40 | 77.5 | 62.5-87.68 | 23 / 8 / 0 | 28 / 28 | 6 / 15 |
| pooled | | 110 / 120 | 91.67 | 85.34-95.41 | | | |

### A-E1 sample (seed 41001)

| # | Record | Year | Rule hit | NDC | Mark | Full product_description |
|---|---|---|---|---|---|---|
| 1 | D-436-2014#2901 | 2014 | compounding | no | correct (compounded) | Papav/Phentol/PG E1, 30 mg/1 mg/20 mcg/mL, injectable, Rx only, Specialty Medicine Compounding Pharmacy, 350 S Lafayette, South Lyon, MI 48178 |
| 2 | D-281-2014#5758 | 2013 | compounding | no | correct (compounded) | Test Cypionate 20mg/ml 5ml, Main Street Compounding Pharmacy, 126 East Main Street, Newbern, TN 38059, 888-658-6200 |
| 3 | D-0996-2016#7125 | 2016 | compounding | no | correct (compounded) | M.l.C. Methyl B12, 25 MG/50MG/25MG/1 MG/ML, packaged in 5mL vials, Rx only, Well Care Compounding Pharmacy Las Vegas, NV 89121 |
| 4 | D-0178-2015#8393 | 2014 | compounding | no | correct (compounded) | BEVACIZUMAB/DEXAMETHASONE, 1.25/0.5 mL, Injectable, 0.05 mL plastic syringe, RX, Creative Compounds, Wilsonville, OR 97070. |
| 5 | D-1638-2015#2764 | 2015 | compounding | no | correct (compounded) | Sufentanil 50 mcg/ml + Bupivacaine 0.25 mg/ml Solution, Sterile-Preservative Free, The Compounding Pharmacy of America, Knoxville, TN |
| 6 | D-0203-2016#6304 | 2015 | compounding | no | correct (compounded) | BIEST TD 80/20 (Estradiol (E2) Trit (Yellow)/Estriol USP Micronized (E3) : PROG (Progesterone USP Micronized) : DHEA (Dehydroepiandrosterone Micronized) IN VERSABASE W/V (weight/volume) 4 : 67.5 :10MG/ML Transdermal cream, dispensed in 10 mL prefilled, amber syringes, Rx only, The Compounder, 340 Marshall Avenue Unit 100, Aurora, IL 60506. |
| 7 | D-545-2015#8996 | 2015 | bulk | no | correct (bulk) | Bismuth Subcarbonate active pharmaceutical ingredient packaged in varying grams or kg in bags or drums, Attix Pharmaceuticals, 184 Front Street East, Unit 801, Toronto, Ontario M5A 4N3, Canada |
| 8 | D-678-2013#5927 | 2013 | compounding | no | correct (compounded) | Test cyp 75 mg-estradiol cyp 5 mg/ml, Clinical Specialties Compounding Pharmacy, 318 Baston Road, Augusta, GA 30907 |
| 9 | D-301-2014#6036 | 2013 | compounding | no | correct (compounded) | Testosterone Pellets 200mg, Main Street Compounding Pharmacy, 126 East Main Street, Newbern, TN 38059, 888-658-6200 |
| 10 | D-252-2014#8724 | 2013 | compounding | no | correct (compounded) | Oral B-12 30ml--cotton candy, Main Street Compounding Pharmacy, 126 East Main Street, Newbern, TN 38059, 888-658-6200 |
| 11 | D-721-2013#2294 | 2013 | compounding | no | correct (compounded) | Dextrose 50% Solution, compounded by Olympia Pharmacy, Orlando, FL |
| 12 | D-215-2014#6166 | 2013 | compounding | no | correct (compounded) | Methylprednisolone 40mg PF 10ml, Main Street Compounding Pharmacy, 126 East Main Street, Newbern, TN 38059, 888-658-6200 |
| 13 | D-243-2014#5861 | 2013 | compounding | no | correct (compounded) | Minoxidil 10% 60ml, Main Street Compounding Pharmacy, 126 East Main Street, Newbern, TN 38059, 888-658-6200 |
| 14 | D-0294-2016#9765 | 2015 | compounding | yes | correct (compounded) | Zinc Sulfate (1 mg/mL), 10 mL Single Dose Vial, For IV Use After Dilution, Rx only, Compounded by US Compounding Pharmacy, Conway, Arkansas, 72032, NDC 62295-3226-07 |
| 15 | D-993-2013#5702 | 2013 | compounding | no | correct (compounded) | PUMICE/LIDOCAINE HCL 1.5%/1% INJ SUSP, all presentations, FOR INTRAVENO AND SQ USE ONLY, STERILE, RX ONLY, Compounded by Beacon Hill Medical Pharmacy PC, dba Rxtra Solutions, Southfield, MI |
| 16 | D-734-2015#9570 | 2015 | bulk | no | correct (bulk) | Irbesartan active pharmaceutical ingredient packaged in varying grams or kg in bags or drums, Attix Pharmaceuticals, 184 Front Street East, Unit 801, Toronto, Ontario M5A 4N3, Canada |
| 17 | D-1553-2015#3163 | 2015 | compounding | no | correct (compounded) | Hydromorphone 60 mg/ml + Bupivacaine 30 mg/ml Solution, Sterile-Preservative Free, The Compounding Pharmacy of America, Knoxville, TN |
| 18 | D-841-2015#8021 | 2015 | bulk | no | correct (bulk) | Phentolamine Mesylate active pharmaceutical ingredient packaged in varying grams or kg in bags or drums, Attix Pharmaceuticals, 184 Front Street East, Unit 801, Toronto, Ontario M5A 4N3, Canada |
| 19 | D-1273-2016#4041 | 2016 | compounding | yes | correct (compounded) | Promethazine 6.25 mg added to 0.9% Sodium Chloride 50 mL in 100 mL B/Braun PAB bag, Rx Only, Compounded by PHARMAKON Pharmaceuticals, Noblesville, IN 46060, NDC 45183-0177-41 |
| 20 | D-140-2014#5942 | 2013 | compounding | no | correct (compounded) | HCG 380 iu prefilled syringes, Main Street Compounding Pharmacy, 126 East Main Street, Newbern, TN 38059, 888-658-6200 |
| 21 | D-1277-2016#3604 | 2016 | compounding | yes | correct (compounded) | Phenylephrine HCI 40mg/250 mL in 0.9% Sodium Chloride 250 mL bag, Rx Only, Compounded by PHARMAKON Pharmaceuticals, Noblesville, IN 46060, NDC 45183-0189-02 |
| 22 | D-559-2013#13865 | 2013 | compounding | no | correct (compounded) | Lipoic Acid 25 mg/mL Injectable, 100 mL vials, compounded by The Compounding Shop, St. Petersburg, FL |
| 23 | D-313-2014#8524 | 2013 | compounding | no | correct (compounded) | Triamcinolone PF 40mg 2ml, Main Street Compounding Pharmacy, 126 East Main Street, Newbern, TN 38059, 888-658-6200 |
| 24 | D-943-2013#5694 | 2013 | compounding | no | correct (compounded) | CALCIUM CHLORIDE 100 MG/ML INJECTABLE, all presentations, FOR INTRAVENO AND SQ USE ONLY, STERILE, RX ONLY, Compounded by Beacon Hill Medical Pharmacy PC, dba Rxtra Solutions, Southfield, MI |
| 25 | D-1432-2016#7641 | 2016 | compounding | yes | correct (compounded) | 6.66 mcg/mL Fentanyl Citrate and 0.125% Bupivacaine HCl (Preservative Free) in 0.9% Sodium Chloride; 15 mL in 20 mL BD Syringe, Service Code 2T6993Rx Only, Compounded by PharMEDium Services, LLC, Memphis, TN 36141, NDC 61553-993-86 |
| 26 | D-0198-2016#8305 | 2015 | compounding | no | correct (compounded) | BIEST TD 80/20 (Estradiol (E2) Trit (Yellow)/Estriol USP Micronized (E3) : PROG (Progesterone USP Micronized) : DHEA (Dehydroepiandrosterone Micronized) : TESTO (Testosterone Trit) W/V (weight/volume) VERSABASE 5.0 : 30 : 2.5 : 0.25 MG/ML Transdermal cream, dispensed in 10 mL prefilled, amber syringes, Rx only, The Compounder, 340 Marshall Avenue Unit 100, Aurora, IL 60506. |
| 27 | D-0224-2015#8407 | 2014 | compounding | no | correct (compounded) | TESTOSTERONE CYPIONATE (SESAME OIL/CMPD), 200mg/mL, injectable, 5 mL glass vial, RX, Creative Compounds, Wilsonville, OR 97070 |
| 28 | D-258-2014#5961 | 2013 | compounding | no | correct (compounded) | Post-menopausal HCG Pk 3rd mont, Main Street Compounding Pharmacy, 126 East Main Street, Newbern, TN 38059, 888-658-6200 |
| 29 | D-0208-2015#6577 | 2014 | compounding | no | correct (compounded) - commercial contrast agent repackaged into vials by a compounding pharmacy; marked compounded | OMNIPAQUE, 300mgI/mL, injectable, 2 mL glass vial, RX, Creative Compounds, Wilsonville, OR 97070 |
| 30 | D-1198-2015#4377 | 2015 | compounding | no | correct (compounded) | Potassium Chloride, Dextrose 5% LR 1000 mL with 40mEq KCL, Qty: 1 1000 mL Bag, Rx Only. Compounded by: United Medical IV Center (Little Rock) 1527 South Bowman Rd. Ste. D Little Rock, AR 72211-4200. |
| 31 | D-1292-2015#9327 | 2015 | compounding | yes | correct (compounded) | S-methylcobalamin 25 mg/mL (PF) Injection, Rx Only, 10 mL Vial, Apothecary Shoppe, Compounding Pharmacy, Tulsa OK 74135, NDC 13861-1701-19 |
| 32 | D-1604-2015#2310 | 2015 | compounding | no | correct (compounded) | Morphine 42 mg/ml + Bupivacaine 8 mg/ml Solution, Sterile-Preservative Free, The Compounding Pharmacy of America, Knoxville, TN |
| 33 | D-1397-2016#8689 | 2016 | compounding | yes | correct (compounded) | 2 mcg/mL Fentanyl Citrate and 0.15% Bupivacaine HCl (Preservative Free) in 0.9% Sodium Chloride, 200 mL in 250 mL Baxter Intravia Bag, Service Code 2K8433, NDC 61553-433-58, Rx Only, Compounded by PharMEDium Services, LLC, Memphis, TN 36141 |
| 34 | D-1538-2016#9562 | 2016 | compounding | no | correct (compounded) | Moxifloxacin HCl 1 mg/ml (0.1mg/0.1ml) and BSS solution, 2ml Single use vial, Rx, Vital Care Compounder, Hattiesburg, MS 39402 |
| 35 | D-1018-2016#9966 | 2016 | compounding | no | correct (compounded) | TRI-MIX # 3, packaged in 5mL vials, Rx only, Well Care Compounding Pharmacy Las Vegas, NV 89121 |
| 36 | D-1608-2015#4484 | 2015 | compounding | no | correct (compounded) | Morphine 50 mg/ml + Bupivacaine 2.5 mg/ml Solution, Sterile-Preservative Free, The Compounding Pharmacy of America, Knoxville, TN |
| 37 | D-1197-2015#4353 | 2015 | compounding | no | correct (compounded) | Vancomycin 1000mg / NS 100mL, Packaged in 100 mL Bags, Rx Only. Compounded by: United Medical IV Center (Little Rock) 1527 South Bowman Rd. Ste. D Little Rock, AR 72211-4200. |
| 38 | D-866-2015#6713 | 2015 | bulk | no | correct (bulk) | Procarbazine HCl active pharmaceutical ingredient packaged in varying grams or kg in bags or drums, Attix Pharmaceuticals, 184 Front Street East, Unit 801, Toronto, Ontario M5A 4N3, Canada |
| 39 | D-0242-2016#8443 | 2015 | compounding | yes | correct (compounded) | Bi-Mix (Papaverine 30 mg/mL, Phentolamine 1 mg/mL), 5 mL Multi-Dose Vial, Rx only, Compounded by US Compounding Pharmacy, Conway, Arkansas, 72032, NDC 62295-3254-05 |
| 40 | D-760-2013#4533 | 2013 | compounding | no | correct (compounded) | MICC (Methionine, Inositol, Choline, Cyanocobalamin, Chromium) Inj and MICC 25/50/330 Inj, compounded by Olympia Pharmacy, Orlando, FL |

### A-E2 sample (seed 41002)

| # | Record | Year | Rule hit | NDC | Mark | Full product_description |
|---|---|---|---|---|---|---|
| 1 | D-0168-2022#12734 | 2021 | compounding | no | correct (compounded) | TESTOSTERONE BI-BLEND 100/100MG/ML INJECTABLE, Rx only, Talon Compounding Pharmacy, 2950 Thousand Oaks Drive Ste 25, San Antonio, Texas 78247 |
| 2 | D-0250-2020#11353 | 2019 | compounding | no | correct (compounded) | S-SODIUM SELINITE 0.219% INJ, 19ml glass vials, Rx only, Red Mountain Compounding Rx |
| 3 | D-0320-2018#9715 | 2018 | compounding | no | correct (compounded) | All sterile drug preparations remaining within expiry prepared from Fentanyl Citrate Base Solution dispensed between October 16, 2017 and November 17, 2017 Compounded by Intrathecal Compounding Specialists, Scott, LA 70583. |
| 4 | D-0341-2017#7003 | 2017 | compounding | no | correct (compounded) | Arginine/Citrulline/Ornit+Lido 100/100/100/10 mg/mL Injectable, 10 mL vials, Compounded by Wells Pharmacy Network, LLC, Ocala, FL |
| 5 | D-0301-2017#7361 | 2017 | compounding | no | correct (compounded) | Testosterone Cypionate/Zinc Gluconate in Sesame Oil, 200 mg/2 mg/mL, (5 ML and 10 ML). Compounded by Tri-Coast Pharmacy |
| 6 | D-0053-2022#13265 | 2021 | compounding | no | correct (compounded) | ACETYLCYSTEINE 10% OPTH SOLN, Red Mountain Compounding Rx |
| 7 | D-0930-2017#9285 | 2017 | compounding | yes | correct (compounded) | Ropivacaine HCl 0.2% 400 mL Total Volume in an ON-Q Pump in 0.9% Sodium Chloride Injection in 400 mL, Rx Only, Compounded by PharMEDium Services, LLC, Sugar Land, TX 77478, NDC: 61553-256-09 |
| 8 | D-1165-2018#10073 | 2018 | compounding | no | correct (compounded) | Testosterone Enanthate/Cypionate injectable, 126/54 mg/mL, packaged in a) 3 mL and b) 5 mL Multiple Dose vials, Rx only, Central Drugs Compounding Pharmacy, 520 W. La Habra Blvd, La Habra, CA 90631 |
| 9 | D-0744-2017#1588 | 2017 | compounding | no | correct (compounded) | TRI MIX 20/30/1 5ML MDV MCG/MG/MG/ML INJ, Injection, 20mcg/30mg/1mg/mL, Rx only, 5 mL Glass/Multiple Dose vial, Prepared by Key Compounding Pharmacy |
| 10 | D-0501-2018#9912 | 2018 | compounding | yes | correct (bulk) - API sold for prescription compounding | Leucovorin Calcium USP for prescription compounding, packaged a) 100mg, (NDC 58597-8084-1); b) 1g (NDC 58597-8084-3); c) 5g (NDC 58597-8084-4); d) 25 g (NDC 58597-8084-5), RX only, packed by American Pharmaceutical Ingredients, LLC 6650 Highland Road, Waterford, MI 48327 |
| 11 | D-0212-2022#12630 | 2021 | compounding | no | correct (compounded) | TRI-MIX PAPAVERINE 30/PHENTOLAMINE 2/PGE-1 30 INJ INJECTABLE, Rx only, Talon Compounding Pharmacy, 2950 Thousand Oaks Drive Ste 25, San Antonio, Texas 78247 |
| 12 | D-0273-2020#11774 | 2019 | compounding | no | correct (compounded) | S-METHYLCOBALAMIN 5,000MCG/ML MDV Injection, 30 ML glass vial, Rx Only, Red Mountain Compounding RX |
| 13 | D-1106-2019#11176 | 2019 | compounding | no | correct (compounded) | PAPAVERINE-PHENTOLAMINE-PGE1 9-1 MG-10 MCG/ML* INJECTABLE, 18 ml, Professional Compounding Pharmacy, 996 NW Circle Blvd. #105 Corvallis, OR 97330 . |
| 14 | D-1094-2019#11174 | 2019 | compounding | no | correct (compounded) | PAPAVERINE-PHENTOLAMINE-PGE1 12-1MG-10MCG/ML INJECTABLE, (a) 10ml, (b) 9ml, Professional Compounding Pharmacy, 996 NW Circle Blvd. #105 Corvallis, OR 97330 |
| 15 | D-0767-2017#2509 | 2017 | compounding | no | correct (compounded) | GSH/NAC INH PV 150/50MG/ML SOLN, Inhalation Solution, 150mg/50mg/mL, Rx only, 4mL Plastic/Multiple Dose vial, Prepared by Key Compounding Pharmacy |
| 16 | D-1676-2019#10921 | 2019 | compounding | yes | correct (compounded) | MANGANESE SULFATE MONOHYDRATE (PFV) 0.1MG/ML INJ, 10 ML per syringe, RXQ Compounding, 340 West State Street, Unit 9, Athens, OH 45701. NDC: 70731-0952-10 |
| 17 | D-0260-2020#11367 | 2019 | compounding | no | correct (compounded) | S-DMSO 6.25% OPTH SOLN, 10 ml dropper bottle, Rx Only, Red Mountain Compounding Rx |
| 18 | D-0771-2017#2084 | 2017 | compounding | no | correct (compounded) | PROCAINE HCL 50ML MDV (CALIF) 1% INJ, Injection, 1%, Rx only, 50mL Glass/Multiple Dose vial, Prepared by Key Compounding Pharmacy |
| 19 | D-0119-2022#12716 | 2021 | compounding | no | correct (compounded) | IC B COMPLEX INJ INJECTABLE, Rx only, Talon Compounding Pharmacy, 2950 Thousand Oaks Drive Ste 25, San Antonio, Texas 78247 |
| 20 | D-1107-2019#10690 | 2019 | compounding | no | correct (compounded) | PAPAVERINE-PHENTOLAMINE-PGE1 30-1 MG-20 MCG/ML* INJECTABLE, 5 ml, Professional Compounding Pharmacy, 996 NW Circle Blvd. #105 Corvallis, OR 97330 . |
| 21 | D-0249-2017#8924 | 2017 | compounding | no | correct (compounded) | BCAA (30 ML) (Isoleucine (L) 15 mg + Leucine (L) 10 mg+ Valine 40 mg+ Lidocaine HCL 10 mg/mL). Compounded by Tri-Coast Pharmacy. |
| 22 | D-0107-2022#13226 | 2021 | compounding | no | correct (compounded) | BI-MIX PAPAVERINE 40/PHENTOLAMINE 2 INJ INJECTABLE, Rx only, Talon Compounding Pharmacy, 2950 Thousand Oaks Drive Ste 25, San Antonio, Texas 78247 |
| 23 | D-0304-2017#7524 | 2017 | compounding | no | correct (compounded) | Testosterone Cypionate/Enanthate/Propionate, 160 mg/20 mg/20 mg/mL, (5 ML). Compounded by Tri-Coast Pharmacy |
| 24 | D-0264-2017#7567 | 2017 | compounding | no | correct (compounded) | Infuvite IV (Ascorbic Acid 200 mg+ Vitamin A Acetate 330 IU+Vitamin D3 200 IU+Thiamine HCL 6 mg+Riboflavin-5-Phosphate Sod 3.6 mg+Pyridoxine HCL 6 mg+Niacinamide 40 mg+Dexpanthenol 15 mg+Vitamin 40E Succinate 10 IU+Phytonadione (K1) 150 mcg/5 mL). 30 ML. Compounded by Tri-Coast Pharmacy. |
| 25 | D-0892-2018#2234 | 2018 | compounding | yes | correct (compounded) | ESTRADIOL 20mg PELLET, 1-count 3ml amber vial. RX only. Compounded by: Qualgen 14844 Bristol Park Blvd, Edmond OK 73013. NDC 69761-020-01 |
| 26 | D-0136-2018#9974 | 2018 | compounding | yes | correct (compounded) | Fentanyl 10 mcg in 0.9% Sodium Chloride 1 mL, 1 mL Vial, Concentration: 10 mcg/mL, This is a compounded injectable drug; Rx only; Hospital/office use only. SSM St. Clare Outsourcing Facility, Fenton, MO. --- NDC: 88890-9010-81 |
| 27 | D-0708-2017#1605 | 2017 | compounding | no | correct (compounded) | 5-MTHF 10ML MDV (CALIF) 5MG/ML INJ, Injection, 5mg/mL, Rx only, 10mLGlass/Multiple Dose vial, Prepared by Key Compounding Pharmacy |
| 28 | D-0712-2017#2989 | 2017 | compounding | no | correct (compounded) | ATROPINE SULFATE 0.5% OPHTH, Ophthalmic 0.50%, Rx only, 15mlLGlass /Multiple Dose vial, Prepared by Key Compounding Pharmacy |
| 29 | D-0444-2019#10936 | 2019 | compounding | no | correct (compounded) | Amino Blend Injection, Ornithine/Arginine/Lysine/Lidocaine 75 mg/75 mg/75 mg/10 mg/mL 10 mL, Rx Only, Promise Pharmacy Compounding Specialists 31818 US Hwy 19N, Palm Harbor, FL 34684 |
| 30 | D-0054-2022#12969 | 2021 | compounding | no | correct (compounded) | ACETYLCYSTEINE 2% OPTH SOLN, Rx only, Red Mountain Compounding Rx |
| 31 | D-1640-2019#11490 | 2019 | compounding | yes | correct (compounded) | BUFFERED LIDOCAINE HCL 1% INJECTION SOL (PF) SYR, 0.5 ML per vial, RXQ Compounding, 340 West State Street, Unit 9, Athens, OH 45701. NDC: 70731-0139-84 |
| 32 | D-0233-2020#11824 | 2019 | compounding | no | correct (compounded) | S-LIDOCAINE HCL 2% INHALATION SOLN SYRINGES, 2ML syringe, Red Mountain Compounding Rx |
| 33 | D-0151-2022#12586 | 2021 | compounding | no | correct (compounded) | TEST CYPIONATE 200MG/ANASTROZOLE 0.5MG/DUTASTERIDE 0.5MG/ML IN OIL INJECTABLE, Rx only, Talon Compounding Pharmacy, 2950 Thousand Oaks Drive Ste 25, San Antonio, Texas 78247 |
| 34 | D-1178-2019#4762 | 2019 | compounding | no | correct (compounded) | Serum Tears 30% Drops, 1 mL Droptainer, Anderson Compounding Pharmacy 310 Bluff City Hwy, Bristol, TN. |
| 35 | D-1101-2019#10771 | 2019 | compounding | no | correct (compounded) | PAPAVERINE-PHENTOLAMINE-PGE1 30-2 MG-30 MCG/ML* INJECTABLE, 5ml, Professional Compounding Pharmacy, 996 NW Circle Blvd. #105 Corvallis, OR 97330 . |
| 36 | D-1158-2019#4738 | 2019 | compounding | no | correct (compounded) | Heparin 10,000 U/Bupivacaine 0.5% 10 mL, Sodium Bicarbonate 8.4% 50 mL, 61 mL Syringe, Anderson Compounding Pharmacy 310 Bluff City Hwy, Bristol, TN. |
| 37 | D-1251-2019#11125 | 2019 | compounding | yes | correct (compounded) | HYDROmorphone 20 mg/100 mL Injectable Solution, Hydromorphone HCl 20 mg 0.9% Sodium Chloride 100 mL, Sterile single use bag, Compounded Drug, Avella of Houston 9265 Kirby Dr., Houston, TX 77054 (877) 794-0404, NDC: 42852-221-10 |
| 38 | D-1012-2018#4686 | 2018 | bulk | no | incorrect - retail botanical (kratom) powder; the kg match is a package size, not a bulk substance | Gaia Kratom (mitragyna speciosa) powder, White Horn, 1oz, 250g, 1kg packages, Gaia Ethnobotanical.com |
| 39 | D-0496-2018#7304 | 2018 | compounding | yes | correct (bulk) - API sold for prescription compounding | Imiquimod USP for prescription compounding, packaged in a) 1g (NDC 58597-8317-1); b) 10g (NDC 58597-8317-3); c) 25g (NDC 58597-8317-4) RX only, packed by American Pharmaceutical Ingredients, LLC 6650 Highland Road, Waterford, MI 48327 |
| 40 | D-1086-2019#11221 | 2019 | compounding | no | correct (compounded) | SODIUM CHLORIDE PRES-FREE 5% OPHTH STERILE* SOLUTION. 20ml eye drops, Professional Compounding Pharmacy, 996 NW Circle Blvd. #105 Corvallis, OR 97330 |

### A-E3 sample (seed 41003)

| # | Record | Year | Rule hit | NDC | Mark | Full product_description |
|---|---|---|---|---|---|---|
| 1 | D-0350-2023#13183 | 2023 | bulk | no | correct (bulk) - excipient raw material in a 20 kg bulk container | Avicel PH- 102 NF, Microcrystalline Cellulose, NF, Ph. Eur., Jp, Net Content/Gross Weight 20.0 KG / 21.1 KG bulk container, Manufactured by: DuPont Nutrition USA, Inc., 1301 Ogletown Road, Newark, DE 19711, USA. Headquarters: DuPont Nutrition Biosciences ApS, Langebrogade 1, Copenhagen, Denmark |
| 2 | D-1193-2022#1271 | 2022 | compounding | no | correct (compounded) | Alprostadil/Papaverine/Phentolamine 60mcg/30mg/3mg/mL, 3mL-vial, Refrigerate, Tailor Made Compounding |
| 3 | D-0416-2025#767 | 2025 | compounding | yes | correct (compounded) | TESTOSTERONE PELLET 200 mg BLUNT, 1 Pellet for Subcutaneous Use, This is a Compounded Drug, Not for Resale, RX or Office Use Only, Belmar Select Outsources, 12860 W. Cedar Drive #211, Lakewood, CO 80228, NDC: 70168-0121-01 |
| 4 | D-1205-2022#1276 | 2022 | compounding | no | correct (compounded) | Glutathione 200mg/mL Preservative Free, Injectable, 30mL-vial, Refrigerate, Tailor Made Compounding |
| 5 | D-0691-2026#178 | 2026 | bulk | no | correct (bulk) | Clomiphene Citrate USP Active Pharmaceutical Ingredient (CAS : 50-41-9), Net Weight a)1 KG (NDC 84849-000-01), b) 500 g (NDC 84849-000-02), (c) 100 g (NDC 84849-000-03), Rx Only, Shimoga Chemicals Address -W-57A, MIDC Kupwad Samgli, Maharashtra, 416436, India. |
| 6 | D-0517-2025#723 | 2025 | compounding | yes | correct (compounded) | Testosterone 200 mg Pellet packaged in 1mL amber vials, Rx only, Compounded product. Qualgen 14844 Bristol Park Blvd Edmond OK 73013, NDC 69761-202-01 |
| 7 | D-0488-2026#339 | 2026 | bulk | yes | correct (bulk) | Magnesium Chloride, 6-Hydrate, Crystal, 500G per bottle, Bulk active pharmaceutical ingredient (API), Avantor Performance Materials, LLC, 100 Matsonford Road, Suite 200, Radnor, PA 19087, NDC 10106-2448-1 |
| 8 | D-0059-2024#13571 | 2023 | compounding | no | correct (compounded) | Lidocaine-phenylephrine 1%-1.5% 1mL Single Dose Vial, Rx only, Compounded by Pine Pharmaceuticals 355 Riverwalk Parkway, Tonawanda, NY 14150. |
| 9 | D-0548-2022#14765 | 2022 | bulk | yes | incorrect (bulk-finished) - finished dosage form in bulk packaging (bulk container, drum, bulk pack or pharmacy bulk package); not a drug substance, API, raw material or intermediate, and such products carry NDCs | APAP 325 mg (Acetaminophen 325 mg, Pamabrom 25 mg tablet) Bulk Container, ULTRAtab Laboratories, Inc., Highland, NY NDC 62959-700-00 |
| 10 | D-0154-2024#13141 | 2023 | compounding+bulk | yes | correct (bulk) - bulk API powder for prescription compounding | NYSTATIN 5BU, Activity (as is): 6482 Units/mg, bulk powder container, Rx Only, For Prescription Compounding, Fagron, Inc. - 2400 Pilot Knob Rd. St Paul, MN 55120. NDC 51552-0041-5 Bar code 3 51552 00415 3 |
| 11 | D-0112-2023#5038 | 2023 | compounding | no | correct (compounded) | Prostaglandin (E1) Injection Solution, 40mcg/ml, 2.5 mL Multiple-Dose vials, Rx Only, Compounded by: Akina Pharmacy, 23475 Rock Haven Way Suite 105, Sterling, VA 20166. |
| 12 | D-0414-2025#775 | 2025 | compounding | yes | correct (compounded) | TESTOSTERONE PELLET 200 mg BLUNT (with Cholesterol </=2%), 1 Pellet for Subcutaneous Use, This is a Compounded Drug, Not for Resale, RX or Office Use Only, Belmar Select Outsources, 12860 W. Cedar Drive #211, Lakewood, CO 80228, NDC: 70168-0124-01 |
| 13 | D-1227-2022#4606 | 2022 | compounding | no | correct (compounded) | Sermorelin/Glycine 2000mcg/5mg/mL, 4mL-vial, Refrigerate, Tailor Made Compounding |
| 14 | D-0117-2023#5140 | 2023 | compounding | no | correct (compounded) | TriMix Plus 001 (PGE1/Papaverine HCl/Phentolamine Mesylate) 20mcg/30mg/2mg/mL INJECTABLE, 2.5 mL Multiple-Dose vials, Rx Only, Compounded by: Akina Pharmacy, 23475 Rock Haven Way Suite 105, Sterling, VA 20166. |
| 15 | D-1192-2022#1232 | 2022 | compounding | no | correct (compounded) | Alpha Lipoic Acid 25mg/mL, 30mL-vial, Refrigerate, Tailor Made Compounding |
| 16 | D-0053-2024#12848 | 2023 | compounding | no | correct (compounded) | Calcium Gluconate Ophthalmic Irrigation Solution 1%, 500 mL bags, Rx only, Compounded by Pine Pharmaceuticals 355 Riverwalk Parkway, Tonawanda, NY 14150. |
| 17 | D-1200-2022#1270 | 2022 | compounding | no | correct (compounded) | Dexpanthenol Preservative Free 250mg/mL, 2mL-vial, Room Temperature, Tailor Made Compounding |
| 18 | D-0116-2023#5107 | 2023 | compounding | no | correct (compounded) | TriMix Injection (PGE1/Papaverine HCl/Phentolamine Mesylate) 100mcg/30mg/3mg/mL INJECTABLE, 2.5 mL Multiple-Dose vials, Rx Only, Compounded by: Akina Pharmacy, 23475 Rock Haven Way Suite 105, Sterling, VA 20166. |
| 19 | D-0538-2022#14626 | 2022 | bulk | yes | incorrect (bulk-finished) - finished dosage form in bulk packaging (bulk container, drum, bulk pack or pharmacy bulk package); not a drug substance, API, raw material or intermediate, and such products carry NDCs | HPC Tablet (Acetaminophen 110 mg, Aspirin 162 mg, Caffeine 32.4 mg, Salicylamide 152 mg) Bulk Container, ULTRAtab Laboratories, Inc., Highland, NY NDC 62969-242-00 |
| 20 | D-0648-2022#14081 | 2022 | compounding | yes | correct (compounded) | HCG 6,000iu (lyo) Human Chorionic Gonadotropin Inj., For Sub-Q or IM Use Only, Not For IV Use, Vial, Rx Only, Compounded By: Revive Rx 3831 Golf Dr., Houston, TX 77018, NDC: 88888-1739-01. |
| 21 | D-0885-2023#16311 | 2023 | bulk | yes | incorrect (bulk-finished) - finished dosage form in bulk packaging (bulk container, drum, bulk pack or pharmacy bulk package); not a drug substance, API, raw material or intermediate, and such products carry NDCs | SnoreStop Naso Spray Bulk, liquid, Distributed by Green Pharma, NDC 61152-199-99 |
| 22 | D-0298-2022#5437 | 2022 | bulk | no | incorrect (bulk-finished) - finished dosage form in bulk packaging (bulk container, drum, bulk pack or pharmacy bulk package); not a drug substance, API, raw material or intermediate, and such products carry NDCs | Klean Touch Hand Sanitizer (Ethyl Alcohol 70%) Ingredients Ethanol and Methanol, in 55-gallon drums, Aroma Release Technology, Inc., 7026 Discovery Drive, Chattanooga, TN 37416 |
| 23 | D-0553-2022#14803 | 2022 | bulk | yes | incorrect (bulk-finished) - finished dosage form in bulk packaging (bulk container, drum, bulk pack or pharmacy bulk package); not a drug substance, API, raw material or intermediate, and such products carry NDCs | Coated Back Relief Tablet (Acetaminophen 250 mg, Magnesium Salicylate 290 mg, Caffeine 50 mg) Bulk Container, ULTRAtab Laboratories, Inc., Highland, NY NDC 62959-800-00 |
| 24 | D-0760-2026#83 | 2026 | compounding+bulk | yes | correct (bulk) - API for prescription compounding | TADALAFIL USP, 0.100 KG, 0.1KG(100gm)-bag, Rx only, "For Prescription Compounding Only", Shoolin Pharma Chem LLP, Block/Survey no 408, B/H Ratnamani Tubes, Near Maruti Inox, Indrad, Kadi, Mahesania, Gujarat, 382715, India, (CAS NO 1715996-29-5), NDC 85702-002-02. |
| 25 | D-0863-2022#13800 | 2022 | compounding | yes | correct (bulk) - API for prescription compounding | Nandrolone Decanoate, USP, 500 g per plastic container, Rx Only, For Prescription Compounding, Fagron, Inc. 2400 Pilot Knob Rd., St Paul, MN 55120. NDC 51552-1564-05 |
| 26 | D-0540-2022#14059 | 2022 | bulk | yes | incorrect (bulk-finished) - finished dosage form in bulk packaging (bulk container, drum, bulk pack or pharmacy bulk package); not a drug substance, API, raw material or intermediate, and such products carry NDCs | Cherry Antacid Tablet (Calcium Carbonate 420 mg) Bulk Container, ULTRAtab Laboratories, Inc., Highland, NY NDC 62959-304-00 |
| 27 | D-0039-2023#13281 | 2022 | compounding | no | correct (compounded) | MITOMYCIN INJECTION 0.375 mg/mL SYR, 0.375 mg/mL solution, 1 mL syringe, Rx only, Vital Care Compounder, 115 S. 40th Ave., Hattiesburg, MS 39402 |
| 28 | D-0927-2023#12799 | 2023 | compounding | yes | correct (compounded) | PHENYLephrine HCl 10mg added to 0.9% Sodium Chloride 250mL, 250 mL IV Bag @60 Total volume), RX only, Advanced Compounding Solutions, 4 Constitution Way Ste L Woburn, MA 01801-1042, NDC: 71546-450-25; |
| 29 | D-0525-2022#14812 | 2022 | bulk | no | incorrect (bulk-finished) - finished dosage form in bulk packaging (bulk container, drum, bulk pack or pharmacy bulk package); not a drug substance, API, raw material or intermediate, and such products carry NDCs | Zee Cold Tabs (Acetaminophen 325 mg, Guaifenesin 100 mg, Phenylephrine HCl 5 mg Bulk Container, ULTRAtab Laboratories, Inc., Highland, NY NDC 62959-111-xx |
| 30 | D-1105-2023#14402 | 2023 | compounding | no | correct (compounded) | Semaglutide/Cyanocobalamin 2mg/0.4mg/mL, 1mLvials, Tailor Made Compounding. |
| 31 | D-0762-2026#115 | 2026 | compounding+bulk | yes | correct (bulk) - API for prescription compounding | TADALAFIL USP, 1.00 KG, 1KG(1000gm)-bag, Rx only, "For Prescription Compounding Only", Shoolin Pharma Chem LLP, Block/Survey no 408, B/H Ratnamani Tubes, Near Maruti Inox, Indrad, Kadi, Mahesania, Gujarat, 382715, India, (CAS NO 171596-29-5), NDC 85702-001-08 |
| 32 | D-1215-2022#1225 | 2022 | compounding | no | correct (compounded) | Methylcobalamin 10mg/mL, a) 1 mL-vial, b) 10mL-vial, c) 30 mL-vial, Room Temperature, Tailor Made Compounding |
| 33 | D-0034-2023#13270 | 2022 | compounding | no | correct (compounded) | LAURETH-9 INJ 2% Solution, 30 ML vial, Rx only, Vital Care Compounder, 115 S. 40th Ave., Hattiesburg, MS 39402 |
| 34 | D-0367-2026#439 | 2026 | bulk | yes | incorrect (bulk-finished) - finished dosage form in bulk packaging (bulk container, drum, bulk pack or pharmacy bulk package); not a drug substance, API, raw material or intermediate, and such products carry NDCs | BZK Antiseptic Towelettes (Benzalkonium Chloride 0.13%), 5" x7", 1000 ea Bulk, Med-Nap, Brooksville, FL 34601, Made in USA, NDC 0924-0246-02. |
| 35 | D-0054-2024#13520 | 2023 | compounding | no | correct (compounded) | Calcium Gluconate 2.5% solution for inhalation, 5mL pre-filled syringes, Rx only, Compounded by Pine Pharmaceuticals 355 Riverwalk Parkway, Tonawanda, NY 14150. |
| 36 | D-0266-2023#13204 | 2023 | compounding | no | correct (compounded) | Thiamine Hydrochloride 200 mg/2mL (100mg/mL), Riboflavin 2 mg/2mL (1mg/mL) Injection, FOR INTRAMUSCULAR OR SLOW INTRAVENOUS USE, 2 mL Sterile Single Use Vial, Preservative-Free, Rx Only, Compounded for a licensed professional or patient use by: McGuff Compounding Pharmacy Services, Inc, Santa Ana, CA 92704. |
| 37 | D-0108-2023#5309 | 2023 | compounding | no | correct (compounded) | QuadMix Super 002 (PGE1/Papaverine HCl/Phentolamine Mesylate/Atropine) 40mcg/30mg/4mg/0.4mg/mL INJECTABLE, packaged in 2.5 mL Multiple-Dose vials, Rx Only, Compounded by: Akina Pharmacy, 23475 Rock Haven Way Suite 105, Sterling, VA 20166. |
| 38 | D-0379-2026#461 | 2026 | compounding | yes | correct (bulk) - API for prescription compounding | Semaglutide, For Rx compounding use only, packaged in a) 1g, NDC 84385-106-01; b) 5g, NDC 84385-106-02; c) 10g, NDC 84385-106-06; d) 25g, NDC 84385-106-03; d) 50g, NDC 84385-106-04 Manufacturer: Harbin Jixianglong Biotech Co., Ltd., North of Baoan Road, East of Changqing Street, Limin Development Zone, Harbin, China |
| 39 | D-1207-2022#1231 | 2022 | compounding | no | correct (compounded) | Gonadorelin 100mcg/mL, 10mL per vial, Refrigerate, Tailor Made Compounding |
| 40 | D-0230-2025#824 | 2025 | bulk | no | incorrect (bulk-finished) - finished dosage form in bulk packaging (bulk container, drum, bulk pack or pharmacy bulk package); not a drug substance, API, raw material or intermediate, and such products carry NDCs | Phenylephrine HCl Injection, USP 100 mg/10 mL (10 mg/mL) vials, Rx only, Pharmacy Bulk Package (supplied as a single unit), Dist. by: Provepharm, Inc., Collegeville, PA 19426 |

## B. Miss rate of the label

Population: records with NO NDC from either source that the label does NOT flag. missed = the item is in fact a compounded or bulk product the rule did not catch.

| Era | Unflagged no-NDC records | Missed | Miss rate % | Wilson 95% | Missed by kind: compounded / bulk / both |
|---|---|---|---|---|---|
| E1 | 1,659 | 27 / 40 | 67.5 | 52.02-79.92 | 26 / 1 / 0 |
| E2 | 2,047 | 18 / 40 | 45.0 | 30.71-60.17 | 17 / 1 / 0 |
| E3 | 966 | 7 / 40 | 17.5 | 8.75-31.95 | 7 / 0 / 0 |

### B-E1 sample (seed 42001)

| # | Record | Year | Mark | Full product_description |
|---|---|---|---|---|
| 1 | D-0757-2016#8543 | 2016 | missed (compounded) | Hydromorphone HCL 25 mg/ml/Bupivacaine HCL 4 mg/ml, vol. 40 ml syringe, Rx only, Hartley Med Ctr Pharmacy, Long Beach, CA |
| 2 | D-0475-2016#3326 | 2015 | missed (compounded) | HCG 1000unit/10mL MTU vial, Rx, Western Drug Inc. 106 E. Main Street, Springerville, Arizona 85938 |
| 3 | D-1487-2014#3298 | 2014 | not | Dermamedics Post Procedure Cream, 1 ounce containers which were distributed with a SKU number of DM 1026 |
| 4 | D-0449-2016#3363 | 2015 | missed (compounded) | Sal-Acid 60% Plaster Paste, Rx, Western Drug Inc. 106 E. Main Street, Springerville, Arizona 85938 |
| 5 | D-0154-2016#8374 | 2015 | missed (compounded) | VITAMIN D3 OIL, Injectable Solution, 400,000 UNITS/ML, syringe size: 20 mL, Rx only, JD & SN Inc, DBA Moses Lake Professional Pharmacy, 1555 S. Pilgrim St. Moses Lake WA 98837, (509)764-2314 |
| 6 | D-0600-2016#8588 | 2016 | missed (compounded) | Ketamine 100 mg/mL, injectable packed in syringes, Total dosage 100 mg/ 1mL, Rx only, PHARMAKON Pharmaceuticals, Inc. |
| 7 | D-0746-2016#6419 | 2016 | missed (compounded) | Hydromorphone HCL 10 mg/ml/Bupivacaine HCL 30 mg/ml, vol. 20 ml syringe, Rx only, Hartley Med Ctr Pharmacy, Long Beach, CA |
| 8 | D-827-2013#5873 | 2013 | not | DayQuil Sinex DayTime Sinus Relief (acetaminophen 325 mg and phenylephrine HCl 5 mg) liquicaps and NyQuil Sinex NightTime Sinus Relief (acetaminophen 325 mg, doxylamine succinate 6.25 mg, and phenylephrine HCl 5 mg) liquicaps Combopack, each 48-count liquicaps per carton contains 32 DayQuil Sinex DayTime Liquicaps and 16 NyQuil Sinex NightTime Liquicaps per carton, Made In Canada, Dist. by Procter & Gamble, Cincinnati, OH 45202, UPC 3 23900 01454 1. |
| 9 | D-0785-2016#6841 | 2016 | not | Phenobarbital/Hyoscyamine/ Atropine/Scopolamine 16.2/0.1037/0.0194/0.0065 mg DONNATAL ELIXIR, 5 ml Cup grape, Alcohol 23.8%, Rx Only, MFG: Concordia, PKG BY: SAFECOR HEALTH, WOBURN, MA, C5921242304. |
| 10 | D-0064-2015#8768 | 2014 | missed (compounded) | Bupivacaine hydrochloride 0.25% injectable packaged in an amber glass injectable vial,Martin Avenue Pharmacy, 1247 Rickert Dr, Naperville, IL. |
| 11 | D-1235-2014#7525 | 2014 | not | Prolifta Dietary Supplement Prolifta, 400mg/capsule, Packaged in 1 and 2 capsule blister packs and 4, 12, and 24 capsule bottles Made in the USA Distributed by: Prolifta LLC 1+877.239.8231 www.proliftaherbal.com. |
| 12 | D-0752-2016#8548 | 2016 | missed (compounded) | Hydromorphone HCL 10 mg/ml, vol. 40 ml syringe, Rx only, Hartley Med Ctr Pharmacy, Long Beach, CA |
| 13 | D-478-2013#5956 | 2013 | missed (compounded) - no firm named; multi-dose vial with a 30-day expiration, the form of the pharmacy-compounded HCG records | HCG Inj 1250 un/ml MDV, 4 ml Subcutaneous, 30 day expiration, |
| 14 | D-0882-2016#6643 | 2016 | not | Pink Bikini capsules, (all colors and all strengths), packaged in 30-count bottle, Manufactured and Distributed by: Lucy's Weight Loss System (dba Waisted With Lucy), Arlington, TX 76010 |
| 15 | D-0431-2016#1616 | 2015 | missed (compounded) | Hydrochloric Acid 2mg Injection, Rx, Western Drug Inc. 106 E. Main Street, Springerville, Arizona 85938 |
| 16 | D-0167-2016#6562 | 2015 | missed (compounded) | Testosterone Cypionate 250 mg/mL Injection, 10 mL vial, Rx, B & B Health Mart Pharmacy, Bellflower, CA |
| 17 | D-0750-2016#8570 | 2016 | missed (compounded) | Hydromorphone HCL 25 mg/ml, vol. 40 ml syringe, Rx only, Hartley Med Ctr Pharmacy, Long Beach, CA |
| 18 | D-1183-2016#1757 | 2016 | missed (compounded) | ESTRADIOLVAL 3MG/TEST CYP 35MG/ TEST PROP 35MG/ML W/PRES. (BENZYL ETOH 2%), 3ML Vials, MEDAUS PHARMACY |
| 19 | D-1038-2015#9326 | 2015 | missed (compounded) | Rifampin 25 mg/1 mL Susp, Health Innov Pharmacy, 295 Pinehurst Ave, Southern Pines, NC 28387, (910) 246-5155 |
| 20 | D-0424-2016#3335 | 2015 | missed (compounded) | Cantharidin 0.7% Sol, Rx, Western Drug Inc. 106 E. Main Street, Springerville, Arizona 85938 |
| 21 | D-1303-2014#8363 | 2014 | not | Mangiacotti - Lemon Verbena Hand Sanitizer Spray, alcohol free, 0.5 fl. Oz., 15 mL spray bottle, UPC 870678005306, Active Ingredient Benzalkonium Chloride 0.1%, Dist by: Mangiacotti, Attleboro, MA 02703. |
| 22 | D-0145-2016#8362 | 2015 | missed (compounded) | TESTOSTERONE/ANASTROZOLE, Pellet, 120/8 mg, Rx only, JD & SN Inc, DBA Moses Lake Professional Pharmacy, 1555 S. Pilgrim St. Moses Lake WA 98837, (509)764-2314 |
| 23 | D-1456-2016#2726 | 2016 | missed (bulk) - USP chemical in 500 g bottles, a raw material | Zinc Acetate, Crystal, USP, packaged in 500 gram bottles, Spectrum Chemical MFG, CORP., New Brunswick, NJ 08901 |
| 24 | D-1041-2015#7978 | 2015 | missed (compounded) | Hydroquinone 10% Cream, Health Innov Pharmacy, 295 Pinehurst Ave, Southern Pines, NC 28387, (910) 246-5155 |
| 25 | D-0137-2016#8385 | 2015 | missed (compounded) | TESTOSTERONE, Pellet, 70 mg, Rx only, JD & SN Inc, DBA Moses Lake Professional Pharmacy, 1555 S. Pilgrim St. Moses Lake WA 98837, (509)764-2314 |
| 26 | D-0629-2016#9456 | 2016 | missed (compounded) | CEFEPIME, Packaged a) 1GM in 50ML Homepumps, b) 2GM in 100ML Homepumps, and c) 12GM in 600ML Homepumps, Rx Only. SENTARA HOME HEALTH SENTARA RX, 535 Independence Pkwy ste.300, Chesapeake, VA 23320-5176. |
| 27 | D-0523-2016#6752 | 2015 | not | HPMC Visoelastic Topical, 8,000 cps, Reference 5200, 1.5 mL in 3-mL Syringe, OASIS Medical Inc, 514 South Vermont Avenue Glendora, CA 91741 |
| 28 | D-0772-2016#6425 | 2016 | not | Rhino 7 Platinum 3000, 1 count Blister Pack, Distributed by Rhino 7, Made in USA, UPC 700729253748 |
| 29 | D-1041-2016#8771 | 2016 | not | VERMOX Tablets 100 mg; 6-count box, UPC 7501109900619 |
| 30 | D-325-2016#6526 | 2015 | missed (compounded) | Sermorelin 1000 mcg/mL SUB-Q* Injection, packaged in a) 3 mL, b) 6mL, c) 7.5ml, d) 9 mL or e) 10 mL vials, Rx only, Essential Wellness PHARMACY, 4625 N. University, Peoria, IL 61614. |
| 31 | D-240-2013#5730 | 2013 | not | TEV-TROPIN (somatropin (rDNA origin) for injection) 5 mg (15 IU). Prescription Only. Distributed By: TEVA Biologics & Specialty Products Division of Teva Pharmaceuticals USA, Sellersville, PA 18960 Manufactured in Israel. |
| 32 | D-1109-2014#3503 | 2014 | missed (compounded) - no firm named; a two-ester mixture with no commercial equivalent | Estradiol Cypionate 2mg/cc testosterone cypionoate 50mg |
| 33 | D-0426-2016#4383 | 2015 | missed (compounded) | Dexpanthanol B5 250mg/mL Injection, Rx, Western Drug Inc. 106 E. Main Street, Springerville, Arizona 85938 |
| 34 | D-0465-2016#1629 | 2015 | missed (compounded) | Tri-Test 1:1:1 300mg/mL Injection, Rx, Western Drug Inc. 106 E. Main Street, Springerville, Arizona 85938 |
| 35 | D-0448-2016#1613 | 2015 | missed (compounded) | Quad Mix Inj, Rx, Western Drug Inc. 106 E. Main Street, Springerville, Arizona 85938 |
| 36 | D-1333-2014#6131 | 2014 | not | Esbelder Fem Mezcla con L-Carnitina Suplemento Alimenticio,30 capsule bottle, Hecho en Mexico: Soluciones HGC S. de R.L. de C.V. Av. Independencia #1060 Fracc. La Rinconada, Aguascalientes, Ags. Mex. C.P. 20136. UPC 7502011000251 |
| 37 | D-300-2013#3317 | 2013 | not | Pentrexcilina Jarabe NF (dextromethorphan HBr and guaifenesin) liquid, 118 mL/ 4 fl oz bottle, Distributed by Laboratorios Nordimex Co., San Diego, CA 92154, UPC 0 91965 02001 1. |
| 38 | D-1020-2015#7928 | 2015 | missed (compounded) | Pregnenolone 20 mg SR Capsule, Health Innov Pharmacy, 295 Pinehurst Ave, Southern Pines, NC 28387, (910) 246-5155 |
| 39 | D-1329-2014#5803 | 2014 | not | Esbelin Siloutte Mezcal Herbal con L-Carnitine Suplemento Alimenticio, 30 capsule bottle, Hecho En Mexico Por: Soluciones HGC S. de R.L. de C.V. Av. Independicia #1016 Frac. La Rinconada Aguascalientes, Ags. Mex C.P. 20136, UPC 7502011000060 |
| 40 | D-0057-2015#6179 | 2014 | missed (compounded) | Alprostadil alcohol 500 mcg/mL injectable packaged in amber glass injectable vial, Martin Avenue Pharmacy, 1247 Rickert Dr, Naperville, IL. |

### B-E2 sample (seed 42002)

| # | Record | Year | Mark | Full product_description |
|---|---|---|---|---|
| 1 | D-0383-2021#12309 | 2021 | not | Triple SupremeZen Plus 3500, packaged in cardboard blisters containing one capsule per card, Distributed by Yolo Studio, Cliffside Park, NJ |
| 2 | D-1601-2019#11597 | 2019 | not | Herpes-P, 500 mg Capsules, 90-count bottles, Herbal Doctor Remedies Alhambra, CA 91801-7081 USA, 1(800) 600-0808 |
| 3 | D-1303-2019#3745 | 2019 | not | DrKids Children's Natural Cough Syrup English Ivy Leaf Organic Agave Nectar Pre-measured Single-Use 0.17 fl. oz. (5 mL), Manufactured in USA by: Unipharma, LLC. Tamarac, FL 33321, UPC 370302489019 |
| 4 | D-0207-2021#4583 | 2021 | missed (compounded) | Sodium Citrate 4% 3 mL Anticoagulation Solution (40mg/mL), Rx only, 3 mL Single Dose Syringe, SCA Pharmaceuticals, 755 Rainbow Rd., Windsor, CT, 06095, barcode 70004090025 |
| 5 | D-1113-2020#12110 | 2020 | not | Blood Clot Purger, Distributed by Herbal Doctor Remedies Alhambra, CA 91801-7081 USA, 1(800) 600-0808 |
| 6 | D-1090-2018#4926 | 2018 | missed (compounded) | P/P/P (Prostaglandin/Papaverine/Phentolamine) Injection, 0.02/30/2 mg/mL, 5 mL vial, Rx only, Ranier's Rx Laboratory, 1107 Lowry Avenue Suite A, Jeannette, PA 15644. |
| 7 | D-0601-2020#11434 | 2019 | missed (compounded) | Morphine Sulfate and Bupivacaine HCL and Baclofen and Clonidine HCL in all strengths, all doses and all packaging, AnazaoHealth 5710 Hoover Blvd Tampa, FL 33634. |
| 8 | D-0570-2017#7440 | 2017 | missed (compounded) | REVERSE DML LOTION (Ketoconazole 2%, Metronidazole 2%, sulfacetamide sodium 10%), Rx only, Synergy RX, 4901 Morena Blvd # 504-A San Diego, CA 92117 (855) 792-6676 |
| 9 | D-0967-2019#10893 | 2019 | not | Dr. King's Natural Medicine Stress Control, 59 mL, (liquid/liquide), DIN-HM 80041740 UPC 357955180524 |
| 10 | D-0259-2018#5205 | 2018 | not | Medline Concordia Nurse Bag Kit. Packaged in USA for Medline Industries, Inc., Northfield, IL 60093 |
| 11 | D-1092-2017#9872 | 2017 | not | GEC LX Laxoplex 60 capsules Dietary Supplement, 60 count bottle, Manufactured by GEC, McKinney, TX, 75070, UPC: 700580499842 |
| 12 | D-1632-2019#11504 | 2019 | not | DrKids Children's Allergy Relief Diphenhydramine HCl 12.5 mg/5 mL Antihistamine, Mixed berry Flavor, 20 Pre-measured Single-Use vials per Carton, Manufactured in USA by: Unipharma, LLC. Tamarac, FL 33321, UPC 370302255010 |
| 13 | D-1087-2017#7608 | 2017 | not | Biotech Underground Tri-Ton Hardcore Formula capsules, 90-count bottle, Distributed by: Dynamic Technical Formulations 12850 Hwy 9 Suite 600-441 Alpharetta, GA 30004 |
| 14 | D-1773-2019#14245 | 2019 | missed (compounded) - IV admixture of a commercial product prepared by an infusion pharmacy | ENTYVIO 300 MG /250 ML 0.9% NACL, Rx Only, Infusion Options, Inc. 5924 13the Ave, Brooklyn, NY 11219-4934, 718-283-7233 |
| 15 | D-0157-2021#12793 | 2020 | not | Best Choice, Clotrimazole Cream, USP 1%, Antifungal, NET WT 0.5 OZ (14.2g), Distributed by: Valu Merchandisers, CO . 5000 Kansas Ave. Kansas City, KS 66106 Made in Canada. UPC 0-70038-20355-1 |
| 16 | D-1744-2019#820 | 2019 | missed (compounded) | Oxytocin 60 units/1000 mL Lactated Ringers Intravenous Solution, Rx Only, Infusion Options, Inc. 5924 13the Ave, Brooklyn, NY 11219-4934, 718-283-7233 |
| 17 | D-0354-2021#12327 | 2021 | not | Triple SupremeZen Gold 3500, Packaged in paper packaging with a pill blister,1 capsule per box, Distributed by VIEW LIFE Distributors Los Angeles CA 90005 UPC 7 15122 05089 4 |
| 18 | D-0424-2018#1696 | 2018 | missed (compounded) | 100 mcg / mL Phenylephrine HCl (Preservative Free) Injection, 10 mL syringe, Rx only, PharMEDium Serivces, LLC |
| 19 | D-1615-2019#11512 | 2019 | not | Sperm Booster, Distributed by Herbal Doctor Remedies Alhambra, CA 91801-7081 USA, 1(800) 600-0808 |
| 20 | D-1554-2019#11663 | 2019 | not | AIR HEADS PINK LEMONADE SCENTED ANTIBACTERIAL HAND GEL (Ethyl Alcohol 62%), 1.35 fl oz / 40 mL, OTC, Distributed by: JFL Enterprises, Inc. Cleveland, Ohio 44102. |
| 21 | D-1106-2017#9513 | 2017 | not | Make Up Perfect ivory (Titanium Dioxide) SPF 10 liquid make-up, 1 oz. Net Wt. 30 ml bottle, Art. 03300, Made in Germany, Doctor Eckstein, Linde Eckstein GMBH Co. Kg, 90522 Oberasbach, Germany, UPC 4 035219 033002. |
| 22 | D-0831-2017#1591 | 2017 | missed (compounded) | Succinylcholine Chloride all strengths, all dosage forms and all packaging, Rx Only, Avella of Houston, Houston, TX 77054 |
| 23 | D-0018-2020#11817 | 2019 | missed (compounded) | C-METHYLCOBALAMIN 25MG/ML INJECTION PFS, packaged in 0.3 mL, 0.5 mL, 1 mL, and 3 mL syringes, Rx only, Colonia Care Pharmacy, 515 Inman Ave., Suite A, Colonia, N.J. 07067 |
| 24 | D-0830-2017#1636 | 2017 | missed (compounded) | Amiodarone all strengths, all dosage forms and all packaging, Rx Only, Avella of Houston, Houston, TX 77054 |
| 25 | D-1778-2019#15010 | 2019 | missed (compounded) | FOSAPREPITANT 150 mg/150 ml NS IVPB, Rx Only, Infusion Options, Inc. 5924 13the Ave, Brooklyn, NY 11219-4934, 718-283-7233 |
| 26 | D-0171-2018#7465 | 2018 | missed (compounded) | Chloramphenicol 500 mg Sulfamethoxazole 500 mg Amphotericin 50 mg Otic Powder packaged in jars, Rx Only, KRS Global Biotechnology, 791 Park of Commerce Blvd, Boca Raton, FL 33487. |
| 27 | D-1442-2020#12230 | 2020 | missed (compounded) | Vardenafil 20 mg Troche, 30 troches per bottle, MasterPharm, 115-02 Liberty Ave, Richmond Hill, NY 11419, (866) 630-5600 |
| 28 | D-1603-2019#11452 | 2019 | not | Herpes-V Balm, Distributed by Herbal Doctor Remedies Alhambra, CA 91801-7081 USA, 1(800) 600-0808 |
| 29 | D-0961-2017#3082 | 2017 | not | UPROAR All Natural Male Enhancement Herbal Dietary Supplement Capsules, supplied in 2, 4 and 10 count packages, Distributed by AH Distribution, DelRay, Beach, FL ---- UPC Code 680474229260 |
| 30 | D-0635-2018#1731 | 2018 | missed (compounded) | B-complex (B1-200mg, B2-4mg, B3-200mg,B5-4mg,B6-4mg) /mL, 5 mL amber vial, Rx only, Partell Specialty Pharmacy, 5835 S. Eastern Ave. #101, Las Vegas, NV 89119 (702) 791-3800 |
| 31 | D-0715-2021#12512 | 2021 | missed (compounded) | MORPHINE-BUPIVACAINE-FENTANYL PF 30MG-15MG-2000MCG/ML INJECTABLE 21 mL syringe, Rx only, Med Shop Total Care 470 East Loop 281 Longview, TX 75605 |
| 32 | D-0231-2018#10153 | 2018 | not | Day Cream SPF15 Cr¿me de jour FPS 15, { Avobenzone 2%, Octinoxate 7%, Oxybenzone 5%} 15 ml / 0.5 fl. oz jar. Made in Canada, Kamins Dermatologics Inc. Montreal, Quebec H9R 2Y6. Distributed by Kamins Dermatologics Montreal, Quebec H9R 2Y6 Made in Fabrique au Canada. UPC code 6 26354 10955 0 |
| 33 | D-1724-2019#11484 | 2019 | not | CVS Health Glycerin Suppositories, 50-count box, Distributed by: CVS Pharmacy, Inc. One CVS Drive Woonsocket, RI 02895. UPC 0 50428 33106 4 |
| 34 | D-0658-2021#4517 | 2021 | not | Durisan Antimicrobial Solutions (benzalkonium chloride) Hand Sanitizer, listed as 0.1% or 0.13%, Alcohol-Free, packaged in a) 18 mL Net Content 0.61 fl oz credit card size container, (UPC 8 52379 00614 1); b) 50 mL Net Content 1.69 oz bottle, (UPC 8 52379 00634 9 and 8 52379 00612 7); c) 118 mL Net Content 4 oz bottle, (UPC 8 52379 00634 9 and 8 52379 00612 9); d) 236.58 mL Net Content 8 oz bottle, (UPC 8 52379 00635 6); e) 250 mL Net Contents 8.45 oz (UPC 8 52379 00611 0); f) 300 mL Net Content 10 oz bottle, (UPC 8 52379 00697 4); g) 550 mL Net Content 18.59 oz bottle, (UPC 8 52379 00620 2) ; h) 1000 mL Net Content 33.81 oz kidney bottle dispensing 0.4 or 0.8 each actuation, (UPC 8 50008 48507 7 and 8 52379 00610 3); and i) 1 Gallon Net Content 128 oz bottle, (UPC 8 52379 00621 9); Sanit Technologies, LLC 7810 25th Court East, Unit 106 Sarasota, Florida 34243 |
| 35 | D-0368-2021#13036 | 2021 | not | IMPERIAL GOLD 2000, Male Sexual Performance Enhancement, 1 Capsule, UPC 718122040702 |
| 36 | D-0881-2021#12917 | 2021 | missed (bulk) - homeopathic bulk formula labeled For Manufacturing Use Only, an intermediate | ZTE-1020 Formula. Contents 1000ml. WHP Homeopathic Medicine, For Manufacturing Use Only, REMEDY: Aurum Metallicum 10X, Crataegus Oxyacantha 10X, Baryta Carbonica 10X, Digitalis Purpurea 10X, Zincum Muriaticum 13X, Chromium Sulphuricum 10X, Manganum Metallicum 10X, Dilution Alcohol 20%. Manufactured for Optimal Health Dimensions. RX Only, Manufactured by Washington Homeopathic Products, Inc. 260 JR Hawvermale Way, Berkeley Springs, WV, 25411. |
| 37 | D-1154-2017#9466 | 2017 | missed (compounded) | L-Glutamine 100mg, 30 mL vials, Rx only, Bella Pharma 3101 W. Devon Ave., Chicago, IL 60659, 1 (877) BELLA. |
| 38 | D-0864-2021#12565 | 2021 | not | Cinnamomum 6X, Flatulence* Sucrose/Lactose Pills, Packaged as a) 4 Dram, b) 1 oz, and Cinnamomum 30X, Flatulence* Sucrose/Lactose Pills, Packaged as 4 Dram, WHP Homeopathic Medicine, Washington Homeopathic Products 260 JR Hawvermale Way, Berkeley Springs WV 25411 |
| 39 | D-0699-2020#1344 | 2020 | missed (compounded) | BUP 30MG/ FENT 400MCG/ML INJ in 20 mL syringe Assurance Infusion (713) 533-8800 |
| 40 | D-0697-2018#10099 | 2018 | not | All Alka-Seltzer Plus¿ packages with a full front panel instant Redeemable Coupon (IRC) affixed to the individual carton. The recalled products can be identified by checking the Bayer logo located on the lower left corner of the front of the carton. If the logo has an orange or green background, the product is included in the recall. |

### B-E3 sample (seed 42003)

| # | Record | Year | Mark | Full product_description |
|---|---|---|---|---|
| 1 | D-1284-2022#13623 | 2022 | not | Arti King Refozado con Ortiga y Omega 3 Tablets, 100-count bottles, Hecho en Mexico por: "PLANTAS MEDICINALES DE MEXICO", Melchor Ocampo No. 55 Local D, Delegacion Xochimilco, C.P. 16800 Mexico, UPC 7 501031 111138 |
| 2 | D-0283-2026#475 | 2026 | not | Personal Care, Vaporizing Chest Rub, 4 oz, 12 count, UPC 048155903319 |
| 3 | D-0522-2024#1011 | 2024 | not | Bull Frog SPF 50 Amphibious Lotion SPF 50 Amphibious Lotion with Water Armor Tech, Broad Spectrum Sunscreen with UVA/UVB Protection, NEW WT. 5 FL OZ (148ML), Distributed by: Bullfrog Brands LLC, PO Box 600207, Dallas, TX 75360 USA. UPC 8 50016 52112 5 |
| 4 | D-0826-2023#13389 | 2023 | not | Lorazepam Oral Concentrate, USP, 2mg per mL, 30 mL bottles, Rx Only, Sterile, Distributed by: Akorn Operating Company, LLC., Gurnee, IL 60031. ALL NDCs |
| 5 | D-0838-2023#13460 | 2023 | not | Promethazine HCl Oral Solution, USP, 6.25 mg/5mL, 473 mL bottles, Rx Only, Distributed by: Akorn Operating Company LLC, Gurnee, IL 60031. ALL NDCs |
| 6 | D-0829-2023#13393 | 2023 | not | Moxifloxacin HCl Ophthalmic Solution, USP, 0.5%, 3 mL bottles, Rx Only, Manufactured by: Akorn, Inc., Lake Forest, IL 60045. ALL NDCs |
| 7 | D-1458-2022#1195 | 2022 | not | HYLANDS 4KIDS COLD N MUCUS RELIEF 4 FL OZ distributed to specific Family Dollar Stores 04/30/2022 through 06/10/2022. |
| 8 | D-1468-2022#1217 | 2022 | not | Colgate Anticavity Fluoride Toothpaste, OPTIC WHITE with CHARCOAL COOL MINT PASTE, Net Wt. 4.2 OZ. UPC 0 35000 97872 1. Dist. by: Colgate-Palmolive Company New York, NY 10022 U.S.A. |
| 9 | D-0053-2026#16957 | 2025 | missed (compounded) - peptide and injectable line of a compounding outsourcer; judgment from the product line | Glutathione Preserved for Injection, all strengths and presentations, GenoGenix LLC, 2840 NW 2nd Ave Ste 204 Boca Raton, FL 33431-6692 |
| 10 | D-0457-2023#1097 | 2023 | not | Purely Soothing MSM Nasal Spray, 15%, packaged in 30ml, 1.014 fl. oz bottles, Manufactured by: Pharmedica USA, Phoenix, AZ, UPC 7 31034 91380 5 |
| 11 | D-0492-2022#12657 | 2022 | not | PAINAID (acetaminophen 110 mg, aspirin 162mg, caffeine 32.4 mg, salicylamide 152mg) 2 tablet packets, Dist. by ZEE Medical Distributors, LLC Mason, OH 45040 |
| 12 | D-0781-2023#12717 | 2023 | not | Acetic Acid Otic Solution, 15 mL per bottle, Rx only, Distributed by: Akorn Operating Company LLC, Gurnee, IL 60031. ALL NDCs |
| 13 | D-0479-2022#12658 | 2022 | not | Lite Remfresh Advanced Ion-Powered Melatonin (Melatonin 0.5mg) Tablets, 36-count blisters, Physician's Seal LLC, Boca Raton, FL 33487 |
| 14 | D-0666-2026#147 | 2026 | not | Gasco Isopropyl Alcohol 70%, Net Contents: 1 US Gallon (3.78 L), Manufactured by: Gasco Industrial Corp., PO Box 1360, Gurabo, PR 00778, Made in USA |
| 15 | D-0391-2022#13109 | 2022 | not | Extra Strength Headache (acetaminophen 250 mg, aspirin 250 mg, caffeine 65 mg) tablets, packaged in 2-count tablets per packet, Manufactured for: Lil' Drug Store Products, Inc., Cedar Rapids, IA 52404 |
| 16 | D-0273-2026#532 | 2026 | not | NYQUIL COLD & FLU -32CT/2PK |
| 17 | D-0451-2024#12963 | 2024 | not | Samurai-X Honey 6800, UPC 2 56891 27553 3. |
| 18 | D-1428-2022#1216 | 2022 | not | FLEET GLYCERIN SUPPOSITORIES 50 CT distributed to specific Family Dollar Stores 04/30/2022 through 06/10/2022. |
| 19 | D-0986-2022#13481 | 2022 | missed (compounded) | Ethanol for Injection 95%, 67 mL Multi-Dose vial, Rx only, US Specialty Formulations, 1403 South Albert Street, Allentown, PA 18103, PN: 69389-06229 |
| 20 | D-0813-2023#12714 | 2023 | not | Ketorolac Tromethamine Ophthalmic Solution, 0.5%, Sterile, packaged in a) 3mL bottles, b bottles) 5 mL, and c)10 mL bottles, Rx Only, Manufactured by: Akorn, Inc., Lake Forest, IL 60045. ALL NDCs |
| 21 | D-0388-2026#407 | 2026 | not | SILINTAN 25/pills, packaged in a 25-count bottle, Shanghai Chinese Medical Works, Shanghai, China |
| 22 | D-0264-2023#5378 | 2023 | not | Ohm Sanitizer Spray (alcohol (ethyl alcohol) 80% v/v, 8 FL OZ (237 ML) bottles. |
| 23 | D-0273-2023#16580 | 2023 | missed (compounded) | Amikacin 450MG IN NS 45ML, Antibiotic, used in a HOMEPUMP, Sentara Home Infusion Pharmacy Services, 535 Independence Pkwy, Ste 300 Chesapeake, VA 23320, |
| 24 | D-1449-2022#1218 | 2022 | not | GS ANTI DIARRHEAL LOPERAMIDE CAPLET 12 CT SKU 915632 IMODIUM AD MINT 4 OZ SKU 902080 IMODIUM AD CAPLET 6 CT SKU 915628 distributed to specific Family Dollar Stores 04/30/2022 through 06/10/2022. |
| 25 | D-1366-2022#1162 | 2022 | not | Dermasil Dry Skin Treatment 10 OZ SKU 2098068 Aveeno Daily Moisturizing Lotion 5 OZ SKU 2005444 Aveeno Baby Daily Moistue Lotion 8 OZ SKU 900016 Vaseline Mens Extra Strength Body and Face Lotion 10 OZ SKU 2003674 distributed to specific Family Dollar Stores 04/30/2022 through 06/10/2022. |
| 26 | D-0225-2024#5135 | 2023 | not | Reumo Flex caplets, packaged in 30-count boxes, Manufactured by: Grupo Yepenza de Mexico, SA de CV, Comerciantes 5824 Col Arcos de Guadalupe, Zapopan Jal Mexico, UPC 7 502214 014598 |
| 27 | D-1398-2022#1157 | 2022 | not | AZO YEAST PLUS 20 CT distributed to specific Family Dollar Stores 04/30/2022 through 06/10/2022. |
| 28 | D-0200-2025#846 | 2025 | not | Systane Lubricant Eye Drops, Ultra PF, Sterile, 25 Vials (0.7mL Each), Manufactured for: Alcon Laboratories, Inc. Forth Worth, TX 76134 |
| 29 | D-0569-2026#268 | 2026 | not | FAMILY WELLNESS, ULTRA STRENGT, ANTACID TABLETS, Calcium Carbonate 1000 mg, 72 CHEWABLE TABLETS, DISTRIBUTED BY: MIDWOOD BRANDS, LLC, 500 VOLVO PKWY, CHESAPEAKE, VA 23320 USA., UP: 0 32251-92282-4. |
| 30 | D-0226-2024#5493 | 2023 | not | Kuka Flex Forte caplets, packaged in 30-count bottles, Manufactured by: Kukamonga, Gonzalez Ortega No 170 Col Centro, 44100 Guadalajara Jal, UPC 0736640810265 |
| 31 | D-0193-2023#13670 | 2023 | missed (compounded) | Apomorphine HCL 2MG/ML (10ML vial) Injectable, Rx Only, Pharmacy Innovations, 2936 W 17th St., Erie, PA. |
| 32 | D-0499-2022#12652 | 2022 | not | PAPENOL (acetaminophen 500 mg), 2 tablet packets, Manufactured for: Afassco Inc. Minden, NV 89423 |
| 33 | D-1516-2022#5153 | 2022 | missed (compounded) | MIC/B12 25/50/50/1 MG/ML Injectable, 10 ML vial, Rx only, Carolina Infusion LLC, 95 Bees Creek Road, Ridgeland, SC 29936. |
| 34 | D-0287-2026#526 | 2026 | not | Toothpaste: a) COLGATE, TOOTHPASTE, WHITENING, 2.5oz, 24ct; UPC: 035000511065; b) COLGATE, TOOTHPASTE, Regular, 2.5oz, 24ct, UPC: 035000511058; c) COLGATE, TOOTHPASTE, TRIPLE, 2.5oz, 24ct, UPC: 035000512109; d) COLGATE, TOOTHPASTE, MINT ZING, 24CT, 2.5oz, UPC: 035000744609; COLGATE, MAXFRESH, SPICY FRESH, RED TOOTH PASTE, 72CT, 150G; e) CREST, TOOTHPASTE, 40CT, 8.2OZ, UPC: 037000247081 |
| 35 | D-0216-2023#945 | 2023 | missed (compounded) | KETAMINE 50MG/ML (10ML VIAL) INJECTABLE, Rx Only, Pharmacy Innovations, 2936 W 17th St., Erie, PA. |
| 36 | D-0864-2023#13093 | 2023 | not | Tropicamide Ophthalmic Solution, USP 0.1%, 15 mL bottles, Rx only, Distributed by: Akorn Operating Company LLC, Gurnee, IL 60031. ALL NDCs |
| 37 | D-0209-2025#15573 | 2025 | not | BADGER 50, ADVENTURE SPORT MINERAL SUNSCREEN WITH CLEAR ZINC, (uncoated 25% zinc oxide), 2.4 oz., Tin, W.S. Badger Company, Inc, 768 Route 10, Gilsum NH, 03448 UPC 6 34084 47150 2 |
| 38 | D-0453-2025#752 | 2025 | not | ENDURANCE BOOST WITH HORNY GOAT WEED, 500mg, 20 capsules per carton, VEPEMVA Nutrition Supplement....rgy and Endurance, UPC X004BB9Z8N |
| 39 | D-0049-2026#17036 | 2025 | missed (compounded) - same firm and product line as E3 #9 | Calcium Chloride for Injection, all strengths and presentations, GenoGenix, LLC, 2840 NW 2nd Ave Ste 204 Boca Raton, FL 33431-6692. |
| 40 | D-0278-2026#565 | 2026 | not | Halls Cough Drops a) BAGS, MENTHOL, 12CT; b) BAGS, HONEY LEM, 12CT; c) BAGS, DEFENSE CITRUS, 12CT; d) BAGS, CHERRY, 12CT; e) M. CHERRY, 20 STK; f) BRAZIL, Cherry, 21CT/27.5G; f) LEMON. HONEY, 20CT #1180E; g) LIME FRESH, 20CT, #1182; h) MENTHOL BLUE, 20CT, #1180A; i) BRAZIL, Menthol, 21CT/27.5G, j) M . STRAWBERRY, 20 STK; k) DEFENSE, VITAMIN C, 20CT, #1181 |

## C. Pre-registered criteria

- V1: pooled precision 91.67% (110 of 120), Wilson 95% 85.34-95.41. Needs >= 85% and lower bound > 70%. **PASS**
- V2: era precisions E1 100.0%, E2 97.5%, E3 77.5%; largest gap 22.5 pp. Needs <= 15. **FAIL**
- V3: miss rates E1 67.5%, E3 17.5%; E3 - E1 = -50.00 pp. Needs <= +15. **PASS**
- **Verdict: EXPLANATION DOES NOT STAND.**
- Sensitivity, NOT the gate: if the 9 records marked incorrect as finished dosage forms in bulk packaging were counted correct, era precisions would be E1 100.0%, E2 97.5%, E3 100.0%, pooled 99.17% (CI 95.43-99.85); V1 PASS, V2 spread 2.5 pp PASS. The verdict above is computed on the marks as made; this line shows how much of it rests on that one marking decision.

**Can each criterion fail on this data?** V1 and V2 compare hand-marked counts with thresholds that a plausible outcome (for example 32 of 40 correct in one era) would breach, so both can fail. V3 compares two measured rates and can fail (here it would need an E3 miss rate above 82.5%), but it is ONE-SIDED: it tests only for the rule going blind LATE. It passes by a wide margin because the misses run the other way, and it says nothing about the large early miss rate, which Part E addresses. None of the three is rank-based. **One limit on what V3 can see:** Part B samples only records with no NDC, as the brief specifies, so V3 cannot detect the rule going blind among compounded or bulk products that DO carry an NDC. That population is in the Part D groups (a missed compounded product with an NDC would sit in "other" and raise its NDC rate). It is recorded here, not tested; testing it would be new scope.

## D. Per-year table and decomposition

Flagged = the label flags the record ("no-NDC-expected" group); other = it does not. NDC = from either source. Coverage = all records with an NDC / all records.

| Year | n | Flagged (% of n) | Other (% of n) | Flagged with NDC (%) | Other with NDC (%) | Coverage % | Flagged by compounding rule / bulk rule |
|---|---|---|---|---|---|---|---|
| 2013 | 1,377 | 678 (49.24) | 699 (50.76) | 3 (0.44) | 408 (58.37) | 29.85 | 651 / 27 |
| 2014 | 1,562 | 163 (10.44) | 1,399 (89.56) | 30 (18.4) | 971 (69.41) | 64.08 | 153 / 13 |
| 2015 | 2,020 | 1,194 (59.11) | 826 (40.89) | 87 (7.29) | 354 (42.86) | 21.83 | 719 / 478 |
| 2016 | 1,254 | 430 (34.29) | 824 (65.71) | 185 (43.02) | 356 (43.2) | 43.14 | 424 / 8 |
| 2017 | 1,073 | 333 (31.03) | 740 (68.97) | 63 (18.92) | 484 (65.41) | 50.98 | 319 / 22 |
| 2018 | 1,426 | 175 (12.27) | 1,251 (87.73) | 99 (56.57) | 752 (60.11) | 59.68 | 134 / 43 |
| 2019 | 2,152 | 375 (17.43) | 1,777 (82.57) | 96 (25.6) | 1,222 (68.77) | 61.25 | 366 / 9 |
| 2020 | 1,035 | 23 (2.22) | 1,012 (97.78) | 7 (30.43) | 545 (53.85) | 53.33 | 11 / 12 |
| 2021 | 1,016 | 188 (18.5) | 828 (81.5) | 7 (3.72) | 558 (67.39) | 55.61 | 181 / 7 |
| 2022 | 1,349 | 134 (9.93) | 1,215 (90.07) | 41 (30.6) | 899 (73.99) | 69.68 | 97 / 39 |
| 2023 | 1,252 | 90 (7.19) | 1,162 (92.81) | 34 (37.78) | 867 (74.61) | 71.96 | 66 / 28 |
| 2024 | 657 | 20 (3.04) | 637 (96.96) | 16 (80.0) | 531 (83.36) | 83.26 | 17 / 3 |
| 2025 | 765 | 26 (3.4) | 739 (96.6) | 20 (76.92) | 589 (79.7) | 79.61 | 22 / 4 |
| 2026 | 603 | 29 (4.81) | 574 (95.19) | 25 (86.21) | 475 (82.75) | 82.92 | 13 / 21 |

**Arithmetic.** For a period, coverage C = s x pF + (1 - s) x pO, where s is the flagged share, pF the NDC rate among flagged records and pO the NDC rate among other records. With bars for the pooled 2013-2026 values (pooled 2013-2026: flagged share 0.2199, NDC rate flagged 0.1848, NDC rate other 0.6586) and d for the change from the first period to the second:

- composition = ds x (pFbar - pObar)
- within-group = sbar x dpF + (1 - sbar) x dpO
- interaction = dC - composition - within-group

Shares are each part divided by dC. A negative share means that part worked against the total change.

| Comparison | Coverage from | Coverage to | Total change, pp | Composition, pp (share) | Within-group, pp (share) | Interaction, pp (share) | s from / to | pF from / to | pO from / to |
|---|---|---|---|---|---|---|---|---|---|
| 2013 -> 2026 | 29.85% | 82.92% | +53.07 | +21.05 (39.7%) | +37.88 (71.4%) | -5.86 (-11.0%) | 0.4924 / 0.0481 | 0.0044 / 0.8621 | 0.5837 / 0.8275 |
| E1 -> E3 | 38.53% | 75.59% | +37.06 | +15.73 (42.5%) | +24.40 (65.8%) | -3.07 (-8.3%) | 0.3967 / 0.0646 | 0.1237 / 0.4548 | 0.5574 / 0.7768 |

## E. What this says

- **The decomposition.** From 2013 to 2026, coverage rose +53.07 pp. Holding within-group NDC rates at their pooled values, the change in group shares accounts for +21.05 pp (39.7% of the change): composition. Holding shares at pooled values, the change in within-group NDC rates accounts for +37.88 pp (71.4%): within-group. The interaction is -5.86 pp (-11.0%). E1 to E3 gives the same ordering: composition 42.5%, within-group 65.8%, interaction -8.3%.
- **Both parts are material.** Within-group change is the larger part in both comparisons, and composition is between half and two-thirds its size (21.05 / 37.88 and 15.73 / 24.40). The claim cannot be "the trend is composition"; it has to carry both.
- **The label fails its own validation (V2), so the split above is computed with a label that is not validated.** E3 precision is lower because the bulk rule catches finished products in bulk packaging, which carry NDCs (9 of the 9 E3 errors). The per-year table is consistent with that: the flagged group's NDC rate reaches 86.21% in 2026.
- **The label also misses most compounded products in the early years** (Part B: 67.5%, 45.0% and 17.5% of unflagged no-NDC records are compounded or bulk items the rule missed, in E1, E2 and E3). V3 passes because the misses FALL over time, not because they are small. Those missed records sit in the "other" group with no NDC, which lowers the other group's early NDC rate. That moves measured change from the composition term into the within-group term, so the within-group share above is larger, and the composition share smaller, than a label without that miss pattern would give. The size of the shift is not estimated here.

## F. Limitations carried forward (not fixed here)

- The run 2 parser does not accept dotted NDCs (27854.101.01) or product-level codes with no package segment. Run 3 found them rare (three misses in 120) and left the parser unchanged.
- **A rule that would be better, recorded and NOT applied (applying it would void run 3):** the compounding signal should key on the preparer, not the word. Most missed compounded records name a pharmacy, infusion pharmacy or outsourcing facility without the stem "compound"; and the bulk signal should exclude finished dosage forms whose description says "bulk container", "bulk pack", "pharmacy bulk package" or drums of a finished product. Whether to adopt either is the author's decision; both would need their own validation run.
- Marks are one reader's judgments. The rules used are stated in `run4_marks.json` ("rules"). Judgments that rested on firm or product line rather than explicit wording carry a note.

