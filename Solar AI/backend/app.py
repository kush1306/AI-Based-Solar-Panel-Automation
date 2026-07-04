from flask import Flask, jsonify, request

import sys
import os

# Add src folder to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from data_loader import load_full_dataset
from demand_forecaster import DemandForecaster
from battery_optimizer import RuleBasedOptimizer

app = Flask(__name__)

print("Loading Delhi dataset...")

df = load_full_dataset()

print("Training demand forecasting model...")

forecaster = DemandForecaster()

forecaster.fit(df)

optimizer = RuleBasedOptimizer()


@app.route("/")
def home():

    return jsonify(
        {
            "message": "AI Solar Panel Automation API",
            "status": "running"
        }
    )


@app.route("/weather")
def weather():

    latest = df.tail(1).to_dict("records")[0]

    return jsonify(latest)


@app.route("/forecast")
def forecast():

    prediction = float(
        forecaster.predict(df.tail(48))[0]
    )

    return jsonify(
        {
            "predicted_demand_kw": prediction
        }
    )


@app.route("/optimize", methods=["POST"])
def optimize():

    body = request.json

    solar_generation = float(body["solar_generation"])

    prediction = float(
        forecaster.predict(df.tail(48))[0]
    )

    latest = df.tail(1).copy()

    latest["demand_kw"] = prediction

    latest["shortwave_radiation"] = solar_generation * 1000

    result = optimizer.run(latest)

    return jsonify(
        result.to_dict("records")[0]
    )


if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )