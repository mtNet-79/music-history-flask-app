from functools import wraps
from flask import request, jsonify
import jwt
import os

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
        print(f'auth error is {error} and code is {status_code} ')

def jwt_required(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            token = None
            auth_header = request.headers.get("Authorization")
            
            if not auth_header:
                raise AuthError({
                    'code': 'authorization_header_missing',
                    'description': 'Authorization header is expected.'
                }, 401)

            else:
                token_parts = auth_header.split(" ")
                if len(token_parts) == 2 and token_parts[0].lower() == "bearer":
                    token = token_parts[1]

            if token is None:
                return jsonify({"message": "Missing JWT token"}), 401

            try:
                payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
                request.user_id = payload["sub"]
                request.user_role = payload["role"]
            except jwt.ExpiredSignatureError:
                return jsonify({"message": "Expired JWT token"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"message": "Invalid JWT token"}), 401

            if allowed_roles and request.user_role not in allowed_roles:
                return jsonify({"message": "Insufficient permissions"}), 403

            return func(*args, **kwargs)

        return decorated

    return decorator
