from functools import wraps
from flask import request, jsonify
from config import SECRET_KEY
import jwt 

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(payload, *args, **kwargs)

    return decorated
        
'''We extracted JWT logic

We verify token

If valid → we pass decoded payload to route

If invalid → stop request

'''