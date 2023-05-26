import pandas as pd
import os

df = pd.read_csv(os.path.join(os.path.dirname(
    __file__), "../data/consumption.csv"))

markets = df["market_name"].unique()

for market in markets:
    market_demand_df = df[df["market_name"] == market]
    market_demand_df = market_demand_df[["mean_price", "quantity", "date"]]
    market_demand_df.columns = ["P", "Q", "t"]
    if market_demand_df["P"].sum() == 0:
        continue
    market_demand_df.to_csv(os.path.join(os.path.dirname(
        __file__), f"../data/demand_function/{market}.csv"))
