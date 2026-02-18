from flask import Flask, request, jsonify, Blueprint
import jwt
import datetime
from config import SECRET_KEY
from db import add_user, get_user
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    hashed_password = generate_password_hash(password)
    
    if add_user(username, hashed_password):
        return jsonify({'message': 'User registered successfully'}), 201
    else:
        return jsonify({'message': 'Username already exists'}), 409

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    user = get_user(username)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    if not check_password_hash(user['hashed_password'], password):
        return jsonify({'message': 'Invalid password'}), 401
    
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    
    return jsonify({'message': 'User logged in successfully', 'token': token}), 200

@auth_bp.route('/dashboard', methods=['GET'])
def dashboard():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'message': 'Missing token'}), 401
    
    try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload['username']
        return jsonify({'message': 'access granted', 'username': username}), 200
    
    except (IndexError, jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        if isinstance(e, IndexError):
            return jsonify({'message': 'Malformed token'}), 401
        elif isinstance(e, jwt.ExpiredSignatureError):
            return jsonify({'message': 'Token expired'}), 401
        else:
            return jsonify({'message': 'Invalid token'}), 401
