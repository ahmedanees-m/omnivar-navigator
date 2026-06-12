# DISCERN — manuscript outline (Phase 11)

**Target:** npj Genomic Medicine (primary); Genome Medicine / Genetics in Medicine.
Preprint: medRxiv. Pre-registration: OSF (before validation). TRIPOD+AI / DECIDE-AI.

> Lock this skeleton + `discern_claims_map.md` BEFORE the reader study (Gate G5).

1. **Introduction** — inherited bleeding disorders are misdiagnosed because look-alike
   diseases converge on one phenotype via shared pathways; the harm is treatment-changing;
   >60% VUS; PP4 needs a disease model, so diagnosis and VUS-resolution are one problem.
2. **Methods**
   - The coupled joint model `P(D,V|E)` (each evidence once; PP4 = disease→variant coupling).
   - VCEP-anchored genetics, decomposed per code and partitioned by owning factor (the
     circularity fix; the VCEP-reconstruction guarantee).
   - Phenotype LRs with pertinent negatives (LIRICAL principle).
   - Sparse-LR uncertainty → calibrated abstention.
   - Management-aware safety interlock; cheapest decisive next observation (EIG over joint);
     partial-input mode; provenance-tagged six-cluster knowledge base.
3. **Results**
   - **Reader study** (headline): non-specialists with vs without DISCERN — accuracy, time,
     correct next-test, harmful-management avoidance.
   - **VUS reclassification** vs VCEP/ClinVar 3-star (echoing Ross 2021 29%→20% on Glanzmann);
     the VCEP-reconstruction (no-inflation) check.
   - **Management-aware misdiagnosis-rescue** on documented mislabelled cases (case-control,
     honest power).
   - **Calibration + confident-and-wrong rate**; credible-interval coverage.
   - **South Indian Glanzmann cohort** — real, ancestry-relevant (GT vs LAD-III).
   - **Generalization** — new clusters via YAML only.
4. **Discussion** — disambiguates within known clusters (not novel-gene discovery); bounded
   by sparse LRs (hence abstention); decision-support, not automation; honest negatives.
5. **Data & Code Availability** — repo + Zenodo DOIs; the discrimination KB as a citable,
   maintainable resource (ISTH SSC / ClinGen VCEP partnership). No real patient data public.

**Figures:** (1) reader-study accuracy/time; (2) VUS-reclass vs 3-star; (3) misdiagnosis-
rescue; (4) GT/LAD-III mechanism case; (5) calibration + confident-wrong; (6) equity /
partial-input next-observation; (7) joint-model schematic (circularity handling).
