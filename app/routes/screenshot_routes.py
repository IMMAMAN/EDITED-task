import logging
import os
import uuid
import zipfile

from flask import Blueprint, current_app, jsonify, request, send_file

from app.services.screenshot_service import start_screenshot_process
from app.utils.helper import check_valid_num_tries, check_valid_url


screenshot_blueprint = Blueprint('screenshots', __name__)


@screenshot_blueprint.route('/', methods=['POST'])
def take_screenshot():
    data = request.get_json()
    
    start_url = data.get("start_url")
    num_links = data.get("num_links")
    

    # this part could be moved to a seperate function
    # routes should only handle routing
    if not start_url or not num_links:
        return jsonify({"error": "start_url and num_links are required"}), 400
    if not check_valid_num_tries(num_links):
        return jsonify({"error": "num_links must be a positive integer"}), 400
    if not check_valid_url(start_url):
        return jsonify({"error": "Invalid URL"}), 400

    unique_id = str(uuid.uuid4())
    logging.info(f"Generated unique ID: {unique_id}")
    success = start_screenshot_process(start_url, num_links, unique_id)

    if success:
        return jsonify({"id": unique_id}), 202
    else:
        return jsonify({"error": "Failed to start screenshot process"}), 500

@screenshot_blueprint.route('/<id>', methods=['GET'])
def get_screenshot(id):
    # TODO: move this to a helper function
    screenshot_folder = os.path.join(current_app.root_path, 'screenshots', id)

    screenshot_path = os.path.join(screenshot_folder, f"{id}.png")
    zip_filename = f"{id}.zip"
    zip_path = os.path.join(screenshot_folder, zip_filename)
    try:
        return send_file(zip_path, mimetype='application/zip', as_attachment=True, download_name = zip_filename)
    except FileNotFoundError:
        return jsonify({"error": f"Screenshots not found for this ID screenshot_path:{screenshot_path}"}), 404
    except Exception as e:
        logging.error(f"Error retrieving screenshots for ID {id}: {e}")
        return jsonify({"error": "Internal server error"}), 500
