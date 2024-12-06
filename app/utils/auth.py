from bson import ObjectId
import jwt
import datetime
from functools import wraps
from flask import request
from app.utils.helpers import response
from app.models.user_model import UserModel
from flask import current_app

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return response(False, "Token is missing!", status=401)
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = UserModel.find_user_by_id(ObjectId(data["id"]))
            if not current_user:
                return response(False, "Invalid token!", status=401)
        except Exception as e:
            return response(False, str(e), status=401)
        return f(current_user, *args, **kwargs)
    return decorated

def generate_token(data: dict) -> str:
    """
    Generate a JWT token.
    :param data: Dictionary of user data (e.g., user ID)
    :return: Encoded JWT token
    """
    payload = {
        **data,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
    return token