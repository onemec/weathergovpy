from enum import Enum
from typing import Optional, Tuple

import urllib3
from pydantic import BaseModel, EmailStr


class WeatherAPIResponseFormat(str, Enum):
    GEOJSON = "application/geo+json"
    JSON_LD = "application/ld+json"
    DWML = "application/vnd.noaa.dwml+xml"
    OXML = "application/vnd.noaa.obs+xml"
    CAP = "application/cap+xml"
    ATOM = "application/atom+xml"

    def header_string(self) -> str:
        """
        Get the HTTP header string to specify your requested response format.

        :return: str
        """
        return f"Accept: {self.value}"


class WeatherAPIClient(BaseModel):
    # Configure your API client details
    # https://www.weather.gov/documentation/services-web-api
    website: Optional[str] = "myweatherapp.com"
    email: Optional[EmailStr] = "contact@myweatherapp.com"
    response_format: Optional[WeatherAPIResponseFormat] = WeatherAPIResponseFormat[
        "CAP"
    ]
    grid_office: Optional[str] = None
    coordinates: Optional[Tuple[float, float]] = None
    http2: Optional[bool] = False

    def get_grid_office(self) -> None:
        """
        Set the office if we haven't manually set `self.grid_office`.

        :return:
        """
        if not self.coordinates:
            raise ValueError("`grid_office` or `coordinates` must be set")
        office_rsp = urllib3.request(
            method="get",
            url=f"https://api.weather.gov/points/{self.coordinates[0]},{self.coordinates[1]}",
        )
        if office_rsp.status != 200:
            raise ConnectionError(
                f"Got a non-200 response code {office_rsp.status} while trying to fetch grid_office."
            )
        grid_office = office_rsp.json().get("properties", {}).get("cwa", "")
        if not grid_office:
            raise ValueError(
                "Failed to retrieve office code for given coordinates.")
        self.grid_office = grid_office
