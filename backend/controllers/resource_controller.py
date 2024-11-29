from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.resource_service import get_resources_in_room, collect_resource
import logging

resource_bp = Blueprint('resource', __name__)
logging.basicConfig(level=logging.INFO)

@resource_bp.route('/room/<int:room_id>', methods=['GET'])
@jwt_required()
def get_resources_endpoint(room_id):
    resources = get_resources_in_room(room_id)
    if resources is None:
        return jsonify({'msg': 'Error fetching resources'}), 500
    return jsonify({'resources': resources}), 200

@resource_bp.route('/collect', methods=['POST'])
@jwt_required()
def collect_resource_endpoint():
    user_id = get_jwt_identity()
    data = request.get_json()
    resource_id = data.get('resource_id')
    quantity = data.get('quantity', 1)

    if not resource_id:
        return jsonify({'msg': 'Resource ID is required'}), 400

    if collect_resource(user_id, resource_id, quantity):
        return jsonify({'msg': f'Collected {quantity} of resource {resource_id}'}), 200
    return jsonify({'msg': 'Failed to collect resource'}), 500
