from unittest.mock import patch, MagicMock
from backend.services.room_service import RoomService

@patch.object(RoomService, 'create_room')
def test_create_room(mock_create_room, client, seed_user):
    user, access_token = seed_user

    # Mock return
    mock_create_room.return_value = MagicMock(id=1, room_name="test_room")

    # Payload
    payload = {"room_name": "test_room"}

    # Make the POST request
    response = client.post(
        '/room/create',
        json=payload,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Assertions
    assert response.status_code == 201
    assert response.json == {"msg": "Room 'test_room' created successfully", "room_id": 1}
    mock_create_room.assert_called_once_with("test_room", user.id)

@patch.object(RoomService, 'join_room')
def test_join_room(mock_join_room, client, seed_user):
    user, access_token = seed_user

    # Mock return
    mock_join_room.return_value = {"msg": "Joined room successfully"}

    # Payload
    payload = {"room_name": "test_room"}

    # Make the POST request
    response = client.post(
        '/room/join',
        json=payload,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Assertions
    assert response.status_code == 200
    assert response.json == {"msg": "Joined room successfully"}
    mock_join_room.assert_called_once_with("test_room", user.id)
