from flask import Blueprint, jsonify

api = Blueprint('api', __name__)

@api.route('/')
def root():
    return jsonify({"version" : "1.0"})
