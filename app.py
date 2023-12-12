from flask import Flask, request, render_template, jsonify, send_from_directory
import requests
import pandas as pd

import matplotlib
matplotlib.use('Agg')  # Matplotlib backend to 'Agg'
import matplotlib.pyplot as plt

import os
import io
import base64

app = Flask(__name__)


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Functions
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def get_api_key():
    with open('api_key_g.txt', 'r') as file:
        return file.read().strip()

    
def fetch_stock_data(symbol, api_key):
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()

        # Checking if the expected data is in the response
        if 'Time Series (Daily)' in data:
            time_series = data['Time Series (Daily)']
            df = pd.DataFrame.from_dict(time_series, orient='index')
            df.index = pd.to_datetime(df.index)
            for col in df.columns:
                df[col] = df[col].astype(float)
            df.sort_index(inplace=True)
            return df
        else:
            # Handling 'Time Series (Daily)' is not in the response
            print("Data not in expected format:", data)
            return None
    else:
        print("Failed to retrieve data:", response.status_code)
        return None    

def create_plot(df, symbol):
    """ Creating a plot and return its URL """

    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['4. close'], label='Closing Price', color='blue')
    plt.title(f'Stock Closing Prices of {symbol} Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)

    # Saving plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    plot_url = base64.b64encode(buf.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{plot_url}"



def fetch_stock_data_with_stats(symbol, api_key):
    """Fetching & calculating statistics"""
    df = fetch_stock_data(symbol, api_key)
    if df is not None:
        stats = {
            'mean': df['4. close'].mean(),
            'max': df['4. close'].max(),
            'min': df['4. close'].min(),
        }
        return df, stats
    else:
        return None, None
    
def calculate_stats(df):
    stats = {
        'mean': df['4. close'].mean(),
        'max': df['4. close'].max(),
        'min': df['4. close'].min(),
        'std_dev': df['4. close'].std(),  # Standard deviation
        'latest': df['4. close'].iloc[-1]
        # You can add more statistics here as needed
    }
    return stats


# Line Chart for Daily Closing Prices
def plot_closing_prices(df, symbol):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df.index, df['4. close'], label='Closing Price', color='blue')
    ax.set_title(f'{symbol} Closing Prices')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.grid(True)
    ax.legend()
    return fig


# Bar Chart for Trading Volume
def plot_trading_volume(df, symbol):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(df.index, df['5. volume'], color='orange')
    ax.set_title(f'{symbol} Trading Volume')
    ax.set_xlabel('Date')
    ax.set_ylabel('Volume')
    ax.grid(True)
    return fig


# Moving Average
def plot_moving_average(df, symbol, window_size=20):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df.index, df['4. close'], label='Closing Price', color='blue', alpha=0.5)
    ax.plot(df.index, df['4. close'].rolling(window=window_size).mean(), label=f'{window_size}-Day Moving Average', color='red')
    ax.set_title(f'{symbol} Moving Average')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.grid(True)
    ax.legend()
    return fig


# Histogram of Daily Price Changes

def plot_daily_price_change_histogram(df, symbol):
    fig, ax = plt.subplots(figsize=(10, 4))
    daily_changes = df['4. close'].pct_change().dropna()
    ax.hist(daily_changes, bins=50, color='green', alpha=0.7)
    ax.set_title(f'{symbol} Daily Price Changes')
    ax.set_xlabel('Percentage Change')
    ax.set_ylabel('Frequency')
    ax.grid(True)
    return fig



# Saving Plots as Images
def create_plots(df, symbol):
    plot_functions = [plot_closing_prices, plot_trading_volume, plot_moving_average, plot_daily_price_change_histogram]
    urls = []

    for plot_func in plot_functions:
        fig = plot_func(df, symbol)
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        plot_url = base64.b64encode(buf.getvalue()).decode('utf-8')
        urls.append(f"data:image/png;base64,{plot_url}")

    return urls











#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ROUTES
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Home page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/get-stock-data', methods=['POST'])
def stock_data():
    try:
        symbol = request.form['symbol']
        api_key = get_api_key()
        df = fetch_stock_data(symbol, api_key)
        if df is not None:
            print("Dataframe fetched successfully")  # Debugging
            plot_urls = create_plots(df, symbol)
            stats = calculate_stats(df)
            print("Plots and stats generated")  # Debugging
            return jsonify({'plot_urls': plot_urls, 'stats': stats})
        else:
            print("Failed to fetch data")  # Debugging
            return jsonify({'error': 'Failed; invalid symbol or exceeded API rate limit'})
    except Exception as e:
        print("An error occurred:", e)
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
