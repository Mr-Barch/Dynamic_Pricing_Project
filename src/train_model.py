import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

PROCESSED_PATH = "data/processed_data.csv"
CATEGORICAL_COLS = ["name", "source", "destination"]
NUMERIC_COLS = ["distance"]
FEATURE_COLS = CATEGORICAL_COLS + NUMERIC_COLS

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

# MAE, RMSE, R2
def evaluate(df, pred_base):
    final_pred = pred_base * df["surge_multiplier"]
    mae = mean_absolute_error(df["price"], final_pred)
    rmse = root_mean_squared_error(df["price"], final_pred)
    r2 = r2_score(df["price"], final_pred)
    return mae, rmse, r2


def baseline_predict(train, df):
    means = train.groupby("name")["base_price"].mean()
    return df["name"].map(means).fillna(train["base_price"].mean())

# Ridge
def make_pipeline(model):
    encoder = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_COLS),
        ("num", "passthrough", NUMERIC_COLS),
    ])
    return Pipeline([("encode", encoder), ("model", model)])


def fit_and_eval(model, train, val):
    pipe = make_pipeline(model)
    pipe.fit(train[FEATURE_COLS], train["base_price"]) # training
    pred = pipe.predict(val[FEATURE_COLS]) # predict base_price
    return pipe, evaluate(val, pred)



if __name__ == "__main__":
    df = load_processed()
    train, val, test = time_split(df)
    pred = baseline_predict(train, val)
    mae, rmse, r2 = evaluate(val, pred)
    print("Baseline val:", round(mae, 3), round(rmse, 3), round(r2, 3))
    pipe, (mae, rmse, r2) = fit_and_eval(Ridge(), train, val)
    print("Ridge val:", round(mae, 3), round(rmse, 3), round(r2, 3))

