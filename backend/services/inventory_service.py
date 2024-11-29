from extensions import db
from models.Inventory import Inventory
import logging

def add_to_inventory(user_id, item_name, quantity):
    try:
        # Check if the item already exists in the inventory
        item = Inventory.query.filter_by(user_id=user_id, item_name=item_name).first()
        if item:
            item.quantity += quantity
        else:
            
            new_item = Inventory(user_id=user_id, item_name=item_name, quantity=quantity)
            db.session.add(new_item)
        
        db.session.commit()
        return True
    except Exception as e:
        logging.error(f"Error adding to inventory: {e}")
        db.session.rollback()
        return False

def remove_from_inventory(user_id, item_name, quantity):
    try:
        item = Inventory.query.filter_by(user_id=user_id, item_name=item_name).first()
        if not item or item.quantity < quantity:
            return False  # Not enough items to remove

        item.quantity -= quantity
        if item.quantity == 0:
            db.session.delete(item)

        db.session.commit()
        return True
    except Exception as e:
        logging.error(f"Error removing from inventory: {e}")
        db.session.rollback()
        return False

def get_inventory(user_id):
    try:
        items = Inventory.query.filter_by(user_id=user_id).all()
        return [{"item_name": item.item_name, "quantity": item.quantity} for item in items]
    except Exception as e:
        logging.error(f"Error fetching inventory for user {user_id}: {e}")
        return None
