from unittest.mock import patch
from backend.services.resource_service import ResourceService

@patch.object(ResourceService, 'get_resources')
def test_get_resources(mock_get_resources, client, seed_user):
    user, access_token = seed_user

    # Mock return
    mock_get_resources.return_value = [
        {"id": 1, "type": "wood", "quantity": 100},
        {"id": 2, "type": "stone", "quantity": 50}
    ]

    response = client.get(
        '/room/resources',
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert response.json == [
        {"id": 1, "type": "wood", "quantity": 100},
        {"id": 2, "type": "stone", "quantity": 50}
    ]
    mock_get_resources.assert_called_once_with(user.room_id)

@patch.object(ResourceService, 'collect_resource')
def test_collect_resource(mock_collect_resource, client, seed_user):
    user, access_token = seed_user

    # Mock return
    mock_collect_resource.return_value = {"msg": "Collected 10 wood"}

    payload = {"resource_id": 1, "quantity": 10}
    response = client.post(
        '/resource/collect',
        json=payload,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert response.json == {"msg": "Collected 10 wood"}
    mock_collect_resource.assert_called_once_with(user.id, 1, 10)
