from flask import Flask, request, render_template
from flask_cors import cross_origin

import pickle
import pandas as pd


app = Flask(__name__)
model = pickle.load(open("Model/flight_price_rf.pkl", "rb"))


@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")


def get_datetime_parts(datetime_str):
    dt = pd.to_datetime(datetime_str, format="%Y-%m-%dT%H:%M")
    return dt.day, dt.month, dt.hour, dt.minute


def one_hot_encode(value, categories, prefix):
    encoded = {f"{prefix}_{cat.replace(' ', '')}": 0 for cat in categories}
    key = f"{prefix}_{value.replace(' ', '')}"
    if key in encoded:
        encoded[key] = 1
    else:
        encoded[f"{prefix}_Other"] = 1  # Fallback for unknown category
    return encoded


@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        # Parse departure and arrival times
        dep_time = request.form["Dep_Time"]
        arr_time = request.form["Arrival_Time"]
        journey_day, journey_month, dep_hour, dep_min = get_datetime_parts(dep_time)
        _, _, arrival_hour, arrival_min = get_datetime_parts(arr_time)

        # Duration calculation
        duration_hour = abs(arrival_hour - dep_hour)
        duration_min = abs(arrival_min - dep_min)

        # Stops
        total_stops = int(request.form["stops"])

        # One-hot encode Airline
        airline = request.form["airline"]
        airline_categories = [
            "Jet Airways",
            "IndiGo",
            "Air India",
            "Multiple carriers",
            "SpiceJet",
            "Vistara",
            "GoAir",
        ]
        airline_encoded = one_hot_encode(airline, airline_categories, "Airline")
        airline_encoded.setdefault("Airline_Other", 0)  # Ensure key exists

        # One-hot encode Source
        source = request.form["Source"]
        source_categories = ["Delhi", "Kolkata", "Mumbai", "Chennai"]
        source_encoded = one_hot_encode(source, source_categories, "Source")

        # One-hot encode Destination
        destination = request.form["Destination"]
        dest_categories = ["Cochin", "Delhi", "Hyderabad", "Kolkata"]
        dest_encoded = one_hot_encode(destination, dest_categories, "Destination")

        # Prepare model input
        input_features = [
            total_stops,
            journey_day,
            journey_month,
            dep_hour,
            dep_min,
            arrival_hour,
            arrival_min,
            duration_hour,
            duration_min,
            airline_encoded["Airline_AirIndia"],
            airline_encoded["Airline_GoAir"],
            airline_encoded["Airline_IndiGo"],
            airline_encoded["Airline_JetAirways"],
            airline_encoded["Airline_Multiplecarriers"],
            airline_encoded["Airline_Other"],
            airline_encoded["Airline_SpiceJet"],
            airline_encoded["Airline_Vistara"],
            source_encoded["Source_Chennai"],
            source_encoded["Source_Kolkata"],
            source_encoded["Source_Mumbai"],
            dest_encoded["Destination_Cochin"],
            dest_encoded["Destination_Delhi"],
            dest_encoded["Destination_Hyderabad"],
            dest_encoded["Destination_Kolkata"],
        ]

        # Predict
        prediction = model.predict([input_features])
        output = round(prediction[0], 2)

        return render_template(
            "index.html", prediction_text=f"Your Flight price is Rs. {output}"
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
