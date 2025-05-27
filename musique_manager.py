import numpy as np
from scipy.io import wavfile


L = 0.86 # m

Serie_de_fourier = {
    "An": [0.3445,0.3002,0.1828,0.06727,0.02257,0.01121,0.003853,-0.002458,-0.005149,-0.0001374,0.004923,0.004188,-0.0009613,-0.001318,0.0003633,-0.003587,-0.006679,-0.005342,-0.00292,-0.0008341,-0.001045,-0.0007168,-0.00447,-0.005222,-0.001972,-0.002355,-0.001342,-0.0008305,-0.0007031,0.001344],
    "Bn": [0.1961,0.1624,-0.005437,-0.06523,-0.02156,-0.01248,-0.01401,-0.001862,-0.00198,0.0007264,0.01687,0.009814,-0.01885,-0.002389,0.02611,0.01029,-0.00819,-0.005058,0.001749,0.004648,0.0002205,-0.0009073,0.003996,0.001952,0.0007429,0.002554,-0.000118,-0.001987,-0.002959,-0.0009415]
}




def deplacement_frot(L: int, frequence: int, x: int, duree: int, fs: int, N_max: int=5) -> tuple[np.ndarray, np.ndarray]:
    """Modélise le mouvement d'une corde frottée (modélisation vue en TP Musique)

    Args:
        L (int): La longueur de la corde (en m)
        frequence (int): La fréquence de la vibration (en Hz)
        x (int): La position sur la corde (en m)
        duree (int): La durée de la vibration (en s)
        fs (int): La fréquence d'échantillonage (en Hz)
        N_max (int, optional): Le nombre d'harmonique à prendre en compte. Defaults to 5.

    Returns:
        tuple[np.ndarray, np.ndarray]: _description_
    """
    t_range = np.linspace(0, duree, int(duree*fs))
    u_range = t_range * 0
    epsilon = 0.5e-3
    

    for n in range(1, N_max+1):
        fn = n * frequence
        for i, t in enumerate(t_range):
            s = 1
            s *= np.exp(-1 * (epsilon * fn * 2 * np.pi * t))
            s *= np.sin(fn * np.pi * x / L)
            s *= (Serie_de_fourier['An'][n] * np.cos(2 * np.pi * fn * t) + Serie_de_fourier['Bn'][n] * np.sin(2 * np.pi * fn * t))

            u_range[i] += s
    
    return u_range, t_range


def note(f: int, duree: int, amplitude: int, fe: int) -> np.ndarray:
    """Génère le signal d'une note de guitare pour une certaine fréquence.

    Args:
        f (int): Fréquence du signal à synthétiser (en Hz)
        duree (int): La durée du signal souhaité (en secondes)
        amplitude (int): L'amplitude du signal
        fe (int): La fréquence d'échantillonage (en Hz)

    Returns:
        np.ndarray: Le signal correspondant à la note générée
    """
    return amplitude * deplacement_frot(L, f, L/2, duree, fe, N_max=7)[0]


def accord(signals: list[np.ndarray]) -> np.ndarray:
    """Superpose les signaux pour les transformer en un accord unique.

    Args:
        signals (list[np.ndarray]): La liste des signaux à superposer

    Returns:
        np.ndarray: Le signal correspondant à l'accord.
    """
    return sum(signals)

def writewavfile(filename, sig, fe):
    """Writes an audio signal (mono) to a wav file

    Parameters
    ----------
    filename : string
        name of the file to be written
    sig : numpy array
        a signal
    fe : float
        sampling frequency
          
   """    
    sig = np.float32(sig)
    sig = sig / np.absolute(sig).max()
    
    wavfile.write(filename, fe, sig)
    

