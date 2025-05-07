from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import datetime

app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'super-secret-kodex-key'
jwt = JWTManager(app)

USERS = {
    "nessa": {
        "password": "kodex123"
    }
}

@app.route("/auth/login", methods=["POST"])
def login():
    username = request.json.get("username", "")
    password = request.json.get("password", "")
    user = USERS.get(username)
    if user and user["password"] == password:
        token = create_access_token(identity=username, expires_delta=datetime.timedelta(days=1))
        return jsonify(access_token=token), 200
    return jsonify({"msg": "Bad credentials"}), 401

@app.route("/auth/protected", methods=["GET"])
@jwt_required()
def protected():
    identity = get_jwt_identity()
    return jsonify(logged_in_as=identity), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

@app.route("/")
def index():
    return "Kodex Auth API is live."
