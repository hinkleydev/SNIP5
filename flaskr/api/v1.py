from flask import Blueprint, jsonify
from api.reader import data

api = Blueprint('api', __name__)

# Root - Returns amount of snippets and languages in use
@api.route('/snippets')
def root():
    languages = []
    for each in data :
        languages.append(each["lang"])
    languages = set(languages) # Remove the duplicates
    languages = list(languages) # Remake list to add to JSON
    return jsonify({"snippets" : len(data), "languages" : languages})

# Specific - Returns all the details of a specific snippet
@api.route('/snippets/<int:id>')
def byID(id):
    for each in data :
        if id != each["id"] : continue # Pass if not what we're after
        return jsonify(each)
    return jsonify({"error" : "not found"}), 404 # Default if nothing is found