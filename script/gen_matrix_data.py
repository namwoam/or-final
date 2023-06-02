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
        travel_time[demand_index, supply_index] = t

distance_df = pd.DataFrame(
    distance, index=demand_locations, columns=supply_locations)
travel_time_df = pd.DataFrame(
    travel_time, index=demand_locations, columns=supply_locations)

distance_df.to_csv(os.path.join(
    os.path.dirname(__file__), "../data/distance-supply2market.csv"))
travel_time_df.to_csv(os.path.join(
    os.path.dirname(__file__), "../data/travel_time-supply2market.csv"))

distance = np.zeros((len(demand_locations), len(demand_locations)))
travel_time = np.zeros((len(demand_locations), len(demand_locations)))
for demand1_index, demand1_location in enumerate(demand_locations):
    for demand2_index,  demand2_location in enumerate(demand_locations):
        result = map_client.distance_matrix(demand1_location, demand2_location)
        # print(result)
        try:
            d = result["rows"][0]["elements"][0]["distance"]["value"]/1000
        except KeyError:
            d = 0
        try:
            t = result["rows"][0]["elements"][0]["duration"]["value"]/60
        except KeyError:
            t = 0
        print("From", demand1_location, "to", demand2_location)
        print(d, t)
        distance[demand1_index, demand2_index] = d
        travel_time[demand1_index, demand2_index] = t

distance_df = pd.DataFrame(
    distance, index=demand_locations, columns=demand_locations)
travel_time_df = pd.DataFrame(
    travel_time, index=demand_locations, columns=demand_locations)

distance_df.to_csv(os.path.join(
    os.path.dirname(__file__), "../data/distance-market2market.csv"))
travel_time_df.to_csv(os.path.join(
    os.path.dirname(__file__), "../data/travel_time-market2market.csv"))

geo_data_df = pd.DataFrame(columns=["place", "lat", "lng"])
for place in supply_locations:
    print(place)