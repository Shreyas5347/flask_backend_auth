from flask import Flask, jsonify
from auth import auth_bp
from db import init_db

app = Flask(__name__)
init_db()
app.register_blueprint(auth_bp)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask Backend Auth API", "status": "running"}), 200

if __name__ == '__main__':
    app.run(debug=True)
