from flask import Flask, render_template, redirect, url_for, request, jsonify
import pandas as pd
from ML.call import get_excel
import requests

app = Flask(__name__)
app.config["SECRET_KEY"] = ""
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/predict', methods=["GET", "POST"])
def predict():
    date1 = request.form.get("start_date")
    date2 = request.form.get("end_date")

    print(f"date1: {date1}\ndate2: {date2}")
    


    return render_template("dashboard.html")
    
@app.route('/get-predictions', methods=['GET'])
def get_predictions():
    try:
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        get_excel(start_date, end_date)

        df = pd.read_excel("Predictions.xlsx")

        df["Date"] = pd.to_datetime(df["Date"])  


        if not start_date or not end_date:
            return jsonify({"error": "Missing date parameters"})

        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        # Filter data by date range
        df_filtered = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

        if df_filtered.empty:
            return jsonify({"error": "No data available for selected range"})

        # Aggregate data by month (use 'M' for month grouping)
        df_filtered["Month"] = df_filtered["Date"].dt.to_period("M")  # Convert to "YYYY-MM"
        df_grouped = df_filtered.groupby("Month")["Electricity Required"].sum().reset_index()  # Sum for each month

        # Convert dataframe to JSON
        data = {
            "labels": df_grouped["Month"].astype(str).tolist(),  # Convert period to string
            "values": df_grouped["Electricity Required"].tolist(),  # Monthly aggregated data
        }

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})
    
    

if __name__ == "__main__":
    app.run(port=5000, debug=True)