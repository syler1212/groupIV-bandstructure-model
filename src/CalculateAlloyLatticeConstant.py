from src.DataSet import LATTICE_A, LATTICE_BOWING_VALUES, A_C_VALLEY_Values, ELASTIC_CONSTANTS


def CalculateLatticeConstant(xSi, yASn):
    """
    Computes the ternary alloy lattice parameter using quadratic Vegard's law
    with pairwise bowing corrections.
    """
    zGe = 1 - xSi - yASn

    SiLatticeConstant  = LATTICE_A['Si']
    GeLatticeConstant  = LATTICE_A['Ge']
    ASnLatticeConstant = LATTICE_A['ASn']

    SiGeLatticeBowing  = LATTICE_BOWING_VALUES['SiGe']
    GeASnLatticeBowing = LATTICE_BOWING_VALUES['GeASn']
    SiASnLatticeBowing = LATTICE_BOWING_VALUES['SiASn']

    LinearLatticeConstant = (xSi * SiLatticeConstant) + (yASn * ASnLatticeConstant) + (zGe * GeLatticeConstant)
    BowingLatticeConstant = (xSi * yASn * SiASnLatticeBowing) + (yASn * zGe * GeASnLatticeBowing) + (xSi * zGe * SiGeLatticeBowing)

    AlloyLatticeConstant = LinearLatticeConstant - BowingLatticeConstant

    return AlloyLatticeConstant


def Calculate_A_C(xSi, yASn):
    """
    Interpolates conduction band hydrostatic deformation potentials 
    for Gamma and L valleys across alloy fractions.
    """
    zGe = 1 - xSi - yASn

    ACgammaSi  = A_C_VALLEY_Values['Si']['Gamma']
    ACgammaGe  = A_C_VALLEY_Values['Ge']['Gamma']
    ACgammaASn = A_C_VALLEY_Values['ASn']['Gamma']

    AC_L_Si  = A_C_VALLEY_Values['Si']['L']
    AC_L_Ge  = A_C_VALLEY_Values['Ge']['L']
    AC_L_ASn = A_C_VALLEY_Values['ASn']['L']

    AC_gamma_alloy = (xSi * ACgammaSi) + (yASn * ACgammaASn) + (zGe * ACgammaGe)
    AC_L_alloy     = (xSi *  AC_L_Si)  + (yASn * AC_L_ASn)  + (zGe * AC_L_Ge)

    return AC_gamma_alloy, AC_L_alloy


def CalculateElasticConstants(xSi, yASn):
    """Linear interpolation of C11 and C12 elastic stiffness constants."""
    zGe = 1 - xSi - yASn
    c11 = xSi * ELASTIC_CONSTANTS['Si']['C11'] + zGe * ELASTIC_CONSTANTS['Ge']['C11'] + yASn * ELASTIC_CONSTANTS['ASn']['C11']
    c12 = xSi * ELASTIC_CONSTANTS['Si']['C12'] + zGe * ELASTIC_CONSTANTS['Ge']['C12'] + yASn * ELASTIC_CONSTANTS['ASn']['C12']
    return c11, c12


def CalculateBiaxialStrain(xSi, yASn, material=None):
    """
    Calculates conduction valley energy corrections under pseudomorphic biaxial strain.
    If no substrate material is specified, returns 0 strain (bulk/relaxed layer).
    """
    if material is None:
        return 0.0, 0.0

    AlloyLatticeConstant = CalculateLatticeConstant(xSi, yASn)
    SubstrateLatticeConstant = LATTICE_A[material]

    # In-plane lattice mismatch strain (epsilon_xx = epsilon_yy)
    InPlaneStrain = ((SubstrateLatticeConstant - AlloyLatticeConstant) / AlloyLatticeConstant)
   
    # C11 and C12 are the crystal's elastic stiffness constants
    C11, C12 = CalculateElasticConstants(xSi, yASn)
    
    # Out-of-plane vertical strain along growth axis [001]
    OutOfPlaneStrain = (-2) * (C12 / C11) * InPlaneStrain

    # Hydrostatic Strain (epsilon_vol / Volume Change)
    epsilonVol = (2 * InPlaneStrain) + OutOfPlaneStrain

    # Shear (Axial) Strain (epsilon_Ax / Shape Distortion)
    epsilonAx = OutOfPlaneStrain - InPlaneStrain

    AC_gamma_alloy, AC_L_alloy = Calculate_A_C(xSi, yASn)

    # Hydrostatic energy shift of the conduction band in Gamma and L valleys
    HydrostaticGammaEnergyChange = epsilonVol * AC_gamma_alloy
    HydrostaticLEnergyChange = epsilonVol * AC_L_alloy
    
    # Conduction band shear shifts (Gamma is isotropic, L shear splits but averages to 0)
    ShearGammaEnergyChange = 0.0
    ShearLEnergyChange = 0.0
    
    EgammaStrainCorrection = HydrostaticGammaEnergyChange + ShearGammaEnergyChange
    ELStrainCorrection = HydrostaticLEnergyChange + ShearLEnergyChange

    return EgammaStrainCorrection, ELStrainCorrection
