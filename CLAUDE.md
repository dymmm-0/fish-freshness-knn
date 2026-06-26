# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Tugas Akhir (final project) for a Digital Image Processing course. The goal is
fish-freshness classification ("Segar" vs "Tidak Segar") from fish-eye photos,
using color-feature extraction and a Flask web app with K-Nearest Neighbor (KNN).
Code and comments are written in Indonesian — match that language when editing.

## Commands

Color-feature scripts use OpenCV, NumPy, pandas, and `openpyxl`:

```bash
pip install opencv-python numpy pandas openpyxl
python "RGB to HSV/konversi-warna.py"     # extract RGB+HSV feature workbook
python "Hanya Contoh/matriks_rgb.py"      # export raw RGB matrices of one sample image
```

The Flask app lives under `WEB/` and has its own dependency list:

```bash
cd WEB
pip install -r requirements.txt
cp .env.example .env
python app.py
```

The app runs on `127.0.0.1:8000` in debug mode when started directly. There are
currently no tests, build, or lint steps. `WEB/README.md` mentions
`python scripts/init_db.py`, but there is no `scripts/` directory; database
tables are currently created by `db.create_all()` inside `create_app()`.

## Architecture

There are two standalone data-preparation scripts plus a Flask/KNN web app. The
standalone scripts do not import the web app.

- **`RGB to HSV/konversi-warna.py`** — batch feature extraction pipeline. Walks
  two class folders, reads each image with `cv2.imread` (BGR order — channels
  are split as `b, g, r`), converts to HSV (`cv2.COLOR_BGR2HSV`, so H is 0–179
  and S/V are 0–255), and computes Mean/Std/Min/Max per channel (R,G,B,H,S,V).
  Output is one workbook with `Semua_Fitur` (all stats) and `Mean` (means only).
  Converted images are intentionally not saved. Corrupt/unreadable images are
  skipped with a `[LEWAT]` log line so the run continues.

- **`Hanya Contoh/matriks_rgb.py`** — one-off helper that dumps the full
  per-pixel R, G, B matrices of a single hard-coded sample image (`gambarContoh`)
  to one Excel sheet per channel, for inspecting raw pixel values by hand.

- **`WEB/app.py`** — Flask app factory and route definitions. On startup it
  creates the upload/database directories, initializes SQLAlchemy, creates DB
  tables, and trains `KNNIkanService` from `WEB/dataset/`. Routes currently cover
  dashboard (`/`), prediction upload (`/prediksi`), history (`/riwayat`), and
  deleting a history item (`/riwayat/<id>/hapus`). Uploaded files are saved under
  `WEB/static/uploads/` with a UUID prefix and `secure_filename`.

- **`WEB/services/feature_extraction.py`** — shared image feature extraction for
  the web app. It returns only six mean features: `mean_r`, `mean_g`, `mean_b`,
  `mean_h`, `mean_s`, `mean_v`. Keep this feature order aligned with the KNN
  training and prediction flow.

- **`WEB/services/knn_service.py`** — loads images from `WEB/dataset/Segar/` and
  `WEB/dataset/Tidak Segar/`, extracts features, trains a `KNeighborsClassifier`,
  and stores simple metrics (`total_dataset`, train/test counts, class counts,
  accuracy, k, confusion matrix). Unreadable images are skipped.

- **`WEB/database/`** — SQLAlchemy setup and `PredictionHistory` model. The model
  stores uploaded filename, predicted label, the six mean features, and creation
  timestamp.

The README says the planned frontend includes dashboard, upload, real-time camera,
history/detail, and about pages. Current repository state has no `WEB/templates/`,
`WEB/static/`, or `WEB/docs/architecture.md`, so `python app.py` can train the
model but routes that render templates will fail until templates are added.

## Important: path resolution gotcha

Both standalone scripts compute `BASE = Path(__file__).resolve().parent` (the
script's own subfolder) and then build dataset paths as `BASE / "DATA" / ...`.
No `DATA/` folder exists for those scripts — the real dataset is in
`WEB/dataset/`. As written, the main extraction script will find `0` files and
produce an empty/near-empty Excel.

Before running the standalone scripts, repoint their path constants at the real
data, e.g. in `konversi-warna.py`:

```python
folderSegar = BASE.parent / "WEB" / "dataset" / "Segar"
folderTidakSegar = BASE.parent / "WEB" / "dataset" / "Tidak Segar"
```

`matriks_rgb.py` has the same issue for both its input image (`BASE / "DATA" /
"Segar" / ...`) and its output (`BASE / "DATA" / ...`).

## Data layout

- `WEB/dataset/Segar/` and `WEB/dataset/Tidak Segar/` — JPEG photos named
  `IMG_<date>_<time>.jpg`. This is the input dataset; treat it as read-only.
- `OUTPUT DATA/fitur_warna_ikan.xlsx` — generated color-feature workbook.
  Regenerable; do not hand-edit.
- `Hanya Contoh/matriks_rgb_contoh.xlsx` — generated raw-RGB-matrix dump for one
  sample image. Regenerable.
- `WEB/.env.example` — placeholder Flask environment config. `WEB/config.py`
  currently loads `.env` but still defines config values directly in `Config`.
