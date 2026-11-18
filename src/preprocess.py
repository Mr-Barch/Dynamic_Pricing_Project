import pandas as pd

RAW_PATH = "data/raw_data.csv"

def load_raw(path=RAW_PATH):
    return pd.read_csv(path)


def drop_missing_and_duplicates(df):
    df = df.dropna(subset=["price"])
    df = df.drop_duplicates(subset=[c for c in df.columns if c != "id"])
    return df.reset_index(drop=True)



if __name__ == "__main__":
    df = load_raw()
    print("Raw:", df.shape)
    df = drop_missing_and_duplicates(df)
    print("After cleaning:", df.shape)
