# groupIV-bandstructure-model

A computational physics tool designed to model the electronic band structure, direct-indirect conduction valley crossovers, and pseudomorphic strain dynamics in ternary Silicon-Germanium-Tin (SiₓGe₁₋ₓ₋ᵧSnᵧ) group-IV semiconductor alloys.

## Features
- **Band Structure & Nonlinear Bowing:** Calculates the Γ (direct) and L (indirect) conduction valleys using composition-dependent quadratic Vegard deviations.
- **Pseudomorphic Biaxial Strain:** Evaluates in-plane lattice mismatch, out-of-plane Poisson expansion/compression, and hydrostatic deformation potentials (a_c) for growth across different substrates.
- **Interactive Band Diagram UI:** Real-time Matplotlib dashboard providing dynamic E vs. k dispersion plots with live compositional sliders.
- **Literature Validation Suite:** Rigorous unit tests via pytest benchmarking direct-gap thresholds against published photoluminescence and demonstrated GeSn laser compositions (8.8% to 15% Sn).
