from flask import Flask, request, render_template, jsonify, send_from_directory
import requests
import pandas as pd
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
    


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ROUTES
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Home page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')



@app.route('/get-stock-data', methods=['POST'])
def stock_data():
    symbol = request.form['symbol']
    api_key = get_api_key()
    df, stats = fetch_stock_data_with_stats(symbol, api_key)
    if df is not None:
        plot_url = create_plot(df, symbol)
        return jsonify({'plot_url': plot_url, 'stats': stats})
    else:
        return jsonify({'error': 'invalid symbol or exceeded API rate limit'})
    

if __name__ == '__main__':
    app.run(debug=True)
