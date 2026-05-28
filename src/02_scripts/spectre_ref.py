import prosail
import numpy as np
import matplotlib.pyplot as plt




# --- Calcul indices ---
def compute_indices(s):
    r = lambda w: s[w - 400]
    ndvi  = (r(800)-r(670)) / (r(800)+r(670))
    savi  = ((r(800)-r(670)) / (r(800)+r(670)+0.5)) * 1.5
    osavi = (r(800)-r(670)) / (r(800)+r(670)+0.16)
    tcari = 3*((r(700)-r(670)) - 0.2*(r(700)-r(550))*(r(700)/r(670)))
    tcari_osavi = tcari / osavi
    rendvi = (r(750)-r(705)) / (r(750)+r(705))
    ndre   = (r(790)-r(720)) / (r(790)+r(720))
    ndii   = (r(819)-r(1649)) / (r(819)+r(1649))
    return {
        'NDVI': ndvi, 'SAVI': savi,
        'TCARI/OSAVI': tcari_osavi,
        'RE-NDVI': rendvi, 'NDRE': ndre,
        'NDII': ndii
    }



if __name__ == '__main__':

    params = dict(
        n=1.5, cab=40, car=10, cbrown=0.25,
        cw=0.03, cm=0.012, ant=2.0,
        lidfa=30, typelidf=2, hspot=0.01,
        tts=30, tto=0, psi=0,
        prospect_version='D'
    )

    s  = prosail.run_prosail(lai=3, psoil=0.8, rsoil=1.0,**params)
    wl = np.arange(400, 2501)



    indices = compute_indices(s)
    print("\nIndices calculés :")
    for name, value in indices.items():
        print(f"{name}: {value:.4f}")   


    # --- Figure ---
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(wl,    s ,  'g-',  linewidth=2, label='Python')
    ax.set_xlabel('Wavelength [nm]')
    ax.set_ylabel('Reflectance')
    ax.set_title('Spctre de reference')
    ax.set_xlim(400, 2500)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('images/02/spectre_ref.png', dpi=150)
    plt.close()
    print("\nFigure sauvegardée.")


