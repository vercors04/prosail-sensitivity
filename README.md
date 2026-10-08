# prosail-sensitivity

Sensitivity analysis of the PROSAIL canopy reflectance model, using the Python package `prosail`. Status: incomplete.

## Content

| Part | Location | Content |
|---|---|---|
| 1. Calibration | `src/01_scripts/` | Adjustment of PROSAIL parameters to a reference spectrum (IVVRM, `data/spectre_ivvrm.txt`). Figures in `images/01/`. |
| 2. Soil brightness | `src/02_scripts/` | Effect of the `psoil` parameter on the simulated spectrum and on vegetation indices (NDVI, NDRE, RE-NDVI, SAVI, NDII, TCARI/OSAVI). Soil spectrum: `data/brown_loamy_sand.txt`. Figures in `images/02/`. |
| Exploration | `notebooks/exploration.ipynb` | Exploratory notebook. |

## Requirements

Python 3 with `prosail`, `numpy` and `matplotlib`.
