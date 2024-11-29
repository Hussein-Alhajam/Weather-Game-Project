from backend.extensions import db
from models.resource import Resource
import logging

from services.inventory_service import add_to_inventory

def get_resources_in_room(room_id):
    try:
        resources = Resource.query.filter_by(room_id=room_id).all()
        return [{
            "type": resource.type,
            "quantity": resource.quantity,
            "location": (resource.location_x, resource.location_y)
        } for resource in resources]
    except Exception as e:
        logging.error(f"Error fetching resources for room {room_id}: {e}")
        return None

def collect_resource(user_id, resource_id, quantity):
    try:
        resource = Resource.query.get(resource_id)
        if not resource or resource.quantity < quantity:
            return False  # Not enough resource to collect

        resource.quantity -= quantity
        if resource.quantity == 0:
            db.session.delete(resource)

        db.session.commit()

        # Add resource to player's inventory
        add_to_inventory(user_id, resource.type, quantity)

        return True
    except Exception as e:
        logging.error(f"Error collecting resource {resource_id}: {e}")
        db.session.rollback()
        return False
