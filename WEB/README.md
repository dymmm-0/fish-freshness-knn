# Klasifikasi Tingkat Kesegaran Ikan Kembung Berdasarkan Citra Mata Menggunakan Metode K-Nearest Neighbor

Aplikasi web untuk mengklasifikasikan tingkat kesegaran ikan kembung ("Segar" /
"Tidak Segar") berdasarkan citra mata ikan, menggunakan metode
**K-Nearest Neighbor (KNN)**.

## Teknologi

**Backend:** Python, Flask, SQLAlchemy, SQLite, OpenCV, Scikit-Learn
**Frontend:** HTML, CSS, JavaScript, Bootstrap 5, Chart.js, SweetAlert2

## Fitur

- Dashboard
- Upload gambar
- Kamera real-time
- Riwayat prediksi
- Detail prediksi
- Tentang aplikasi

## Struktur Proyek

Lihat `docs/architecture.md`.

## Menjalankan (akan diisi setelah implementasi)

```bash
pip install -r requirements.txt
cp .env.example .env
python scripts/init_db.py
python app.py
```
