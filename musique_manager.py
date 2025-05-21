import numpy as np
from scipy.io import wavfile


L = 0.86 # m
mu = 13.9e-3 # ?
T = 500 # N
duree = 0.1 # s

fs = 11025 # Hz


EI = 210e9 * np.pi * (1e-3)**4 / 64




json = {
  "An": [
    0.3445,
    0.3002,
    0.1828,
    0.06727,
    0.02257,
    0.01121,
    0.003853,
    -0.002458,
    -0.005149,
    -0.0001374,
    0.004923,
    0.004188,
    -0.0009613,
    -0.001318,
    0.0003633,
    -0.003587,
    -0.006679,
    -0.005342,
    -0.00292,
    -0.0008341,
    -0.001045,
    -0.0007168,
    -0.00447,
    -0.005222,
    -0.001972,
    -0.002355,
    -0.001342,
    -0.0008305,
    -0.0007031,
    0.001344
  ],
  "Bn": [
    0.1961,
    0.1624,
    -0.005437,
    -0.06523,
    -0.02156,
    -0.01248,
    -0.01401,
    -0.001862,
    -0.00198,
    0.0007264,
    0.01687,
    0.009814,
    -0.01885,
    -0.002389,
    0.02611,
    0.01029,
    -0.00819,
    -0.005058,
    0.001749,
    0.004648,
    0.0002205,
    -0.0009073,
    0.003996,
    0.001952,
    0.0007429,
    0.002554,
    -0.000118,
    -0.001987,
    -0.002959,
    -0.0009415
  ]
}







def frequence_n(n, L, EI, T, mu):
    V = np.sqrt(T/mu)
    
    s = n / (2 * L)
    s *= V
    s *= np.sqrt(1+(EI/T) * (n * np.pi / L)**2)
    return s



def deplacement(mu, L, T, x, duree, fs):
    t_range = np.linspace(0, duree, int(duree*fs))
    u_range = t_range * 0
    
    V = np.sqrt(T/mu)
    omega_0 = np.pi * V / L
    
    U_max = 2
    
    epsilon = 1e-3
    
    infini = 20
    
    for p in range(infini):
        for i, t in enumerate(t_range):
            s = 8 * U_max * (-1)**p / (np.pi**2 * (2 * p + 1)**2)
            s *= np.cos((2*p + 1) * omega_0 * t)
            s *= np.sin((2*p + 1) * np.pi * x / L)
            s *= np.exp(-1 * (epsilon * frequence_n(p, L, EI, T, mu) * 2 * np.pi * t))
            u_range[i] += s
    
    

    return u_range, t_range

def deplacement_frot(mu, L, T, frequence, x, duree, fs, N_max=5):
    t_range = np.linspace(0, duree, int(duree*fs))
    u_range = t_range * 0
    
    V = np.sqrt(T/mu)
    omega_0 = np.pi * V / L
    
    U_max = 1
    
    epsilon = 0.5e-3
    

    for n in range(1, N_max+1):
        fn = n * frequence
        for i, t in enumerate(t_range):
            s = 1
            s *= np.exp(-1 * (epsilon * fn * 2 * np.pi * t))
            s *= np.sin(n * frequence * np.pi * x / L)
            s *= (json['An'][n] * np.cos(2 * np.pi * fn * t) + json['Bn'][n] * np.sin(2 * np.pi * fn * t))


            u_range[i] += s
    
    return u_range, t_range



def note(f, duree, amplitude, fe):
    return amplitude * deplacement_frot(mu, L, T, f, L/2, duree, fe, N_max=20)[0]



def mix(x):
    return np.concatenate(list(e for e in x))

def accord(x):
    return sum(x)

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
    

