# prosail-sensitivity

Sensitivity analysis of the PROSAIL canopy reflectance model, using the Python package `prosail`. Status: incomplete.

## Content

| Script | Content |
|---|---|
| `src/01_scripts/script_calibrage.py` | Compares a PROSAIL spectrum (parameters set manually, similar to those of the IVVRM) with the IVVRM reference spectrum `data/spectre_ivvrm.txt`: NDVI, RE-NDVI, NDWI, RMSE, MAE and R². Figure: `images/01/comparaison_ivvrm.png`. |
| `src/02_scripts/spectre_ref.py` | Computation of vegetation indices (`compute_indices`) and reference spectrum figure (`images/02/spectre_ref.png`). |
| `src/02_scripts/var_psoil_ind.py` | Effect of `psoil` (with `rsoil` = 1.0) on NDVI, SAVI, TCARI/OSAVI, RE-NDVI, NDRE and NDII for LAI from 0 to 6, and LAI from which the variation with `psoil` falls below a threshold. Figures: `images/02/effet_psoil_<index>.png`. |
| `src/02_scripts/var_psoil_spec.py` | Effect of `psoil` on reflectance at 550, 670, 705, 720, 750, 790, 800, 819 and 1649 nm for LAI from 0 to 6. Figures: `images/02/effet_psoil_<wavelength>.png` (670, 819 and 1649 nm) and `images/02/heatmap_attenuation.png`. |
| `src/02_scripts/test_spectre_sol.py` | Compares the PROSAIL internal soil spectrum (mix of two soil spectra weighted by `psoil`) with a USGS soil spectrum (`data/brown_loamy_sand.txt`): RMSE, MAE and R². |

## Requirements

Python 3 with `prosail`, `numpy`, `matplotlib` and `scipy`.
