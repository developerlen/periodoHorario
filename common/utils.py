import os
import pandas as pd


def write_excel(df: pd.DataFrame, dir_path: str, filename: str):
    filepath = os.path.join(dir_path, filename)
    df.to_excel(filepath)
    print(f"\n\nDone! --> check the file {filename} in the folder:\n{dir_path}\n\n")
