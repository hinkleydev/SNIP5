from flask import Blueprint, render_template, jsonify

snippets = Blueprint('simple_page', __name__)

@snippets.route('/', defaults={'page': 'index'})
def all(page):
    return jsonify({"message": "working"})