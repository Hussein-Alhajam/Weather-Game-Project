from unittest.mock import patch
from backend.services.game_service import GameService

@patch.object(GameService, 'initialize_game_room')
def test_initialize_game_room(mock_initialize, client, seed_user):
    user, access_token = seed_user

    # Mock return
    mock_initialize.return_value = {"msg": "Game room initialized successfully"}

    payload = {
        "room_id": 1,
        "players": [{"user_id": user.id}],
        "resources": [{"type": "wood", "quantity": 50}],
        "inventory": {str(user.id): [{"item_name": "axe", "quantity": 1}]}
    }

    response = client.post(
        '/game/initialize',
        json=payload,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert response.json == {"msg": "Game room initialized successfully"}
    mock_initialize.assert_called_once_with(1, [{"user_id": user.id}], [{"type": "wood", "quantity": 50}], {str(user.id): [{"item_name": "axe", "quantity": 1}]})

@patch.object(GameService, 'save_game')
def test_save_game(mock_save_game, client, seed_user):
    user, access_token = seed_user

    # Mock return
    mock_save_game.return_value = {"msg": "Game state saved successfully"}

    response = client.post(
        '/game/save',
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert response.json == {"msg": "Game state saved successfully"}
    mock_save_game.assert_called_once_with(user.id)

@patch.object(GameService, 'load_game')
def test_load_game(mock_load_game, client, seed_user):
    user, access_token = seed_user

    # Mock return
    mock_load_game.return_value = {"msg": "Game state loaded successfully"}

    response = client.get(
        '/game/load?save_id=1',
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert response.json == {"msg": "Game state loaded successfully"}
    mock_load_game.assert_called_once_with(user.id, 1)
