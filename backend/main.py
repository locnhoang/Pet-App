# main.py - Place all your routes into this file
from flask import Flask, request, jsonify, redirect, url_for, render_template, send_from_directory
from flask_cors import CORS
from flasgger import Swagger
from users import *
from pets import *
from application import *
from questionnaire import *
from save_pet import *
from admin import *
import os

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)


# API Calls
# User Routes
@app.route('/api/sign_up', methods=['POST'])
def sign_up_user():
    """Calls create_user()"""
    return create_user()

@app.route('/api/login', methods=['POST'])
def login_user():
    """Calls log_user()"""
    return log_user()


# Pet Routes
@app.route('/api/pets', methods=['GET'])
def pets():
    """Calls get_pets"""
    return get_pets()

@app.route('/api/pets/<int:id>', methods=['GET'])
def pet_info(id):
    """Calls get_pet_info"""
    return get_pet_info(id)

@app.route('/api/admin/add_pet', methods=['POST'])
def handle_add_pet():
    return add_pet()

@app.route('/api/questionnaire', methods=['POST'])
def questionnaire():
    return submit_text_questionnaire()

@app.route('/api/application', methods=['POST'])
def send_application():
    return submit_application()

@app.route('/api/saved', methods=['POST'])
def send_save():
    return changeSaveState()

@app.route('/api/saved/<int:user_id>', methods=['GET'])
def saved(user_id):
    return savedPets(user_id)

@app.route('/api/saved/<int:user_id>/<int:pet_id>', methods=['GET'])
def isSaved(user_id, pet_id):
    return isPetSaved(user_id, pet_id)

@app.route('/api/admin/login', methods=['POST'])
def admin_login_route():
    return admin_login()

@app.route('/api/admin/questionnaires', methods=['GET'])
def list_pending_qs():
    return get_pending_questionnaires()

@app.route('/api/admin/questionnaires/<int:q_id>', methods=['PUT'])
def decide_q(q_id):
    approve = request.json.get("approve")   # 1 = approve, 0 = deny
    return set_questionnaire_decision(q_id, approve)

@app.route("/api/admin/applications", methods=["GET"])
def handle_get_applications():
    return get_pending_applications()

@app.route("/api/admin/applications/<int:app_id>", methods=["PUT"])
def handle_decide_application(app_id):
    data = request.get_json()
    return set_application_decision(app_id, data.get("approved"))

@app.route('/api/user/<int:user_id>/status', methods=['GET'])
def user_status(user_id):
    return get_questionnaire_status(user_id)

@app.route('/api/user/<int:user_id>/apply_status', methods=['GET'])
def apply_status(user_id):
    """Calls application_status"""
    return get_application_status(user_id)

@app.route('/')
def backend_home():
    return '<h1>Backend Server</h2>'
    #return render_template('home.html')

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(os.path.join(app.root_path, 'images'), filename)


if __name__ == "__main__":

    app.run(debug=True)
