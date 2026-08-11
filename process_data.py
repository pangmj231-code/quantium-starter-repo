import pandas as pd
import glob
import os

all_files = glob.glob("data/*.csv")

processed_dfs = []

for file in all_files:
    df = pd.read_csv(file)
    
    pink_df = df[df["product"] == "Pink Morsel"].copy()
    
    pink_df["sales"] = pink_df["quantity"] * pink_df["price"]
    
    final_df = pink_df[["sales", "date", "region"]]
    
    processed_dfs.append(final_df)

final_output = pd.concat(processed_dfs, ignore_index=True)

final_output.to_csv("formatted_output.csv", index=False)