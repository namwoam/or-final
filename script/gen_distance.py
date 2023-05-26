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

supply_locations = production_df["region"].unique()
demand_locations = consumption_df["market_name"].unique()
print(demand_locations)
demand_locations_code = consumption_df["market_code"].unique()
print(demand_locations_code)
demand_locations = [
    f"{market_name}綜合農產品批發市場" for market_name in demand_locations]

distance = np.zeros((len(demand_locations), len(supply_locations)))
travel_time = np.zeros((len(demand_locations), len(supply_locations)))
for demand_index, demand_location in enumerate(demand_locations):
    for supply_index,  supply_location in enumerate(supply_locations):
        result = map_client.distance_matrix(supply_location, demand_location)
        # print(result)
        try:
            d = result["rows"][0]["elements"][0]["distance"]["value"]/1000
        except KeyError:
            d = 0
        try:
            t = result["rows"][0]["elements"][0]["duration"]["value"]/60
        except KeyError:
            t = 0
        print("From", supply_location, "to", demand_location)
        print(d, t)
        distance[demand_index, supply_index] = d
        travel_time[demand_index, supply_index] = d

distance_df = pd.DataFrame(
    distance, index=demand_locations_code, columns=supply_locations)
travel_time_df = pd.DataFrame(
    travel_time, index=demand_locations_code, columns=supply_locations)

distance_df.to_csv(os.path.join(
    os.path.dirname(__file__), "../data/distance.csv"))
travel_time_df.to_csv(os.path.join(
    os.path.dirname(__file__), "../data/travel_time.csv"))
