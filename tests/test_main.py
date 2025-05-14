from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from the Timezone Converter!"}


def test_convert_time_valid_conversion():
    response = client.get(
        "/convert_time",
        params={
            "time": "10:00",
            "from_tz": "America/Los_Angeles",
            "to_tz": "America/New_York",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["original_time"] == "10:00 America/Los_Angeles"
    assert data["converted_time"] == "13:00 America/New_York"


def test_convert_time_utc_conversion():
    response = client.get(
        "/convert_time",
        params={
            "time": "12:00",
            "from_tz": "UTC",
            "to_tz": "Europe/London",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["original_time"] == "12:00 UTC"
    assert data["converted_time"] == "13:00 Europe/London"


def test_convert_time_invalid_timezone():
    response = client.get(
        "/convert_time",
        params={
            "time": "10:00",
            "from_tz": "Invalid/Timezone",
            "to_tz": "Europe/London",
        },
    )
    assert response.status_code == 400
    assert "Invalid timezone or country name" in response.json()["detail"]


def test_convert_time_invalid_time_format():
    response = client.get(
        "/convert_time",
        params={
            "time": "Invalid Time",
            "from_tz": "America/Los_Angeles",
            "to_tz": "Europe/London",
        },
    )
    assert response.status_code == 400
    assert "Invalid time format" in response.json()["detail"]


def test_all_timezones():
    response = client.get("/all_timezones")
    assert response.status_code == 200
    data = response.json()
    assert "timezones" in data
    assert len(data["timezones"]) > 0


def test_get_timezone_valid_country_name():
    response = client.get("/timezones/United States")
    assert response.status_code == 200
    data = response.json()
    assert data["country"] == "United States"
    assert len(data["timezone"]) > 0


def test_get_timezone_valid_country_code():
    response = client.get("/timezones/United States")
    assert response.status_code == 200
    data = response.json()
    assert data["country"] == "United States"
    assert len(data["timezone"]) > 0


def test_get_timezone_invalid_country_name():
    response = client.get("/timezones/InvalidCountry")
    assert response.status_code == 400
    assert "Invalid country name" in response.json()["detail"]


def test_get_timezone():
    response = client.get("/timezones/Russia")
    assert response.status_code == 200
    data = response.json()
    assert data["country"] == "Russian Federation"
    assert len(data["timezone"]) > 0


def test_convert_time_with_country_name():
    response = client.get(
        "/convert_time",
        params={"time": "15:00", "from_tz": "Nepal", "to_tz": "United States"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "Asia/Kathmandu" in data["original_time"]
    assert "America/New_York" in data["converted_time"]


def test_convert_time_with_official_country_name():
    response = client.get(
        "/convert_time",
        params={
            "time": "09:00",
            "from_tz": "Korea, Republic of",
            "to_tz": "America/Los_Angeles",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "Asia/Seoul (Korea, Republic of)" in data["original_time"]
    assert " America/Los_Angeles" in data["converted_time"]
