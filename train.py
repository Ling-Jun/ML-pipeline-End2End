import argparse
import numpy as np
import pandas as pd
import lightgbm as lgb
import matplotlib.pyplot as plt
from sktime.forecasting.compose import TransformedTargetForecaster, make_reduction
from sktime.forecasting.trend import PolynomialTrendForecaster
from sktime.transformations.series.detrend import Deseasonalizer, Detrender
from sktime.forecasting.model_selection import temporal_train_test_split
from sklearn.metrics import mean_absolute_error
from joblib import dump
import neptune.new as neptune
from neptune.new.types import File
import os

plt.style.use("bmh")
import warnings

warnings.filterwarnings("ignore")

# Construct an argument parser
args = argparse.ArgumentParser()
args.add_argument("-d", "--data", required=True, help="path to processed data")
args.add_argument("-mr", "--model_root", required=True, help="model root path")
args.add_argument("-fr", "--fig_root", required=True, help="image root path")
args = vars(args.parse_args())

print("Model root is " + str(args["model_root"]))
print("Image root is " + str(args["fig_root"]))


# processed_data = "../data/df2_processed.csv"
# model_root = "../artifacts/models/"
# fig_root = "../artifacts/figs/"

df = pd.read_csv(args["data"], index_col=0)
s = df.kw_cap
test_len = 365 * 24
s_train, s_test = temporal_train_test_split(s, test_size=test_len)

def plot_forecast(
    series_train,
    series_test,
    forecast,
    extra_title="",
    train_label="train",
    test_label="test",
    figsize=(12, 4),
):
    mae = mean_absolute_error(series_test, forecast)

    plt.figure(figsize=figsize)
    plt.title(extra_title + f"MAE: {mae:.4f}", size=18)
    series_train.plot(label=train_label, color="b")
    series_test.plot(label=test_label, color="g")
    forecast.index = series_test.index
    forecast.plot(label="forecast", color="r")
    plt.legend(prop={"size": 16})
    fig = plt.gcf()

    return fig, mae


def create_forecaster_w_desesonalizer(
    regressor,
    model="additive",
    sp=365 * 5,
    degree=1,
    window_length=10 * 24,
    strategy="recursive",
    scitype="infer",
):
    forecaster = TransformedTargetForecaster(
        [
            ("deseasonalize", Deseasonalizer(model=model, sp=sp)),
            ("detrend", Detrender(forecaster=PolynomialTrendForecaster(degree=degree))),
            (
                "forecast",
                make_reduction(
                    regressor,
                    window_length=window_length,
                    strategy=strategy,
                    scitype=scitype,
                ),
            ),
        ]
    )

    return forecaster


def train_forecaster(train, test, forecaster, train_label="train", test_label="test"):
    forecaster.fit(train)
    fh = np.arange(len(test)) + 1
    y_pred = forecaster.predict(fh=fh)
    fig, mae = plot_forecast(
        train,
        test,
        y_pred,
        train_label=train_label,
        test_label=test_label,
        figsize=(14, 4),
    )

    return fig, mae, forecaster

env_vars = os.environ
print(env_vars)
run = neptune.init(project="lingjun/Remote-Community-Power-Usage", 
    api_token=env_vars['NEPTUNE_API_TOKEN'],
    run="REM-50"
)  
params = {
    "n_estimators": 30,
    "learning_rate": 0.05,
    "seasonal_period": 365 * 24,
    "window_length":  10 * 24
}

regressor = lgb.LGBMRegressor(n_estimators=params["n_estimators"], learning_rate=params["learning_rate"])
forecaster = create_forecaster_w_desesonalizer(regressor, sp=params["seasonal_period"], window_length=params["window_length"])
img, mae, forecaster = train_forecaster(s_train, s_test, forecaster)
img.savefig(args["fig_root"]+'/figure.png')


model_path = args["model_root"] + "lgbm_forecaster.pickle"
print(model_path)
if model_path:
    dump(forecaster, model_path)
    print("Model is saved at " + model_path)

run["parameters"] = params
# uploads model to Neptune, but it's stored in Runs, not Models on Neptune UI
# We have to use File.as_pickle(<path>) to upload the pickled model, just .upload(<path>) won't work
# Can we upload File as it is, instead of as_pickle()??
run["model/pickled_model"].upload(File.as_pickle(forecaster))
# run["model/pickled_model"].upload(File.upload_files("lgbm_forecaster.pickle"))
