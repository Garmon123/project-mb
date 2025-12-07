from flask import jsonify

def hello():
    return jsonify(message="Welcome to the API!")
