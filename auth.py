from flask import Flask, request, jsonify, Blueprint
from db import db_connection
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400
    hashed_password = generate_password_hash(password)
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("create table if not exists users (id integer primary key autoincrement, username text not null, hashed_password text not null)  ")
    cursor.execute("INSERT INTO users (username, hashed_password) VALUES (?, ?)", (username,hashed_password))
    conn.commit()
    conn.close()
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    if not check_password_hash(user['hashed_password'], password):
        return jsonify({'message': 'Invalid password'}), 401
    return jsonify({'message': 'User logged in successfully'}), 200
