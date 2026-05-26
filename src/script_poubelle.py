import prosail
import numpy as np
import matplotlib.pyplot as plt

# Paramètres exacts du document Word — figure angle solaire
params_base = dict(
    n=1.5, cab=40, car=8, cbrown=0,
    cw=0.01, cm=0.009, ant=0.0,
    lidfa=-0.35, lidfb=-0.15, typelidf=1,
    hspot=0.01,
    tto=5, psi=0,
    psoil=1.0, rsoil=1.0,
    alpha=40.0,
    prospect_version='D'
)

lai_values = np.arange(0, 8.1, 0.1)
tts_values = [0, 10, 20, 30, 40, 50, 60, 70, 80]

fig, ax = plt.subplots(figsize=(8, 6))

for tts in tts_values:
    ndvi_values = []
    for lai in lai_values:
        s = prosail.run_prosail(lai=lai, tts=tts, **params_base)
        rouge = s[270]   # 670 nm
        nir   = s[400]   # 800 nm
        ndvi  = (nir - rouge) / (nir + rouge)
        ndvi_values.append(ndvi)
    ax.plot(lai_values, ndvi_values, label=f'tts={tts}')

ax.set_xlabel('LAI')
ax.set_ylabel('NDVI')
ax.set_title('Solar zenith angle — reproduction figure document Word')
ax.legend(fontsize=8)
ax.set_xlim(0, 8)
ax.set_ylim(0, 1)
plt.tight_layout()
plt.savefig('comparaison_ivvrm_tts.png', dpi=150)
plt.close()
print("Figure sauvegardée.")