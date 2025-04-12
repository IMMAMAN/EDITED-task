from flask import Blueprint, jsonify


health_blueprint = Blueprint('health', __name__)

@health_blueprint.route('/isalive', methods=['GET'])
def is_alive():
    return jsonify({"status": "OK"}), 200
