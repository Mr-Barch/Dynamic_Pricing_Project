# Dynamic Pricing Engine

Predicts the base price of an Uber/Lyft ride in Boston and shows surge pricing in a Streamlit demo.

Final price = predicted base price x surge multiplier.

## Data

Rideshare dataset (Kaggle): "Uber and Lyft Dataset Boston, MA"
https://www.kaggle.com/datasets/brllrb/uber-and-lyft-dataset-boston-ma

Boston, 26.11.2018 - 18.12.2018, 693,071 rows. Download `rideshare_kaggle.csv`, rename it to
`raw_data.csv` and put it in the `data/` folder. Data and the trained model are not stored in the repository.

## Project structure

```
data/raw_data.csv          raw data (not in git)
data/processed_data.csv    cleaned data (created by preprocess.py, not in git)
notebooks/eda.ipynb        EDA: correlation of hour and weather with price
models/pricing_model.pkl   trained model (created by train_model.py, not in git)
src/preprocess.py          cleaning and features
src/train_model.py         training, model comparison, saving the best model
src/surge.py               surge rules
app.py                     Streamlit demo
```

## How it works

1. **Cleaning** (`src/preprocess.py`): drop rows without price (Uber Taxi) and duplicates,
   target `base_price = price / surge_multiplier`, remove outliers with the 3 x IQR rule per product.
2. **Features**: `name`, `source`, `destination` (one-hot) and `distance`.
   Hour and weather are not used as features: their correlation with `base_price`
   is practically zero (|r| < 0.002, see `notebooks/eda.ipynb`).
3. **Split by time**: 70% train, 10% validation, 20% test (no random split).
4. **Models**: baseline (mean price of the product), Ridge, RandomForest, XGBoost.
   The best model is chosen by MAE on validation. Metrics are computed for the final price:
   predicted `base_price` x real `surge_multiplier`.
5. **Surge** (`src/surge.py`): business rules, not learned from data.

## Results

| Model | MAE (validation) | RMSE | R2 |
|---|---|---|---|
| Baseline | 2.891 | 3.854 | 0.827 |
| Ridge | 1.651 | 2.231 | 0.942 |
| RandomForest | 0.991 | 1.484 | 0.974 |
| XGBoost | 1.027 | 1.504 | 0.974 |

Best model: RandomForest. On the test set: MAE 0.998 USD, R2 0.974 (baseline: MAE 2.897 USD).

## Surge rules

Surge starts at 1.0 and the following amounts are added:

| Condition | Added |
|---|---|
| Rush hour (7-9 and 16-19) | +0.35 |
| Light rain | +0.15 |
| Heavy rain | +0.40 |
| Event | +0.25 |
| Night (22-5) on weekends | +0.20 |

The result is rounded to a step of 0.25 and limited to 1.0 - 3.0.
No surge for Shared, UberPool and WAV.

## How to run

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

python src/preprocess.py
python src/train_model.py
python -m streamlit run app.py
```
