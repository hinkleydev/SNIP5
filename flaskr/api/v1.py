from flask import Blueprint, jsonify
from api.reader import data

api = Blueprint('api', __name__)

# Root - Returns amount of snippets and languages in use
@api.route('/')
def root():
    languages = []
    for each in data :
        languages.append(each["lang"])
    languages = set(languages)
    languages = list(languages)
    return jsonify({"snippets" : len(data), "languages" : languages})
