from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.inventory_service import add_to_inventory, remove_from_inventory, get_inventory
import logging

inventory_bp = Blueprint('inventory', __name__)
logging.basicConfig(level=logging.INFO)

@inventory_bp.route('/inventory', methods=['GET'])
@jwt_required()
def get_inventory_endpoint():
    user_id = get_jwt_identity()
    inventory = get_inventory(user_id)
    if inventory is None:
        return jsonify({'msg': 'Error fetching inventory'}), 500
    return jsonify({'inventory': inventory}), 200

@inventory_bp.route('/add', methods=['POST'])
@jwt_required()
def add_to_inventory_endpoint():
    user_id = get_jwt_identity()
    data = request.get_json()
    item_name = data.get('item_name')
    quantity = data.get('quantity', 1)

    if not item_name:
        return jsonify({'msg': 'Item name is required'}), 400

    if add_to_inventory(user_id, item_name, quantity):
        return jsonify({'msg': f'Added {quantity} {item_name} to inventory'}), 200
    return jsonify({'msg': 'Failed to add item to inventory'}), 500

@inventory_bp.route('/remove', methods=['POST'])
@jwt_required()
def remove_from_inventory_endpoint():
    user_id = get_jwt_identity()
    data = request.get_json()
    item_name = data.get('item_name')
    quantity = data.get('quantity', 1)

    if not item_name:
        return jsonify({'msg': 'Item name is required'}), 400

    if remove_from_inventory(user_id, item_name, quantity):
        return jsonify({'msg': f'Removed {quantity} {item_name} from inventory'}), 200
    return jsonify({'msg': 'Failed to remove item from inventory'}), 500
