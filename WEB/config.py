from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = "dev-secret-key"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'database' / 'app.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATASET_DIR = BASE_DIR / "dataset"
    UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    KNN_NEIGHBORS = 3
    TEST_SIZE = 0.2
    RANDOM_STATE = 42
