import prosail
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from spectre_ref import compute_indices

params = dict(
    n=1.5, cab=40, car=10, cbrown=0.25,
    cw=0.03, cm=0.012, ant=2.0,
    lidfa=30, typelidf=2, hspot=0.01,
    tts=30, tto=0, psi=0,
    prospect_version='D'
)


lai_values   = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6]
psoil_values = np.linspace(0, 1, 8)
indices_names = ['NDVI', 'SAVI', 'TCARI/OSAVI', 'RE-NDVI', 'NDRE', 'NDII']
couleurs = [cm.viridis(i / (len(lai_values)-1)) for i in range(len(lai_values))] #paletted e couleur viridis, qui varie avec autant valeurs de LAI
resultats = {idx: {lai: [] for lai in lai_values} for idx in indices_names} #dic de dic : pour chaques indices toutes les val de LAI et da,s ces vals de LAI la variation en fonction de psoil


for lai in lai_values:
    for psoil in psoil_values:
        s = prosail.run_prosail(lai=lai, psoil=psoil, rsoil=1.0, **params)
        idx = compute_indices(s)
        for nom in indices_names:
            resultats[nom][lai].append(idx[nom])




#-----affichage tableau-----
for nom in indices_names:
    print(f"\n=== {nom} ===")
    for lai in lai_values:
        valeurs = [f"{v:.4f}" for v in resultats[nom][lai]]
        print(f"  LAI={lai}: {valeurs}")


print()
print()


#-----calcul des differences-----
seuils = {}
for nom in indices_names:   
    val = [v for lai in lai_values for v in resultats[nom][lai]]
    plage = max(val) - min(val)
    seuil_relatif = 0.02 * plage  # 2% de la plage totale
    seuil_absolu = 0.01
    seuilf = min(seuil_relatif, seuil_absolu)

    for lai in lai_values:
        if max(resultats[nom][lai]) - min(resultats[nom][lai]) < seuilf:
            seuils[nom] = lai
            break
        else:
            seuils[nom] = None

for nom, seuil in seuils.items():
    print(f"{nom} : variation < {seuilf:.4f} pour LAI >= {seuil}")

print()
print()


for lai in [0, 0.5, 1, 2, 3]:
    print(f"\nLAI={lai}")
    for psoil in np.linspace(0, 1, 5):
        s = prosail.run_prosail(lai=lai, psoil=psoil, rsoil=1.0, **params)
        print(f"  psoil={psoil:.2f} : R(819)={s[419]:.4f}  R(1649)={s[1249]:.4f}  NDII={( s[419]-s[1249])/(s[419]+s[1249]):.4f}")
#-----affichage figures-----
for nom in indices_names:
    fig, ax = plt.subplots(figsize=(8, 5))
    for lai, couleur in zip(lai_values, couleurs):
        lw = 2.5 if lai == seuils[nom] else 1.5
        ls = '--' if lai == seuils[nom] else '-'
        ax.plot(psoil_values, resultats[nom][lai],
                color=couleur, linewidth=lw,
                linestyle=ls, label=f'LAI = {lai}')
    ax.set_xlabel('psoil')
    ax.set_ylabel(nom)
    ax.set_title(f'{nom} — effet de psoil (rsoil=1.0)')
    ax.legend(fontsize=8, loc='best')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'images/02/effet_psoil_{nom.replace("/","_")}.png', dpi=150)
    plt.close()
    print(f"Figure {nom} sauvegardée.")







