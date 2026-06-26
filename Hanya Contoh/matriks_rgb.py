"""
Ekspor matriks RGB asli dari SATU gambar contoh ke Excel.

Tiap channel (R, G, B) ditulis ke sheet sendiri sebagai matriks penuh
sesuai ukuran asli gambar (tinggi x lebar). Berguna untuk melihat nilai
piksel mentah dan menghitung manual di Excel.
"""

from pathlib import Path

import cv2
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent

# Gambar contoh yang mau diekspor matriksnya.
# Ganti ke path gambar lain kalau perlu.
gambarContoh = BASE / "DATA" / "Segar" / "IMG_20191016_063900.jpg"

# File Excel hasil
outputFile = BASE / "DATA" / "matriks_rgb_contoh.xlsx"


def main():
    img = cv2.imread(str(gambarContoh))
    if img is None:
        raise SystemExit(f"Gambar tidak terbaca: {gambarContoh}")

    # cv2 membaca dalam urutan BGR -> pisahkan
    b, g, r = cv2.split(img)
    tinggi, lebar = r.shape
    print(f"Gambar : {gambarContoh.name}")
    print(f"Ukuran : {tinggi} x {lebar} (tinggi x lebar)")

    # Label baris/kolom mengikuti koordinat piksel (mulai dari 0)
    indexBaris = [f"baris_{i}" for i in range(tinggi)]
    kolom = [f"kolom_{j}" for j in range(lebar)]

    outputFile.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(outputFile, engine="openpyxl") as writer:
        for nama, kanal in (("R", r), ("G", g), ("B", b)):
            df = pd.DataFrame(kanal.astype(np.int64),
                              index=indexBaris, columns=kolom)
            df.to_excel(writer, sheet_name=nama)

    print("=================================================")
    print("Selesai.")
    print(f"Sheet  : R, G, B (matriks penuh {tinggi} x {lebar})")
    print(f"Disimpan di: {outputFile}")
    print("=================================================")


if __name__ == "__main__":
    main()
