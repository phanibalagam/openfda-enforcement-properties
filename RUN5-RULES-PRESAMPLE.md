# A15 Run 5 - label v2 rule text, written BEFORE any run 5 sample was drawn

SHA-256 of the rule text block below: `85f19758a6c8c1f20f4cf1117cc2fa99fb979e8b9c1ce1f8aa4593a2b6993d09`

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
