from pathlib import Path
from uuid import uuid4

from flask import Flask, current_app, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from config import Config
from database import db
from database.models import PredictionHistory
from services.feature_extraction import ekstrak_fitur_gambar, fitur_ke_dict
from services.knn_service import KNNIkanService


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
    Path(app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")).parent.mkdir(parents=True, exist_ok=True)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        app.knn_service = KNNIkanService(
            dataset_dir=app.config["DATASET_DIR"],
            k=app.config["KNN_NEIGHBORS"],
            test_size=app.config["TEST_SIZE"],
            random_state=app.config["RANDOM_STATE"],
        )

    @app.route("/")
    def dashboard():
        return render_template("dashboard.html", metrics=current_app.knn_service.metrics)

    @app.route("/prediksi", methods=["GET", "POST"])
    def prediksi():
        hasil = None
        gambar_url = None
        fitur = None

        if request.method == "POST":
            file = request.files.get("gambar")
            if not file or file.filename == "":
                return render_template("prediksi.html", error="Pilih gambar terlebih dahulu")

            if not _ekstensi_diizinkan(file.filename):
                return render_template("prediksi.html", error="Format gambar harus PNG, JPG, atau JPEG")

            nama_file = f"{uuid4().hex}_{secure_filename(file.filename)}"
            path_simpan = Path(current_app.config["UPLOAD_FOLDER"]) / nama_file
            file.save(path_simpan)

            fitur_array = ekstrak_fitur_gambar(path_simpan)
            fitur = fitur_ke_dict(fitur_array)
            hasil = current_app.knn_service.prediksi(fitur_array)
            gambar_url = url_for("static", filename=f"uploads/{nama_file}")

            riwayat = PredictionHistory(
                filename=nama_file,
                predicted_label=hasil,
                **fitur,
            )
            db.session.add(riwayat)
            db.session.commit()

        return render_template("prediksi.html", hasil=hasil, gambar_url=gambar_url, fitur=fitur)

    @app.route("/riwayat")
    def riwayat():
        data = PredictionHistory.query.order_by(PredictionHistory.created_at.desc()).all()
        return render_template("riwayat.html", data=data)

    @app.post("/riwayat/<int:id_riwayat>/hapus")
    def hapus_riwayat(id_riwayat):
        data = PredictionHistory.query.get_or_404(id_riwayat)
        path_gambar = Path(current_app.config["UPLOAD_FOLDER"]) / data.filename
        if path_gambar.exists():
            path_gambar.unlink()
        db.session.delete(data)
        db.session.commit()
        return redirect(url_for("riwayat"))

    return app


def _ekstensi_diizinkan(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
