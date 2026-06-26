import cv2
import numpy as np


FEATURE_NAMES = ["mean_r", "mean_g", "mean_b", "mean_h", "mean_s", "mean_v"]


def ekstrak_fitur_gambar(path_gambar):
    gambar = cv2.imread(str(path_gambar))
    if gambar is None:
        raise ValueError("Gambar tidak dapat dibaca")

    b, g, r = cv2.split(gambar)
    hsv = cv2.cvtColor(gambar, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    fitur = np.array([
        float(np.mean(r)),
        float(np.mean(g)),
        float(np.mean(b)),
        float(np.mean(h)),
        float(np.mean(s)),
        float(np.mean(v)),
    ])

    return fitur


def fitur_ke_dict(fitur):
    return {nama: float(nilai) for nama, nilai in zip(FEATURE_NAMES, fitur)}
