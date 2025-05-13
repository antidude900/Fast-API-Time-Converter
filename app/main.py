from fastapi import FastAPI, Query, HTTPException
from datetime import datetime, time
import pycountry
import pytz
from typing import Optional
from fastapi.responses import JSONResponse
from starlette.responses import Response
from .countries import COUNTRIES


app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello from the Timezone Converter!"}

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
            timezones = pytz.country_timezones.get(country.alpha_2)

            if not timezones:
                raise ValueError
            
            return timezones[0]
        
        except Exception:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid timezone or country name: {tz_or_country}"
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

@app.get("/convert_time")
async def convert_time(
    time: str = Query(..., description="Time to convert (e.g: '10:00'"),
    from_tz: str = Query(..., description="Source timezone (e.g: 'Asia/Kathmandu')"),
    to_tz: str = Query(..., description="Destination timezone (e.g: 'Asia/Delhi')"),
):
    try:
        dt_object = datetime.strptime(time, "%H:%M")
        time_obj = dt_object.time()
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid time format.  Please use HH:MM format (e.g., '10:00').",
        )

    converted_dt = convert_timezone(time_obj, from_tz, to_tz)
    final_from_tz =resolve_timezone(from_tz)
    final_to_tz = resolve_timezone(to_tz)

    return {
        "original_time": f"{time} {final_from_tz} {f"({from_tz})" if final_from_tz != from_tz else ''}".strip(),
        "converted_time": f"{converted_dt.strftime('%H:%M')} {final_to_tz} {f"({to_tz})" if final_to_tz != to_tz else ''}".strip(),
    }

@app.get("/all_timezones")
async def get_timezones():
    return {"timezones": pytz.all_timezones}

@app.get("/timezones/{country_name}")
def get_timezone(country_name: str):
    try:
        country = pycountry.countries.search_fuzzy(country_name)[0]
    except LookupError:
        raise HTTPException(
            status_code=400, detail=f"Invalid country name: {country_name}"
        )

    timezones = pytz.country_timezones.get(country.alpha_2)
    if not timezones:
        return {"country": country.name, "timezone": "No timezone found"}

    return {"country": country.name, "timezone": timezones}