# DISCERN - VCEP Per-Code Spec Verification (2026-06-13)

**Scope:** independently verify and extract the per-gene ClinGen VCEP rule tables that the
`rules/vcep/specs/*.yaml` files had been holding as documented DEFAULTS (the genuine
outstanding "placeholder" item). Two independent sources were used and cross-checked:

1. **The machine-readable CSpec registry** (`cspec.genome.network/cspec/ui/svi/svi/<GN>`) -
   the authoritative criteria specifications.
2. **The VCEPs' own applied records in the ClinGen Evidence Repository** (the 2,653
   bleeding-gene variants already on the VM) - the curators' narratives state the cut-offs
   verbatim and show the strength actually applied per code. Triangulated with
   `eval/erepo_thresholds.py`.

No value below is taken on trust from any draft note; each is tied to a source.

## Verified frequency thresholds + PM2 strength

| Gene (spec) | BA1 | BS1 | PM2 (AF) | PM2 strength | Source |
|---|---|---|---|---|---|
| ITGA2B/ITGB3 GT (PD-VCEP) | >0.0024 | >0.00158 | <0.0001 | **Supporting** (509/509) | eRepo (608 GT records; narratives quote the cut-offs) |
| F8 (CFD-VCEP, GN071 v2.0.0) | >=0.000333 | >=0.0000333 | absent-in-males | **Supporting** (61/62) | CSpec GN071 + eRepo (95 records) |
| F9 (CFD-VCEP) | >=0.0000556 | >=0.0000278 | hemizygote | **Supporting** (52/52) | eRepo (71 records) |
| VWF (VWD-VCEP, GN081) | >0.1 | >0.01 | <0.0001 | **Supporting** (73/73) | CSpec GN081 + eRepo (119 records) |
| GP1BA BSS (PD-VCEP, GN079) | >=0.001 | 0.0005-0.001 | <=0.0001114 | **Supporting** (112/112) | CSpec GN079 + eRepo (140 records) |
| RUNX1 (MM-VCEP) | (not re-verified) | (not re-verified) | - | **Supporting** (1040/1054) | eRepo (PM2 strength only) |

**PM2_Supporting is confirmed across all six panels** (1,847 PM2 records total, all
Supporting, zero Moderate). This is the substantive forward-scoring fix: the loader's ACMG
default for a "PM" code is Moderate (2 pt); these VCEPs apply PM2 at Supporting (1 pt), and
PM2 is the single most-applied criterion. `code_strengths: {PM2: PP}` now encodes this.

## Computational thresholds (documented in spec notes; not yet wired into the in-silico adapter)

| Gene | PP3 | BP4 | Predictor set |
|---|---|---|---|
| F8 (GN071) | REVEL>=0.6 OR SpliceAI>=0.2 | REVEL<=0.3 AND SpliceAI<=0.1 | REVEL + SpliceAI |
| VWF (GN081) | REVEL>=0.644 OR SpliceAI>=0.5 | REVEL<=0.290 AND SpliceAI<0.1 | REVEL + SpliceAI |
| GP1BA (GN079) | REVEL>=0.644 (Sup) / >=0.773 (Mod) OR SpliceAI>=0.5 | REVEL<=0.290 AND SpliceAI=0 | REVEL + SpliceAI |

## Corrections made during verification (the reason to verify rather than trust)

1. **GN079 is the GP1BA (Bernard-Soulier) spec, NOT ITGA2B/ITGB3 (GT).** An earlier note
   (and a draft summary) mislabeled it. The GT YAML no longer claims GN079; GP1BA.yaml now
   carries GN079 with its real thresholds.
2. **F8 does NOT use CADD.** A draft claim of "F8 REVEL>=0.6 / CADD>=21" was half wrong:
   REVEL>=0.6 is the PP3 cut-off (correct), but F8 uses SpliceAI>=0.2, not CADD. Corrected.
3. **VWF does NOT use CADD at present.** A draft claim of "VWF REVEL>0.644 / CADD>20" was
   half wrong: REVEL>=0.644 is correct (PP3 Supporting); the VWD VCEP is "not using CADD at
   this time" (will consider during pilot). Corrected.
4. **F8 BS1 = 0.0000333, not 0.000167.** One eRepo record quoted 0.000167; the CSpec
   registry (authoritative) and the other records give 0.0000333. CSpec value used.
5. **F8 BA1 (0.000333) and VWF BA1 (0.1) were retrievable** after all - F8 BA1 from both
   eRepo and CSpec; VWF BA1 from CSpec GN081 (eRepo states the variant FAF then "(BA1)" but
   does not restate the cut-off, so eRepo alone could not give it).

## Honest residual status (three parts)

1. **Closed / verified:** frequency criteria (BA1/BS1/PM2) + PM2_Supporting strength for
   GT, F8, F9, VWF, GP1BA - no longer placeholders.
2. **Documented simplification, not a fillable gap:** the variant-dependent strength
   DECISION TREES (PVS1 by NMD/domain/deletion-size; PS4 by proband ratio) cannot be a
   single static strength and remain at ACMG baseline; the computational REVEL/SpliceAI
   cut-offs are documented in spec notes but not yet wired into the in-silico adapter.
3. **Still pending:** RUNX1 BA1/BS1 numeric thresholds (PM2 strength is verified); the GT
   spec PDF is image-only so the GT values rest on the eRepo applied records (authoritative
   for what the panel applied) rather than the spec PDF text; F8/F9 PM2 are encoded as low
   numeric proxies for the real "absent-in-(hemizygous)-males" rule.

This does **not** change the 93.0% ACMG-combining-fidelity number: that eval reads strengths
directly from the eRepo "Applied Evidence Codes (Met)" strings, not from these YAMLs. What
these specs fix is DISCERN's OWN forward scoring of a new variant from raw gnomAD frequency
against the gene-specific cut-off - which is the actual "VCEP gene-specific" capability.
