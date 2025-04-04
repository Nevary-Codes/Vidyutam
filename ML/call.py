import pandas as pd
import requests
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(42)

API_KEY = "BSCBTUZPLE8NG5DP93RMXJLBJ"
API_KEY1 = "9776QD9CJJ2D6V72LBGUFC9CB"
API_KEY2 = "GGML2K3YSE444K7M26JHYMUS4"
API_KEY3 = "JJQ3THWN98WC6EB2664QU3T7C"
API_KEY4 = "369DGLGMGV8MZJ2FL5H5TM2J6"
API_KEY5 = "YZKHR268UFVXTHV7AAHTA2SGC"
API_KEY6 = "7YXZYUY4G7BQHLMTEWJDCZXHP"
API_KEY7 = "J7VG3JLB5DVT929K54E5FYLVA"

API_KEY8 = "JQG3XP7LAYUC8GU5VLAZX7V88"

API_KEY9 = "EJ59UR2LZSBUJ3PGNXEDMAAFG"


def load_model(name):
    loaded_model = pickle.load(open(name, "rb"))
    return loaded_model


def check_holiday(data, holidays):
    data["Holidays"] = data["datetime"].isin(holidays["Date"])


def convert_date(data):
    data["currentYear"] = data["datetime"].apply(lambda x: x.year)
    data["currentMonth"] = data["datetime"].apply(lambda x: x.month)
    data["currentDay"] = data["datetime"].apply(lambda x: x.day)
    data["currnetDayOfWeek"] = data["datetime"].apply(lambda x: x.weekday())
    data["currnetDayOfYear"] = data["datetime"].apply(lambda x: x.timetuple().tm_yday)
    data.drop(labels=["datetime"], axis=1, inplace=True)


def change_data(data, holidays):
    check_holiday(data, holidays)
    convert_date(data)



def process(date1, date2):
    api = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Delhi%2CINDIA/{date1}/{date2}?unitGroup=metric&contentType=csv&include=days&include=hours&key={API_KEY}"
    holidays = pd.read_csv("Data/Public Holidays/2025.csv")
    holidays = holidays[~holidays['Type'].isin(['observance', 'Restricted', 'Restricted Holiday'])]


    date_range = pd.date_range(start=date1, end=date2, freq='h')
    global df
    df = pd.DataFrame(date_range, columns=['datetime'])
    df['Hour'] = df['datetime'].dt.hour
    df['datetime'] = df['datetime'].dt.date
    
    
    response = requests.get(api)
    with open("output.csv", "wb") as file:
        file.write(response.content)
    
    weather = pd.read_csv("output.csv")
    weather = weather[["datetime", "tempmax", "tempmin", "temp", "feelslikemax", "feelslikemin", "feelslike", "solarenergy"]]
    weather["datetime"] = pd.to_datetime(weather["datetime"])
    weather["datetime"] = weather["datetime"].dt.date
    weather_excel = weather.drop("solarenergy", axis=1)
    weather_excel.to_excel("Weather.xlsx")
    

    result = pd.merge(df, weather, on="datetime", how="left")
    
    change_data(result, holidays)
    result.drop_duplicates(inplace=True)
    result.reset_index(inplace=True, drop=True)
    
    return result


def get_excel(date1, date2):
    dat = process(date1, date2)
    loaded_model = load_model("best-model-xgbr-1.pkl")
    y_preds = loaded_model.predict(dat)

    predictions = pd.DataFrame(columns=["Date", "Electricity Required"])
    predictions["Date"] = df["datetime"].astype(object)
    predictions["Electricity Required"] = y_preds
    
    excel_filename = "Predictions.xlsx"
    predictions.to_excel(excel_filename, index=False)
    


def get_monthly_data(date1, date2):
    get_excel(date1, date2)
    predictions = pd.read_excel("Predictions.xlsx")
    predictions["Date"] = pd.to_datetime(predictions["Date"])
    predictions.set_index('Date', inplace=True)
    predictions["Electricity Required"] = predictions["Electricity Required"]/1000
    monthly_data = predictions.resample('ME').sum()
    monthly_data.reset_index(inplace=True)
    monthly_data["Date"] = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    monthly_data.to_excel("Monthly_Predictions.xlsx", index=False)
    get_graphs()

def get_graphs():
    data = pd.read_excel("Predictions.xlsx")
    monthly_data = pd.read_excel("Monthly_Predictions.xlsx")
    data['Date'] = data['Date'] + pd.to_timedelta(data.index, unit='h')

    # Line chart
    fig, ax = plt.subplots(figsize=(20,5))
    ax.plot(data["Date"], data["Electricity Required"])
    ax.set_xlabel("Date")
    ax.set_ylabel("Energy")
    fig.savefig("/Users/aryanmanchanda/Desktop/Vidyutam/Web/static/images/line_chart.jpg")
    plt.close(fig)  # Close the figure to free memory

    # Pie chart
    fig, ax = plt.subplots()
    ax.pie(monthly_data["Electricity Required"], autopct='%1.1f%%')
    ax.legend(monthly_data["Date"], loc="center left", bbox_to_anchor=(1, 0.5))
    ax.set_title("Monthly Energy Consumption")
    fig.savefig("/Users/aryanmanchanda/Desktop/Vidyutam/Web/static/images/pie_chart.jpg")
    plt.close(fig)

    total_sum = data["Electricity Required"].sum() / 1000

    # Bar chart
    fig, ax = plt.subplots(figsize=(8, 2)) 
    ax.barh(y=[0], width=[total_sum], color='skyblue')
    ax.set_xlim(0, total_sum * 2)
    ax.text(total_sum + total_sum * 2 * 0.02, 0, f'{total_sum} GW', va='center', ha='left', color='black')
    ax.get_yaxis().set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_xaxis().set_ticks([])
    ax.set_title("Sum of Electricity Required (in GW)")
    plt.savefig("/Users/aryanmanchanda/Desktop/Vidyutam/Web/static/images/total.jpg")
    plt.close(fig)

    # Monthly line chart
    fig, ax = plt.subplots(figsize=(12,5))
    ax.plot(monthly_data["Date"], monthly_data["Electricity Required"])
    ax.set_xlabel("Months")
    ax.set_ylabel("Energy")
    plt.savefig("/Users/aryanmanchanda/Desktop/Vidyutam/Web/static/images/monthly_line.jpg")
    plt.close(fig)