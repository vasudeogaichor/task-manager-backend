from flask import jsonify
from typing import Dict

def response(success: bool, message: str, data: Dict = None, status: int = 200):
    return jsonify({"success": success, "message": message, "data": data}), status
