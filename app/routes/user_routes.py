from flask import Blueprint, jsonify

user_bp = Blueprint("users", __name__)


@user_bp.route("/users")
def get_users():
    return {"message": "list of users"}
