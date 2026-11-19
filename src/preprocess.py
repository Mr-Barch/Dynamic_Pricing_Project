import pandas as pd

RAW_PATH = "data/raw_data.csv"

def load_raw(path=RAW_PATH):
    return pd.read_csv(path)


def drop_missing_and_duplicates(df):
    df = df.dropna(subset=["price"])
    df = df.drop_duplicates(subset=[c for c in df.columns if c != "id"])
    return df.reset_index(drop=True)

def add_base_price(df):
    df = df.copy()
    df["base_price"] = df["price"] / df["surge_multiplier"]
    return df


def remove_outliers(df, k=3.0):
    q1 = df.groupby("name")["base_price"].transform(lambda s: s.quantile(0.25))
    q3 = df.groupby("name")["base_price"].transform(lambda s: s.quantile(0.75))
    iqr = q3 - q1
    mask = (df["base_price"] >= q1 - k * iqr) & (df["base_price"] <= q3 + k * iqr)
    return df[mask].reset_index(drop=True)




if __name__ == "__main__":
    df = load_raw()
    print("Raw:", df.shape)
    df = drop_missing_and_duplicates(df)
    print("After cleaning:", df.shape)
    df = add_base_price(df)
    print(df["base_price"].describe())
    df = remove_outliers(df)
    print("After outliers:", df.shape)

