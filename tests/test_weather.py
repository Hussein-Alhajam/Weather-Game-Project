from unittest.mock import patch
from backend.services.weather_service import WeatherService

@patch.object(WeatherService, 'get_current_weather')
def test_get_weather(mock_get_weather, client, seed_user):
    user, access_token = seed_user

    # Mock return value
    mock_get_weather.return_value = {"condition": "Sunny", "temperature": "25°C"}

    # Make the GET request
    response = client.get(
        '/weather/current',
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Assertions
    assert response.status_code == 200
    assert response.json == {"condition": "Sunny", "temperature": "25°C"}
    mock_get_weather.assert_called_once_with(user.id)
