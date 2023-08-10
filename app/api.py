from flask import Blueprint, jsonify, current_app, session

api = Blueprint('api', __name__, url_prefix='/api/v1')

@api.route('/status')
def status():
    return jsonify({ "message": "API Operational" })