from pydantic import ValidationError

from weathergovpy import WeatherAPIClient, WeatherAPIResponseFormat


def test_default_values():
    client = WeatherAPIClient(grid_office="ABCD")
    assert client.website == "myweatherapp.com"
    assert client.email == "contact@myweatherapp.com"
    assert client.response_format == WeatherAPIResponseFormat["CAP"]
    assert client.grid_office == "ABCD"
    assert client.coordinates is None
    assert client.http2 is False


def test_get_grid_office_success():
    client = WeatherAPIClient(coordinates=(37.7749, -122.4194))
    client.get_grid_office()
    assert client.grid_office == "MTR"


def test_get_grid_office_coordinates_required():
    client = WeatherAPIClient()
    with pytest.raises(ValueError, match="`grid_office` or `coordinates` must be set"):
        client.get_grid_office()


def test_get_grid_office_non_200_response():
    client = WeatherAPIClient(coordinates=(1000.0, 2000.0))  # Fake invalid coordinates
    with pytest.raises(ConnectionError, match="Got a non-200 response code .*"):
        client.get_grid_office()


def test_get_grid_office_missing_office_code():
    client = WeatherAPIClient(
        coordinates=(38.9072, -77.0369)
    )  # Fake coordinates with missing office code
    with pytest.raises(
        ValueError, match="Failed to retrieve office code for given coordinates."
    ):
        client.get_grid_office()


def test_email_validation():
    with pytest.raises(ValidationError):
        WeatherAPIClient(email="invalid_email")


def test_valid_email():
    client = WeatherAPIClient(email="valid.email@example.com")
    assert client.email == "valid.email@example.com"


def test_setting_http2():
    client = WeatherAPIClient(http2=True)
    assert client.http2 is True
