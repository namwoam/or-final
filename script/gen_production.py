import pandas as pd
import os
df = pd.read_csv(os.path.join(os.path.dirname(__file__), "COA_OpenData.csv"))
cabbage_df = df[df["蔬菜類別"] == "甘藍"]
cabbage_df = cabbage_df[["年度", "地區別", "產量"]]
cabbage_df.columns = ["year", "region", "quantity"]
cabbage_df.to_csv(os.path.join(
    os.path.dirname(__file__), "../data/production.csv"))
