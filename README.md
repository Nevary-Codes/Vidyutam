# Vidyutam ⚡📈

**Vidyutam** is an AI-powered electricity demand forecasting system designed to predict short-term and long-term power consumption for a given state. It enables utilities, grid operators, and policymakers to plan and optimize energy distribution based on projected demand trends.

## 🎯 Objective

To build a reliable and scalable forecasting system that incorporates:
- Historical consumption data
- Weather conditions
- Local holidays and events
- Time-based patterns (hour, day, seasonality)

## 🔍 Features

- 📊 Forecast electricity demand at state-level granularity
- 🌦️ Integrate real-time weather data
- 📅 Incorporate public holidays and events
- 🔁 Use lag features and rolling statistics for improved accuracy
- 🧠 ML models: XGBoost (baseline), LSTM/GRU (deep learning)
- 🖥️ Dashboard-ready output format (JSON/CSV)
- 🧪 Cross-validation and error metrics (MAE, RMSE, MAPE)

## 🧱 Tech Stack

- **Python** (pandas, scikit-learn, xgboost, keras)
- **Data Sources**: CSV, Weather API, Public holiday APIs
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Deployment-ready**: Flask API and HTML CSS frontend

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- pip for installing dependencies

### Setup

```bash
git clone https://github.com/your-username/vidyutam.git
cd vidyutam
pip install -r requirements.txt
```

### Launch Frontend Dashboard

```bash
python run app.py
```

## 📂 Project Structure

```
vidyutam/
├── ML/
├── templates/
├── static/
├── app.py                   # Streamlit dashboard (optional)
├── requirements.txt
└── README.md
```

## 🧠 Methodology

- Time-series feature engineering
- XGBoost regression model as baseline
- Seasonal decomposition and anomaly handling
- Deep learning extensions (LSTM, GRU)
- Grid search and rolling validation for tuning

## 📈 Sample Output

```
Date        | Predicted Demand (MW)
------------|-----------------------
2025-08-08  | 5890
2025-08-09  | 6123
2025-08-10  | 5987
```

## 🧪 Evaluation Metrics

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- Mean Absolute Percentage Error (MAPE)


---

> ⚡ *Vidyutam – Powering the future with smarter forecasts.*
