"""v3.1 Track A2: novel-variant intrinsic scoring + PVS1/PS4 strength trees."""
from core.schemas import Strength
from rules.point_engine import Classification
from rules.variant_scoring import Annotations, ps4_strength, pvs1_strength, score_variant


def test_high_frequency_variant_is_benign():
    sv = score_variant("F8", "x", Annotations(af=0.01))   # F8 BA1 = 0.000333
    assert "BA1" in sv.codes
    assert sv.classification == Classification.B


def test_rare_lof_with_nmd_is_pathogenic_leaning():
    sv = score_variant("F8", "x", Annotations(af=0.0, consequence="frameshift", nmd_predicted=True))
    assert any(c.startswith("PVS1_VeryStrong") for c in sv.codes)
    assert "PM2_Supporting" in sv.codes                    # F8 applies PM2 at Supporting
    assert sv.classification in (Classification.P, Classification.LP)


def test_missing_predictors_gives_reduced_confidence():
    sv = score_variant("F8", "x", Annotations(af=0.0))     # no REVEL/splice provided
    assert sv.confidence.startswith("reduced")


def test_gene_without_spec_is_reduced_confidence():
    sv = score_variant("SERPINF2", "x", Annotations(af=0.0))   # no VCEP spec -> Gate G2
    assert sv.covered is False
    assert sv.confidence.startswith("reduced")


def test_computational_pp3_and_bp4():
    hi = score_variant("F8", "x", Annotations(af=0.0, revel=0.9, splice=0.0))
    assert "PP3_Supporting" in hi.codes
    lo = score_variant("VWF", "x", Annotations(af=0.005, revel=0.1, splice=0.0))  # VWF BP4 REVEL<=0.290
    assert "BP4_Supporting" in lo.codes


def test_pvs1_tree_levels():
    assert pvs1_strength(Annotations(consequence="frameshift", nmd_predicted=True)) == Strength.PVS
    assert pvs1_strength(Annotations(consequence="frameshift", nmd_predicted=False,
                                     in_functional_domain=True)) == Strength.PS
    assert pvs1_strength(Annotations(consequence="frameshift", nmd_predicted=False)) == Strength.PM
    assert pvs1_strength(Annotations(consequence="missense")) is None


def test_ps4_proband_ratio_tree():
    assert ps4_strength(Annotations(proband_count=20)) == Strength.PS
    assert ps4_strength(Annotations(proband_count=6)) == Strength.PM
    assert ps4_strength(Annotations(proband_count=2)) == Strength.PP
    assert ps4_strength(Annotations(proband_count=None)) is None
