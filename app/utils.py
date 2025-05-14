from datetime import datetime, time
from fastapi import HTTPException
import pycountry
import pytz


COUNTRIES = {
    "Bolivia": "Bolivia, Plurinational State of",
    "Iran": "Iran, Islamic Republic of",
    "Laos": "Lao People's Democratic Republic",
    "Moldova": "Moldova, Republic of",
    "North Korea": "Korea, Democratic People's Republic of",
    "South Korea": "Korea, Republic of",
    "Syria": "Syrian Arab Republic",
    "Tanzania": "Tanzania, United Republic of",
    "Venezuela": "Venezuela, Bolivarian Republic of",
    "Vietnam": "Viet Nam",
    "Czechia": "Czech Republic",
    "Russia": "Russian Federation",
    "Taiwan": "Taiwan, Province of China",
}


def resolve_timezone(tz_or_country: str) -> str:
    try:
        pytz.timezone(tz_or_country)
        return tz_or_country
    except pytz.UnknownTimeZoneError:
        try:
            tz_or_country = tz_or_country.strip().capitalize()

            country_name = COUNTRIES.get(tz_or_country)

            if country_name is None:
                country_name = tz_or_country
            country = pycountry.countries.get(name=country_name)

            if country is None:
                raise LookupError

            timezones = pytz.country_timezones.get(country.alpha_2)

            if not timezones:
                raise LookupError

            return timezones[0]

        except Exception:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid timezone or country name: {tz_or_country}",
            )


def convert_timezone(input_time: time, from_tz: str, to_tz: str) -> datetime:
    from_zone_name = resolve_timezone(from_tz)
    to_zone_name = resolve_timezone(to_tz)

    from_zone = pytz.timezone(from_zone_name)
    to_zone = pytz.timezone(to_zone_name)

    naive_datetime = datetime.combine(datetime.today(), input_time)
    localized_datetime = from_zone.localize(naive_datetime)
    converted_datetime = localized_datetime.astimezone(to_zone)

    return converted_datetime
