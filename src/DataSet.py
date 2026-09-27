# Valley parameters at 300 K (in eV)
VALLEYS = {
    'Ge':   {'Gamma': 0.800, 'L': 0.664},
    'Si':   {'Gamma': 4.180, 'L': 2.010},
    'ASn':  {'Gamma': -0.413, 'L': 0.090}
}

# Non-linear bowing parameters (in eV)
BOWING = {
    'SiGe':  {'Gamma': 0.21, 'L': 0.00},
    'GeASn': {'Gamma': 2.10, 'L': 0.80},
    'SiASn': {'Gamma': 1.30, 'L': 0.00}
}

ELEMENTS_BAND_GAP_E = {
    'Ge': 0.66,
    'Si': 1.12,
    'A-Sn': 0.00
}

# Bandgap Pairwise bowing parameters (eV)
BOWING_COMBO_VALUES = {
    'SiGe': 0.21,
    'GeA-Sn': 2.10,
    'SiA-Sn': 1.30
}

# Γ-point (Zone Center, k = 0) in units of 2π/a
ELEMENTS_ROE_Valley_POS = {
    'Si':   (0.0, 0.0, 0.0),
    'Ge':   (0.0, 0.0, 0.0),
    'a-Sn': (0.0, 0.0, 0.0)
}

# Δ-valley (along [100] direction toward X) in units of 2π/a
# For Si: sits ~85% along the [100] axis
# For Ge: sits ~85% along [100] (secondary conduction valley above L)
# For a-Sn: Δ-line approaches the zone-boundary X-point (1.0, 0.0, 0.0)
ELEMENTS_Delta_Valley_POS = {
    'Si':   (0.85, 0.0, 0.0),
    'Ge':   (0.85, 0.0, 0.0),
    'a-Sn': (1.00, 0.0, 0.0)
}

# Lattice constants at 300 K (Angstroms)
LATTICE_A = {
    "Si": 5.431,
    "Ge": 5.658,
    "ASn": 6.489
}

# Real lattice constant bowing parameters in Angstroms (Å)
# From published literature (e.g., J. Non-Cryst. Solids / PRB):
LATTICE_BOWING_VALUES = {
    'SiGe':  -0.026,   # Å (small negative deviation)
    'GeASn':  0.166,   # Å (often taken between 0.041 and 0.166 Å)
    'SiASn':  0.000    # Å (typically approximated as 0.0 due to extreme immiscibility)
}

# Conduction band hydrostatic deformation potentials a_c (eV)
A_C_VALLEY_Values = {
    'Ge':   {'Gamma': -8.24,  'L': -1.54},
    'Si':   {'Gamma': -10.50, 'L': -1.80},
    'ASn':  {'Gamma': -6.00,  'L': -2.14}
}

# Elastic stiffness constants (in GPa) for biaxial strain ratio C12/C11
ELASTIC_CONSTANTS = {
    'Si':  {'C11': 165.8, 'C12': 63.9},
    'Ge':  {'C11': 128.5, 'C12': 48.3},
    'ASn': {'C11': 69.0,  'C12': 29.3}
}