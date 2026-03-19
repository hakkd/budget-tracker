from flask import Blueprint, jsonify

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index():
    return jsonify({"message": "Budget Tracker API is running"})


@main_bp.get("/health")
def health():
    return jsonify({"status": "ok"}), 200
