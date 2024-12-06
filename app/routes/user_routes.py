from flask import Blueprint, request
from app.utils.auth import generate_token
from bson.objectid import ObjectId
from app.utils.helpers import response
from app.utils.auth import token_required
from werkzeug.security import generate_password_hash
from app.models.user_model import UserModel

user_bp = Blueprint('user', __name__)

@user_bp.route("/register", methods=["POST"])
def register_user():
    data = request.json
    if not data or not all(k in data for k in ("username", "email", "password")):
        return response(False, "Missing fields!", status=400)
    print('data - ', data)
    user_id = UserModel.create_user(data)
    token = generate_token({"id": str(user_id)})
    return response(True, "User registered successfully!", {"user_id": str(user_id), "token": token})

@user_bp.route("/edit", methods=["PUT"])
@token_required
def edit_user(current_user):
    data = request.json
    if not data:
        return response(False, "No data provided!", status=400)

    update_fields = {k: v for k, v in data.items() if k in ("username", "email", "password")}
    if "password" in update_fields:
        update_fields["password"] = generate_password_hash(update_fields["password"], method='pbkdf2:sha256')

    result = UserModel.update_user(current_user["_id"], update_fields)

    if result.matched_count == 0:
        return response(False, "User not found or no updates made!", status=404)

    return response(True, "User updated successfully!")

@user_bp.route("/login", methods=["POST"])
def login_user():
    data = request.json
    if not data or not all(k in data for k in ("email", "password")):
        return response(False, "Missing fields!", status=400)

    user = UserModel.find_user_by_email(data["email"])
    if user and UserModel.check_password(user, data["password"]):
        token = generate_token({"id": str(user["_id"])})
        return response(True, "Login successful!", {"token": token})
    return response(False, "Invalid email or password!", status=401)
