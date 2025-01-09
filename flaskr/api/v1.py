from flask import Blueprint, jsonify
from api.reader import data

api = Blueprint('api', __name__)

@api.route('/')
def root():
    return jsonify({"snippets" : len(data)})
