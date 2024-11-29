from unittest.mock import patch, MagicMock
from backend.services.inventory_service import InventoryService

@patch.object(InventoryService, 'get_inventory')
def test_get_inventory(mock_get_inventory, client, seed_user):
    user, access_token = seed_user

    # Mock return value
    mock_get_inventory.return_value = [
        {"item_name": "axe", "quantity": 1},
        {"item_name": "rope", "quantity": 3}
    ]

    # Make the GET request
    response = client.get(
        '/inventory',
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Assertions
    assert response.status_code == 200
    assert response.json == [
        {"item_name": "axe", "quantity": 1},
        {"item_name": "rope", "quantity": 3}
    ]
    mock_get_inventory.assert_called_once_with(user.id)

@patch.object(InventoryService, 'add_to_inventory')
def test_add_to_inventory(mock_add_to_inventory, client, seed_user):
    user, access_token = seed_user

    # Mock method behavior
    mock_add_to_inventory.return_value = {"message": "Added 1 axe"}

    # Payload
    payload = {"item_name": "axe", "quantity": 1}

    # Make the POST request
    response = client.post(
        '/inventory/add',
        json=payload,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Assertions
    assert response.status_code == 200
    assert response.json == {"message": "Added 1 axe"}
    mock_add_to_inventory.assert_called_once_with(user.id, "axe", 1)
