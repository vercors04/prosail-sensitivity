import prosail
import numpy as np
import matplotlib.pyplot as plt



#======= param a la main =======#
# param similaire à celui de l'IVVRM
# params: dict[str, float | str] = dict(
#     n=1.5, cab=40, car=10, cbrown=0.25,
#     cw=0.03, cm=0.012, ant=2.0,
#     lidfa=30, typelidf=2, hspot=0.01,
#     tts=30, tto=0, psi=0,
#     psoil=0.5, rsoil=0.8,
#     prospect_version='D'
# )

params = dict(
    n=1.5, cab=40, car=10, cbrown=0.0,
    cw=0.03, cm=0.012, ant=0.0,
    lidfa=30, typelidf=2, hspot=0.01,
    tts=30, tto=0, psi=0,
    prospect_version='D'
)

wl = np.arange(400, 2501)
s  = prosail.run_prosail(lai=3, **params)

# indices tests
ndvi   = (s[800 - 400]- s[670 - 400]) / (s[800 - 400] + s[670 - 400])
rendvi = (s[750 - 400] - s[705 - 400]) / (s[750 - 400] + s[705 - 400])
ndwi   = (s[800 - 400] - s[1600 - 400]) / (s[800 - 400] + s[1600 - 400])

print("=== Python ===")
print(f"NDVI    = {ndvi:.4f}")
print(f"RE-NDVI = {rendvi:.4f}")
print(f"NDWI    = {ndwi:.4f}")




#======= IVVRM =======#
data    = np.loadtxt('data/spectre_ivvrm.txt', skiprows=1)  # séparateur tab par défaut
wl_iv   = data[:, 0]
refl_iv = data[:, 1]  


ndvi_iv   = (refl_iv[800-400] - refl_iv[670-400]) / (refl_iv[800-400] + refl_iv[670-400])
rendvi_iv = (refl_iv[750-400] - refl_iv[705-400]) / (refl_iv[750-400] + refl_iv[705-400])
ndwi_iv   = (refl_iv[800-400] - refl_iv[1600-400]) / (refl_iv[800-400] + refl_iv[1600-400])

print("\n=== IVVRM ===")
print(f"NDVI    = {ndvi_iv:.4f}")
print(f"RE-NDVI = {rendvi_iv:.4f}")
print(f"NDWI    = {ndwi_iv:.4f}")

print("\n=== Écarts ===")
print(f"ΔNDVI    = {abs(ndvi - ndvi_iv):.4f}")
print(f"ΔRE-NDVI = {abs(rendvi - rendvi_iv):.4f}")
print(f"ΔNDWI    = {abs(ndwi - ndwi_iv):.4f}")





#======= Comparaison spectres =======#
# ----erreurs-----
rmse = np.sqrt(np.mean((s - refl_iv)**2))
mae  = np.mean(np.abs(s - refl_iv))
r2   = 1 - np.sum((s - refl_iv)**2) / np.sum((refl_iv - np.mean(refl_iv))**2)
print("\n=== Erreurs ===")
print(f"RMSE = {rmse:.6f}")
print(f"MAE  = {mae:.6f}")
print(f"R²   = {r2:.6f}")

# --- Figure ---
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(wl,    s ,  'g-',  linewidth=2, label='Python')
ax.plot(wl_iv, refl_iv , 'b--', linewidth=1, label='IVVRM')
ax.set_xlabel('Wavelength [nm]')
ax.set_ylabel('Reflectance')
ax.set_title('Comparaison Python vs IVVRM')
ax.set_xlim(400, 2500)
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('images/01/comparaison_ivvrm.png', dpi=150)
plt.close()
print("\nFigure sauvegardée.")