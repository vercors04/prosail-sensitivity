import prosail
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from spectre_ref import compute_indices
import matplotlib.cm as cm

params = dict(
    n=1.5, cab=40, car=10, cbrown=0.25,
    cw=0.03, cm=0.012, ant=2.0,
    lidfa=30, typelidf=2, hspot=0.01,
    tts=30, tto=0, psi=0,
    prospect_version='D'
)

lai_values   = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6]
psoil_values = np.linspace(0, 1, 8)
wl_values    = [550, 670, 705, 720, 750, 790, 800, 819, 1649]
resultats = {wl: {lai: [] for lai in lai_values} for wl in wl_values}
couleurs = [cm.plasma(i / (len(lai_values)-1)) for i in range(len(lai_values))]


for lai in lai_values:
    for psoil in psoil_values:
        s = prosail.run_prosail(lai=lai, psoil=psoil, rsoil=1.0, **params)
        for val in wl_values:
            resultats[val][lai].append(s[val - 400])


#-----affichage tableau-----
for val in wl_values:
    print(f"\n=== {val} ===")
    for lai in lai_values:
        valeurs = [f"{v:.4f}" for v in resultats[val][lai]]
        print(f"  LAI={lai}: {valeurs}")


print()
print()



#-----affichage graph courbes-----

fig, ax = plt.subplots(figsize=(8, 5))
for lai, couleur in zip(lai_values, couleurs):
        lw = 1.5
        ls = '-' 
        ax.plot(psoil_values, resultats[670][lai],
                color=couleur, linewidth=lw,
                linestyle=ls, label=f'LAI = {lai}')
ax.set_xlabel('psoil')
ax.set_ylabel('670 nm (rouge)')
ax.set_title(f'{670}nm — effet de psoil (rsoil=1.0)')
ax.legend(fontsize=8, loc='best')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'images/02/effet_psoil_{670}.png', dpi=150)
plt.close()
print(f"Figure {670}nm sauvegardée.")


fig, ax = plt.subplots(figsize=(8, 5))
for lai, couleur in zip(lai_values, couleurs):
        lw = 1.5
        ls = '-' 
        ax.plot(psoil_values, resultats[1649][lai],
                color=couleur, linewidth=lw,
                linestyle=ls, label=f'LAI = {lai}')
ax.set_xlabel('psoil')
ax.set_ylabel('1649 nm (infrarouge)')
ax.set_title(f'{1649}nm — effet de psoil (rsoil=1.0)')
ax.legend(fontsize=8, loc='best')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'images/02/effet_psoil_{1649}.png', dpi=150)
plt.close()
print(f"Figure {1649}nm sauvegardée.")


fig, ax = plt.subplots(figsize=(8, 5))
for lai, couleur in zip(lai_values, couleurs):
        lw = 1.5
        ls = '-' 
        ax.plot(psoil_values, resultats[819][lai],
                color=couleur, linewidth=lw,
                linestyle=ls, label=f'LAI = {lai}')
ax.set_xlabel('psoil')
ax.set_ylabel('819 nm (infrarouge)')
ax.set_title(f'{819}nm — effet de psoil (rsoil=1.0)')
ax.legend(fontsize=8, loc='best')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'images/02/effet_psoil_{819}.png', dpi=150)
plt.close()
print(f"Figure {819}nm sauvegardée.")






# ----- atténuation de l'effet sol par bande -----
print("\n=== Écart max-min (Δ) par bande et par LAI ===")
header = f"{'LAI':<6}" + "".join(f"{wl:>8}" for wl in wl_values)
print(header)
for lai in lai_values:
    ligne = f"{lai:<6}"
    for wl in wl_values:
        delta = max(resultats[wl][lai]) - min(resultats[wl][lai])
        ligne += f"{delta:>8.4f}"
    print(ligne)

# ----- heatmap atténuation -----
delta_matrix = np.array([
    [max(resultats[wl][lai]) - min(resultats[wl][lai])
     for wl in wl_values]
    for lai in lai_values
])

fig, ax = plt.subplots(figsize=(10, 6))
im = ax.imshow(delta_matrix, aspect='auto', cmap='RdYlGn_r',
               vmin=0, vmax=0.35)
plt.colorbar(im, ax=ax, label='Δ réflectance (max - min sur psoil)')
ax.set_xticks(range(len(wl_values)))
ax.set_xticklabels([f'{wl} nm' for wl in wl_values], rotation=45)
ax.set_yticks(range(len(lai_values)))
ax.set_yticklabels([f'LAI={lai}' for lai in lai_values])
ax.set_title('Sensibilité au sol par bande et par LAI\n'
             '(rouge = fort effet, vert = faible effet)')
plt.tight_layout()
plt.savefig('images/02/heatmap_attenuation.png', dpi=150)
plt.close()
print("Heatmap atténuation sauvegardée.")