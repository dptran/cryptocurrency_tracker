from app.blueprints.main.models import Tracker
from .import bp as api
from flask import json, jsonify, request
from .auth import token_auth
from app import db


@api.route('/tracker/<int:id>', methods=['GET'])
@token_auth.login_required
def get_tracker(id):
    return jsonify(Tracker.query.get(id).to_dict())
