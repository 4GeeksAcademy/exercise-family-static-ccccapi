import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from random import randint

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._members = [
            {"id": 1, "first_name": "Tommy", "age": 23, "lucky_numbers": [34, 65, 23, 4, 6], "last_name": last_name},
            {"id": 2, "first_name": "Sandra", "age": 22, "lucky_numbers": [12, 34, 33, 45, 32], "last_name": last_name},
            {"id": 3, "first_name": "John", "age": 45, "lucky_numbers": [21, 56, 34, 12], "last_name": last_name}
        ]
    
    def _generateId(self):
        return randint(0, 99999999)

    def add_member(self, member):
        if "id" not in member:
            member["id"] = self._generateId()
        if "last_name" not in member:
            member["last_name"] = self.last_name
        self._members.append(member)
        return member

    def delete_member(self, id):
        for i, member in enumerate(self._members):
            if member["id"] == id:
                self._members.pop(i)
                return {"done": True}
        return {"done": False}

    def get_member(self, id):
        for member in self._members:
            if member["id"] == id:
                return member
        return None

    def update_member(self, id, data):
        for i, member in enumerate(self._members):
            if member["id"] == id:
                updated_member = {**member, **data, "id": id}
                self._members[i] = updated_member
                return updated_member
        return None

    def get_all_members(self):
        return self._members

jackson_family = FamilyStructure("Jackson")

@app.errorhandler(Exception)
def handle_invalid_usage(error):
    return jsonify({"message": str(error)}), 400

@app.route('/members', methods=['GET'])
def get_all_members():
    return jsonify(jackson_family.get_all_members()), 200

@app.route('/members', methods=['POST'])
def add_member():
    member_data = request.get_json()

    required_fields = ["first_name", "age", "lucky_numbers"]
    if not all(field in member_data for field in required_fields):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    new_member = jackson_family.add_member(member_data)

    return jsonify({
        "id": new_member["id"],
        "first_name": new_member["first_name"],
        "age": new_member["age"],
        "lucky_numbers": new_member["lucky_numbers"],
        "last_name": new_member["last_name"]
    }), 200

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"message": "Member not found"}), 404

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    result = jackson_family.delete_member(id)
    return jsonify(result), 200

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    data = request.get_json()
    updated = jackson_family.update_member(id, data)
    if updated:
        return jsonify(updated), 200
    else:
        return jsonify({"message": "Member not found"}), 404

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
