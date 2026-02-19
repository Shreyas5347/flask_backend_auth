from flask import Flask, request, jsonify, Blueprint
import jwt
import datetime
from utils import token_required
from config import SECRET_KEY
from db import add_user, get_user
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password. Ensure you are sending JSON with Content-Type: application/json'}), 400
    
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
    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400
    
    users = get_user(username)
    
    if not users:
        return jsonify({'message': 'User not found'}), 404
    
    if not check_password_hash(users['hashed_password'], password):
        return jsonify({'message': 'Invalid password'}), 401
    
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
   

    return jsonify({'message': 'User logged in successfully', 'token': token}), 200

@auth_bp.route('/dashboard', methods=['GET'])
@token_required
def dashboard(payload):
    return jsonify({'message': 'access granted', 'username': payload['username']}), 200
    
    
