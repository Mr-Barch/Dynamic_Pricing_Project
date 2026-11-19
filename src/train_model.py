import pandas as pd

PROCESSED_PATH = "data/processed_data.csv"
def load_processed(path=PROCESSED_PATH):
    return pd.read_csv(path)

def time_split(df, train_frac=0.7, val_frac=0.1):
    n = len(df)
    train_end = int(n * train_frac)
    val_end = int(n * (train_frac + val_frac))
    train = df.iloc[:train_end]
    val = df.iloc[train_end:val_end]
    test = df.iloc[val_end:]
    return train, val, test

if __name__ == "__main__":
    df = load_processed()
    train, val, test = time_split(df)
    for name, part in [("train", train), ("val", val), ("test", test)]:
        print(name, part.shape, part["timestamp"].min(), part["timestamp"].max())