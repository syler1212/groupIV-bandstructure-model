from DataSet import VALLEYS, BOWING
from CalculateAlloyLatticeConstant import CalculateBiaxialStrain


class BandGapResult(tuple):
    """
    2-tuple (BandGap, eg) for backwards compatibility with existing tests,
    while also exposing e_gamma and e_l for the UI.
    """
    def __new__(cls, band_gap, eg, e_gamma, e_l):
        return super().__new__(cls, (band_gap, eg))

    def __init__(self, band_gap, eg, e_gamma, e_l):
        self.e_gamma = e_gamma
        self.e_l = e_l


def CalculateBandGapType(xSi, yASn, material=None):
    """
    Evaluates Gamma and L valley energy levels using Vegard's law with 
    nonlinear bowing parameters, applies strain corrections, and identifies
    whether the fundamental gap is Direct or Indirect.
    """
    zGe = 1 - xSi - yASn
    EgammaStrainCorrection, ELStrainCorrection = CalculateBiaxialStrain(xSi, yASn, material)

    EgammaSi  = VALLEYS['Si']['Gamma']
    EgammaGe  = VALLEYS['Ge']['Gamma']
    EgammaASn = VALLEYS['ASn']['Gamma']

    SiGeGammaBowing  = BOWING['SiGe']['Gamma']
    GeASnGammaBowing = BOWING['GeASn']['Gamma']
    SiASnGammaBowing = BOWING['SiASn']['Gamma']

    # Linear Vegard Average + Bowing for Gamma valley
    EgammaLinear = xSi * EgammaSi + zGe * EgammaGe + yASn * EgammaASn
    EgammaBowing = xSi * yASn * SiASnGammaBowing + xSi * zGe * SiGeGammaBowing + yASn * zGe * GeASnGammaBowing
    
    EgammaFinal = (EgammaLinear - EgammaBowing) + EgammaStrainCorrection
    
    E_L_Si  = VALLEYS['Si']['L']
    E_L_Ge  = VALLEYS['Ge']['L']
    E_L_ASn = VALLEYS['ASn']['L']

    SiGeLBowing  = BOWING['SiGe']['L']
    GeASnLBowing = BOWING['GeASn']['L']
    SiASnLBowing = BOWING['SiASn']['L']

    # Linear Vegard Average + Bowing for L valley
    E_L_Linear = xSi * E_L_Si + zGe * E_L_Ge + yASn * E_L_ASn
    E_L_Bowing = xSi * yASn * SiASnLBowing + xSi * zGe * SiGeLBowing + yASn * zGe * GeASnLBowing
    
    E_L_Final = (E_L_Linear - E_L_Bowing) + ELStrainCorrection

    # Determine fundamental bandgap nature
    if EgammaFinal <= E_L_Final:
        BandGap = 'Direct'
        eg = EgammaFinal
        WaveLength = 1.24 / eg if eg > 0 else 'semimetallic'
    else:
        BandGap = 'Indirect'
        eg = E_L_Final
        WaveLength = 'no wavelength'

    return BandGapResult(BandGap, eg, EgammaFinal, E_L_Final)