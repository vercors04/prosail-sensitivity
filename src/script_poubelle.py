import prosail
import numpy as np
import spyndex

# Paramètres PROSAIL
params = dict(
    n=1.5, cab=40, car=10, cbrown=0.25,
    cw=0.03, cm=0.012, ant=2.0,
    lidfa=30, typelidf=2, hspot=0.01,
    tts=30, tto=0, psi=0,
    psoil=0.7, rsoil=0.35,
    prospect_version='D'
)

# Simuler un spectre
s = prosail.run_prosail(lai=3, **params)

# Extraire les bandes nécessaires
R445  = s[445  - 400]
R475  = s[475  - 400]
R510  = s[510  - 400]
R531  = s[531  - 400]
R550  = s[550  - 400]
R570  = s[570  - 400]
R670  = s[670  - 400]
R680  = s[680  - 400]
R700  = s[700  - 400]
R705  = s[705  - 400]
R750  = s[750  - 400]
R800  = s[800  - 400]
R860  = s[860  - 400]
R1240 = s[1240 - 400]
R1600 = s[1600 - 400]

# Afficher les détails des indices pertinents
print("=== Détails des indices (source : Awesome Spectral Indices) ===\n")
for nom in ['NDVI', 'SAVI', 'OSAVI', 'MSAVI', 'EVI',
            'RENDVI', 'TCARI', 'TCARIOSAVI', 'SIPI',
            'NDWI', 'NDMI']:
    idx = spyndex.indices[nom]
    print(f"{nom} — {idx.long_name}")
    print(f"  Formule   : {idx.formula}")
    print(f"  Bandes    : {idx.bands}")
    print(f"  Référence : {idx.reference}")
    print()

# Calculer les indices manuellement
print("=== Valeurs calculées sur spectre PROSAIL (LAI=3, Cab=40) ===\n")

ndvi        = (R800 - R670) / (R800 + R670)
savi        = (R800 - R670) / (R800 + R670 + 0.5) * 1.5
osavi       = (R800 - R670) / (R800 + R670 + 0.16)
msavi2      = (2*R800 + 1 - np.sqrt((2*R800+1)**2 - 8*(R800-R670))) / 2
evi         = 2.5 * (R800-R670) / (R800 + 6*R670 - 7.5*R475 + 1)
rendvi      = (R750 - R705) / (R750 + R705)
tcari       = 3 * ((R700-R670) - 0.2*(R700-R550)*(R700/R670))
osavi_      = (R800 - R670) / (R800 + R670 + 0.16)
tcari_osavi = tcari / osavi_
sipi        = (R800 - R445) / (R800 - R680)
ndwi        = (R860 - R1240) / (R860 + R1240)
ndmi        = (R800 - R1600) / (R800 + R1600)

indices = {
    'NDVI':        ndvi,
    'SAVI':        savi,
    'OSAVI':       osavi,
    'MSAVI2':      msavi2,
    'EVI':         evi,
    'RE-NDVI':     rendvi,
    'TCARI':       tcari,
    'TCARI/OSAVI': tcari_osavi,
    'SIPI':        sipi,
    'NDWI':        ndwi,
    'NDMI':        ndmi,
}

for nom, val in indices.items():
    print(f"{nom:<15} = {val:.4f}")