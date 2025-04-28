from flask import Flask, render_template, request
import requests
import pandas as pd
import os
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import datetime

app = Flask(__name__)

SERVICE_URL = (
    "https://services3.arcgis.com/Et5Qfajgiyosiw4d/"
    "arcgis/rest/services/AxonCrimeData_Export_view/FeatureServer/19/query"
)
CACHE_CSV = "crime_data.csv"

def fetch_all_features():
    params = {
        "where":"1=1","outFields":"*","f":"json",
        "orderByFields":"OBJECTID ASC",
        "resultRecordCount":2000,"resultOffset":0
    }
    all_attrs = []
    while True:
        r = requests.get(SERVICE_URL, params=params); r.raise_for_status()
        batch = r.json().get("features", [])
        if not batch: break
        all_attrs += [f["attributes"] for f in batch]
        params["resultOffset"] += params["resultRecordCount"]
    return all_attrs

def load_crime_data():
    if os.path.exists(CACHE_CSV):
        df = pd.read_csv(CACHE_CSV)
    else:
        recs = fetch_all_features()
        df = pd.DataFrame(recs) if recs else pd.DataFrame()
        if not df.empty:
            df.to_csv(CACHE_CSV, index=False)
    return df

def geocode_address(address):
    loc = Nominatim(user_agent="safety_app").geocode(address)
    return (loc.latitude, loc.longitude) if loc else None

def filter_crimes_nearby(df, loc, radius_km=1.0):
    latc = next((c for c in df.columns if "lat" in c.lower()), None)
    lonc = next((c for c in df.columns if "lon" in c.lower()), None)
    if not latc or not lonc:
        return pd.DataFrame()
    df = df.dropna(subset=[latc, lonc])
    df["Distance_km"] = df.apply(
        lambda r: geodesic(loc, (r[latc], r[lonc])).km, axis=1
    )
    return df[df["Distance_km"] <= radius_km]

def calculate_safety_score(df):
    weights = {
        "HOMICIDE":10,"RAPE":9,"ROBBERY":8,"AGGRAVATED ASSAULT":7,
        "BURGLARY":6,"LARCENY":5,"MOTOR VEHICLE THEFT":7,"ARSON":6
    }
    now = datetime.datetime.now()
    total = 0.0

    # normalize date field if present
    if "OCCUR_DATE" in df.columns:
        df["occur_dt"] = pd.to_datetime(df["OCCUR_DATE"], unit="ms", errors="coerce")

    for _, r in df.iterrows():
        # pick a crime-type column that exists
        ct = None
        for key in ("OFFENSE_DESC","UCR_Literal","ucr_literal","CRIME"):
            if key in r and pd.notna(r[key]):
                ct = str(r[key]).upper()
                break
        base = weights.get(ct, 3)

        odt = r.get("occur_dt")
        if pd.notna(odt):
            days = (now - odt).days
            recency = max(0, (30 - days) / 30)
            tod = 1.2 if 6 <= odt.hour < 18 else 1.0
        else:
            recency, tod = 0.0, 1.0

        total += base * (1 + recency) * tod

    return round(max(0, 100 - total), 1)

@app.route("/", methods=["GET","POST"])
def index():
    safety_score = None
    address      = None
    crimes       = None
    error        = None

    if request.method == "POST":
        address = request.form["address"]
        loc     = geocode_address(address)
        if not loc:
            error = "Could not geocode that address."
        else:
            df = load_crime_data()
            if df.empty:
                error = "No crime data available."
            else:
                crimes = filter_crimes_nearby(df, loc, 1.0)
                # DEBUG: print available columns
                print("🔍 Crime columns:", crimes.columns.tolist())
                if crimes.empty:
                    error = "No crimes found within 1 km."
                else:
                    safety_score = calculate_safety_score(crimes)

    return render_template(
        "index.html",
        safety_score=safety_score,
        crimes=crimes,
        address=address,
        error_message=error
    )

if __name__ == "__main__":
    app.run(debug=True)
