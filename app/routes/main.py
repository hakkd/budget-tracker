import os
import pandas as pd
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename

main_bp = Blueprint("main", __name__)

ALLOWED_EXTENSIONS = {".csv", ".pdf"}


def _is_allowed_filename(filename: str) -> bool:
    if "." not in filename:
        return False
    ext = os.path.splitext(filename)
    return ext in ALLOWED_EXTENSIONS


@main_bp.get("/")
def index():
    return jsonify({"message": "Budget Tracker API is running"})


@main_bp.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@main_bp.post("/upload")
def upload():
    if "file" not in request.files:
        return (
            jsonify(
                {
                    "error": "Missing file field. Use multipart/form-data with key 'file'."
                }
            ),
            400,
        )

    file = request.files["file"]
    if not file or file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    filename = secure_filename(str(file.filename))
    if not _is_allowed_filename(filename):
        return jsonify({"error": "Only .csv and .pdf files are supported."}), 400

    # TODO:
    # - check if statement data is valid
    # - check if data is duplicate
    # - clean data
    # - apply categorization
    # - persist data

    # TODO: placeholder, fill in actual return
    return jsonify({"message": "success"}), 201
