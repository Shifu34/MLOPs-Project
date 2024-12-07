from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from datetime import timedelta
import bcrypt

app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"  # Adjust the URI according to your MongoDB setup
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

mongo = PyMongo(app)
jwt = JWTManager(app)
db = mongo.db

# User collection
users = db.users

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password'].encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())  # Hashing the password before storing

    # Check if username exists
    if users.find_one({"username": username}):
        return jsonify({'message': 'Username already exists'}), 409

    users.insert_one({
        "username": username,
        "password": hashed
    })
    return jsonify({'message': 'User created successfully.'}), 201

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = users.find_one({"username": data['username']})

    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
        token = create_access_token(identity=user['username'])
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# Prediction endpoint
@app.route('/predict', methods=['POST'])
@jwt_required()
def predict():
    data = request.get_json()
    # Dummy logic for prediction
    result = {'temperature': data['temperature'] * 1.8 + 32}  # Convert C to F for demonstration
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
