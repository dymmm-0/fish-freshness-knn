"""
Ekstraksi fitur WARNA dari gambar ikan untuk klasifikasi kesegaran.

Versi Python dari grey.m, tapi mengekstrak fitur warna (RGB + HSV)
bukan grayscale. Hasil disimpan ke satu file Excel agar bisa dihitung
manual di Excel. Gambar hasil konversi TIDAK disimpan.
"""

from pathlib import Path

import cv2
import numpy as np
import pandas as pd

# =========================
# LOKASI FOLDER DATASET
# (relatif terhadap lokasi file ini, biar tidak nyangkut ke root drive)
# =========================
BASE = Path(__file__).resolve().parent
folderSegar = BASE / "DATA" / "Segar"
folderTidakSegar = BASE / "DATA" / "Tidak Segar"

# File Excel hasil ekstraksi fitur (disimpan di DATA/ proyek ini)
outputFile = BASE / "OUTPUT DATA" / "fitur_warna_ikan.xlsx"

# Ekstensi gambar yang diproses
EKSTENSI = ("*.jpg", "*.jpeg", "*.png")


def ambilFile(folder: Path):
    """Kumpulkan semua file gambar (jpg/jpeg/png) dalam satu folder."""
    files = []
    for pola in EKSTENSI:
        files.extend(sorted(folder.glob(pola)))
    return files


def prosesFolder(fileList, label):
    """Ekstrak fitur warna untuk semua gambar dalam satu kelas."""
    data = []
    n = len(fileList)
    print(f'Memproses kelas "{label}" ({n} gambar)...')

    for i, path in enumerate(fileList, start=1):
        try:
            # cv2 membaca dalam urutan BGR
            img = cv2.imread(str(path))
            if img is None:
                raise ValueError("file tidak terbaca (None)")

            # Pisahkan channel RGB
            b, g, r = cv2.split(img)

            # Konversi ke HSV (OpenCV: H 0-179, S 0-255, V 0-255)
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)

            baris = {"Nama_File": path.name}
            for nama, kanal in (
                ("R", r), ("G", g), ("B", b),
                ("H", h), ("S", s), ("V", v),
            ):
                arr = kanal.astype(np.float64).ravel()
                baris[f"Mean_{nama}"] = arr.mean()
                baris[f"Std_{nama}"] = arr.std(ddof=1)
                baris[f"Min_{nama}"] = arr.min()
                baris[f"Max_{nama}"] = arr.max()

            baris["Kelas"] = label
            data.append(baris)

        except Exception as e:
            # Kalau ada 1 gambar rusak, lewati saja, proses tetap jalan
            print(f"  [LEWAT] {path.name} -> {e}")

        # Tampilkan progres tiap 25 gambar
        if i % 25 == 0 or i == n:
            print(f"  {i} / {n} selesai")

    return data


def main():
    fileSegar = ambilFile(folderSegar)
    fileTidakSegar = ambilFile(folderTidakSegar)

    dataSegar = prosesFolder(fileSegar, "Segar")
    dataTidakSegar = prosesFolder(fileTidakSegar, "Tidak Segar")

    # Gabungkan hasil kedua kelas
    data = dataSegar + dataTidakSegar

    # Susun urutan kolom: Nama_File, fitur per channel, lalu Kelas
    kolom = ["Nama_File"]
    for nama in ("R", "G", "B", "H", "S", "V"):
        kolom += [f"Mean_{nama}", f"Std_{nama}", f"Min_{nama}", f"Max_{nama}"]
    kolom += ["Kelas"]

    T = pd.DataFrame(data, columns=kolom)

    # Sheet khusus: hanya Mean tiap channel (RGB + HSV)
    kolomMean = ["Nama_File", "Mean_R", "Mean_G", "Mean_B",
                 "Mean_H", "Mean_S", "Mean_V", "Kelas"]
    T_mean = T[kolomMean]

    outputFile.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(outputFile, engine="openpyxl") as writer:
        T.to_excel(writer, sheet_name="Semua_Fitur", index=False)
        T_mean.to_excel(writer, sheet_name="Mean", index=False)

    # =========================
    # INFO RINGKASAN
    # =========================
    print("=================================================")
    print("Proses selesai.")
    print(f"Jumlah file segar ditemukan      : {len(fileSegar)}")
    print(f"Jumlah file tidak segar ditemukan: {len(fileTidakSegar)}")
    print(f"Total data berhasil diproses     : {len(T)}")
    print(f"File Excel disimpan di           : {outputFile}")
    print("=================================================")


if __name__ == "__main__":
    main()
