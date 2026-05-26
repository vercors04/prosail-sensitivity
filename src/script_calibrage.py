import prosail
import numpy as np
import matplotlib.pyplot as plt

# Paramètres fixes — exactement ceux de Jacquemoud et al. 2009 Fig.3
params = dict(
    n=1.5, cab=50, car=8, cbrown=0,
    cw=0.01, cm=0.005,
    lidfa=57.3, hspot=0.25,
    tts=20, tto=0, psi=0,
    psoil=0.7,    # sol légèrement sec
    rsoil=0.35    # brillance modérée → sol sombre
)

# LAI de 0 à 10
lai_values = [0, 1, 2, 3, 4, 5, 6, 8, 10]
wavelengths = np.arange(400, 2501, 1)

fig, ax = plt.subplots(figsize=(10, 5))

for lai in lai_values:
    spectre = prosail.run_prosail(lai=lai, **params)
    ax.plot(wavelengths, spectre, label=f'LAI = {lai}')

ax.set_xlabel('Longueur d\'onde (nm)')
ax.set_ylabel('Réflectance')
ax.set_title('Reproduction Fig. 3 — Jacquemoud et al. (2009)')
ax.legend(fontsize=8, ncol=2)
ax.set_xlim(400, 2500)
ax.set_ylim(0, 1)
plt.tight_layout()
plt.savefig('validation_jacquemoud2009_fig3.png', dpi=150)
plt.close()
print("Figure sauvegardée.")