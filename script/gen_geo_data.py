from dotenv import load_dotenv
import os
import numpy as np
import pandas as pd
import googlemaps

load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))

goole_map_api = os.getenv('GOOGLE_MAP_API')
map_client = googlemaps.Client(key=goole_map_api)

production_df = pd.read_csv(os.path.join(
    os.path.dirname(__file__), "../data/production.csv"))
consumption_df = pd.read_csv(os.path.join(
    os.path.dirname(__file__), "../data/consumption.csv"))

supply_locations = list(production_df["region"].unique())
demand_locations = consumption_df["market_name"].unique()
demand_locations = [
    f"{market_name}綜合農產品批發市場" for market_name in demand_locations]
geo_data_df = pd.DataFrame(columns=["place", "lat", "lng"])
for place in supply_locations+demand_locations:
    res = map_client.find_place(place, input_type="textquery")
    place_id = res["candidates"][0]["place_id"]
    res = map_client.place(place_id)
    location = res["result"]["geometry"]["location"]
    geo_data_df.loc[len(geo_data_df)] = [
        place, location["lat"], location["lng"]]


print(geo_data_df)

geo_data_df.to_csv(os.path.join(os.path.dirname(
    __file__), "../", "data", "geo_data.csv"))
