import librosa
import numpy as np
from scipy.ndimage import maximum_filter
from .config import *

def get_constellation_map(path, limit_duration=None):
    y, sr = librosa.load(path, sr=SR, mono=True, duration=limit_duration)

    S = np.abs(librosa.stft(y, n_fft=N_FFT, hop_length=HOP))
    S_db = librosa.amplitude_to_db(S, ref=np.max)

    threshold = np.median(S_db) + MIN_AMPLITUDE
    local_max = maximum_filter(S_db, size=PEAK_NEIGHBORHOOD) == S_db

    peaks = np.argwhere(local_max & (S_db > threshold))

    constellation = []
    for freq, time in peaks:
        constellation.append((int(time), int(freq)))

    constellation.sort(key=lambda x: x[0])
    return constellation
