import numpy as np
from scipy.interpolate import interp1d
import prosail

## ===== Chargement spectre USGS ===== ##
data = np.loadtxt('data/brown_loamy_sand.txt', skiprows=21)

wl_um   = data[:, 0] #longueur d'onde pas dans le bon sens 
refl_pct = data[:, 1] #refl en pourcentage, pas en fraction et pareil pas bon sens

# inversion sens 
wl_um    = wl_um[::-1]
refl_pct = refl_pct[::-1]

# garder bonne longueur d'onde
mask = (wl_um >= 0.4) & (wl_um <= 2.5)
wl_um    = wl_um[mask]
refl_pct = refl_pct[mask]

# Convertir µm vers nm et % vers fraction
wl_nm   = wl_um * 1000
refl    = refl_pct / 100.0

# on a pas tt les pts de 400 à 2500 nm, on va devoir interpoler pour les utiliser dans PROSAIL
wl_prosail = np.arange(400, 2501)
f = interp1d(wl_nm, refl, bounds_error=False,
             fill_value=(refl[0], refl[-1])) #interpolation linéaire, fill_value : si une longueur d'onde est hors plage, on utilise la première ou dernière valeur connue
sol_usgs = f(wl_prosail) 
print ("Sepctre USGS (interpolé pour prosail) :")
print(f"Réflectance à 670 nm  : {sol_usgs[270]:.3f}")
print(f"Réflectance à 800 nm  : {sol_usgs[400]:.3f}")
print(f"Réflectance à 1600 nm : {sol_usgs[1200]:.3f}")

params = dict(
    n=1.5, cab=40, car=10, cbrown=0.25,
    cw=0.03, cm=0.012, ant=2.0,
    lidfa=30, typelidf=2, hspot=0.01,
    tts=30, tto=0, psi=0,
    prospect_version='D'
)

s1 = prosail.run_prosail(lai=3, rsoil0=sol_usgs, **params)




print()
## ===== Spectre fait main ===== ##
psoil = 0.8
rsoil = 1.0
s2  = prosail.run_prosail(lai=3, psoil=psoil, rsoil=rsoil,**params)

from prosail import spectral_library
spectra     = spectral_library.get_spectra()
sol_interne = rsoil * (psoil * spectra.soil.rsoil1 + (1 - psoil) * spectra.soil.rsoil2)
print (f"Sepctre interne psoil={psoil}, rsoil={rsoil} :")
print(f"Réflectance à 670 nm  : {sol_interne[270]:.3f}")
print(f"Réflectance à 800 nm  : {sol_interne[400]:.3f}")
print(f"Réflectance à 1600 nm : {sol_interne[1200]:.3f}")


print()
rmse = np.sqrt(np.mean((sol_interne - sol_usgs)**2))
mae  = np.mean(np.abs(sol_interne - sol_usgs))
ss_res = np.sum((sol_interne - sol_usgs)**2)
ss_tot = np.sum((sol_usgs - np.mean(sol_usgs))**2)
r2   = 1 - ss_res / ss_tot

print(f"RMSE : {rmse:.4f}")
print(f"MAE  : {mae:.4f}")
print(f"R²   : {r2:.4f}")