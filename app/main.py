from fastapi import FastAPI, Query, HTTPException
from datetime import datetime
import pycountry  # to get the timezone of a country if country name is provided
import pytz  # to convert time from one timezone to another
from app.utils import COUNTRIES, resolve_timezone, convert_timezone

app = FastAPI()


@app.get("/")
async def read_root():
    """
    Root endpoint to check if the API is running
    """
    return {"message": "Hello from the Timezone Converter!"}


@app.get("/convert_time")
async def convert_time(
    time: str = Query(..., description="Time to convert (e.g: '10:00'"),
    from_tz: str = Query(..., description="Source timezone (e.g: 'Asia/Kathmandu')"),
    to_tz: str = Query(..., description="Destination timezone (e.g: 'Asia/Delhi')"),
):
    """
    Endpoint to convert time from one timezone to another.

    Parameters:
    - time: Time in HH:MM format
    - from_tz: Source timezone (Can be a timezone or a country name)
    - to_tz: Destination timezone (Can be a timezone or a country name)

    Returns:
    - original_time: The original time with the source timezone and country name(if from_tz is a timezone)
    - converted_time: The converted time with the destination timezone and country name(if to_tz is a timezone)
    """
    try:
        dt_object = datetime.strptime(time, "%H:%M")
        time_obj = dt_object.time()
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid time format.  Please use HH:MM format (e.g., '10:00').",
        )

    converted_dt = convert_timezone(time_obj, from_tz, to_tz)
    final_from_tz = resolve_timezone(from_tz)
    final_to_tz = resolve_timezone(to_tz)

    return {
        "original_time": f"{time} {final_from_tz} {f'({from_tz})' if final_from_tz != from_tz else ''}".strip(),
        "converted_time": f"{converted_dt.strftime('%H:%M')} {final_to_tz} {f'({to_tz})' if final_to_tz != to_tz else ''}".strip(),
    }


@app.get("/all_timezones")
async def get_timezones():
    """
    Endpoint to get list of all timezones.
    """
    return {"timezones": pytz.all_timezones}


@app.get("/timezones/{country_name}")
def get_timezone(country_name: str):
    """
    Endpoint to get timezones for a given country name.

    Parameters:
    - country_name: Name of the country

    Returns:
    - country: Name of the country
    - timezone: List of timezones for the country
    """
    try:
        country = pycountry.countries.get(name=country_name)
        if not country:
            country = pycountry.countries.get(name=COUNTRIES.get(country_name))

        if not country:
            raise LookupError

        timezones = pytz.country_timezones.get(country.alpha_2)

        if not timezones:
            raise LookupError

        return {"country": country.name, "timezone": timezones}
    except LookupError:
        raise HTTPException(
            status_code=400, detail=f"Invalid country name: {country_name}"
        )
