from pathlib import Path

import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

from services.feature_extraction import ekstrak_fitur_gambar


class KNNIkanService:
    def __init__(self, dataset_dir, k=3, test_size=0.2, random_state=42):
        self.dataset_dir = Path(dataset_dir)
        self.k = k
        self.test_size = test_size
        self.random_state = random_state
        self.model = None
        self.metrics = {}
        self._latih_model()

    def _latih_model(self):
        fitur, label = self._muat_dataset()
        if len(fitur) < 2:
            raise ValueError("Dataset tidak cukup untuk melatih model KNN")

        stratify = label if len(set(label)) > 1 else None
        x_train, x_test, y_train, y_test = train_test_split(
            fitur,
            label,
            test_size=self.test_size,
            random_state=self.random_state,
            stratify=stratify,
        )

        jumlah_tetangga = min(self.k, len(x_train))
        self.model = KNeighborsClassifier(n_neighbors=jumlah_tetangga)
        self.model.fit(x_train, y_train)

        y_pred = self.model.predict(x_test)
        labels = ["Segar", "Tidak Segar"]
        self.metrics = {
            "total_dataset": int(len(fitur)),
            "total_train": int(len(x_train)),
            "total_test": int(len(x_test)),
            "jumlah_segar": int(np.sum(label == "Segar")),
            "jumlah_tidak_segar": int(np.sum(label == "Tidak Segar")),
            "akurasi": float(accuracy_score(y_test, y_pred)),
            "k": int(jumlah_tetangga),
            "confusion_matrix": confusion_matrix(y_test, y_pred, labels=labels).tolist(),
        }

    def _muat_dataset(self):
        fitur = []
        label = []
        ekstensi = {".jpg", ".jpeg", ".png"}

        for nama_label in ["Segar", "Tidak Segar"]:
            folder = self.dataset_dir / nama_label
            if not folder.exists():
                continue

            for path_gambar in folder.iterdir():
                if path_gambar.suffix.lower() not in ekstensi:
                    continue
                try:
                    fitur.append(ekstrak_fitur_gambar(path_gambar))
                    label.append(nama_label)
                except ValueError:
                    continue

        return np.array(fitur), np.array(label)

    def prediksi(self, fitur):
        if self.model is None:
            raise ValueError("Model belum tersedia")
        return self.model.predict([fitur])[0]
