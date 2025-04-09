"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# GET all members
@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

# GET a single member by ID
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({"error": "Miembro no encontrado"}), 404
    return jsonify(member), 200

# POST a new member
@app.route('/member', methods=['POST'])
def add_member():
    member_data = request.get_json()
    if not member_data:
        return jsonify({"error": "Datos requeridos"}), 400

    new_member = jackson_family.add_member(member_data)
    return jsonify(new_member), 201

# DELETE a member
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    deleted = jackson_family.delete_member(member_id)
    if not deleted:
        return jsonify({"error": "Miembro no encontrado"}), 404
    return jsonify({"message": "Miembro eliminado"}), 200

# PUT to update a member
@app.route('/member/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    data = request.get_json()
    updated = jackson_family.update_member(member_id, data)
    if updated is None:
        return jsonify({"error": "Miembro no encontrado"}), 404
    return jsonify(updated), 200

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
