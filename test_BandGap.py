import pytest
from DataSet import VALLEYS, BOWING
from CalculateBandGapType import CalculateBandGapType  


def test_pure_germanium_baseline():
    """Pure Ge (xSi=0, yASn=0) must be Indirect with fundamental gap ~0.664 eV."""
    nature, eg = CalculateBandGapType(xSi=0.0, yASn=0.0)
    assert nature == "Indirect"
    assert eg == pytest.approx(0.664, abs=1e-3)


def test_pure_silicon_baseline():
    """Pure Si (xSi=1, yASn=0) must be Indirect."""
    nature, eg = CalculateBandGapType(xSi=1.0, yASn=0.0)
    assert nature == "Indirect"
    assert eg == pytest.approx(2.010, abs=1e-3)


def test_sub_crossover_ge_sn_6_percent():
    """6% Sn alloy is below the direct crossover threshold (~8.8%) and must remain Indirect."""
    nature, eg = CalculateBandGapType(xSi=0.0, yASn=0.06)
    assert nature == "Indirect"
    # Experimental photoluminescence bandgap at 300 K is ~0.58 eV
    assert eg == pytest.approx(0.58, abs=0.04)


def test_unstrained_crossover_threshold():
    """Verifies the theoretical crossover occurs near ~8.8% to 9.0% Sn."""
    # Just below crossover: 8.0% Sn -> Indirect
    nature_pre, _ = CalculateBandGapType(xSi=0.0, yASn=0.080)
    assert nature_pre == "Indirect"

    # Just above crossover: 9.5% Sn -> Direct
    nature_post, eg_post = CalculateBandGapType(xSi=0.0, yASn=0.095)
    assert nature_post == "Direct"
    assert eg_post == pytest.approx(0.51, abs=0.04)


def test_published_laser_alloy_11_percent():
    """11% Sn alloy (optically pumped laser demo) must be Direct."""
    nature, eg = CalculateBandGapType(xSi=0.0, yASn=0.11)
    assert nature == "Direct"
    # Literature room-temperature direct gap is ~0.49 eV
    assert eg == pytest.approx(0.49, abs=0.04)


def test_published_laser_alloy_12_6_percent():
    """12.6% Sn alloy (first demonstrated bulk GeSn laser) must be Direct."""
    nature, eg = CalculateBandGapType(xSi=0.0, yASn=0.126)
    assert nature == "Direct"
    # Literature room-temperature direct gap is ~0.47 eV
    assert eg == pytest.approx(0.47, abs=0.04)


def test_published_diode_laser_15_percent():
    """15% Sn alloy (electrically injected diode laser) must be Direct with Eg > 0."""
    nature, eg = CalculateBandGapType(xSi=0.0, yASn=0.15)
    assert nature == "Direct"
    # Literature room-temperature direct gap is ~0.40 eV
    assert eg == pytest.approx(0.40, abs=0.04)
    assert eg > 0.0, "Must be a semiconductor, not semimetallic!"


def test_silicon_rich_alloy_is_indirect():
    """Adding Silicon increases the bandgap and forces the alloy Indirect."""
    nature, eg = CalculateBandGapType(xSi=0.20, yASn=0.05)
    assert nature == "Indirect"
    assert eg > 0.70